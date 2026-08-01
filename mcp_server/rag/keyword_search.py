import re
from rank_bm25 import BM25Plus


def tokenize(text: str) -> list[str]:
    """تقطيع النص إلى كلمات صغيرة وتجاهل العلامات"""
    return re.findall(r"[a-z0-9]+", text.lower())


class KeywordStore:
    def __init__(self):
        self.rows = []          # تخزين المستندات والـ Metadata
        self._bm25 = None
        self._dirty = True      # مؤشر لمعرفة هل تم تحديث البيانات للحاجة لإعادة بناء الفهرس

    def upsert(self, payload, metadata):
        """إضافة مستند جديد للذاكرة"""
        self.rows.append({"payload": payload, "metadata": metadata})
        self._dirty = True

    def _rebuild_index(self):
        """بناء فهرس BM25 عند إضافة بيانات جديدة"""
        corpus = [tokenize(self._as_text(r["payload"])) for r in self.rows]
        self._bm25 = BM25Plus(corpus) if corpus else None
        self._dirty = False

    @staticmethod
    def _as_text(payload) -> str:
        if isinstance(payload, str):
            return payload
        return payload.get("event_summary") or payload.get("text") or str(payload)

    def query(self, query_text: str, top_k: int = 3, filter: dict | None = None):
        """البحث عن أفضل المستندات المطبقة للـ Query والـ Filter"""
        # فلترة البيانات حسب الـ Filter (مثل entity_id)
        candidate_idxs = [
            i for i, r in enumerate(self.rows)
            if not filter or all(r["metadata"].get(k) == v for k, v in filter.items())
        ]
        if not candidate_idxs:
            return []

        if self._dirty:
            self._rebuild_index()
        if self._bm25 is None:
            return []

        tokens = tokenize(query_text)
        scores = self._bm25.get_scores(tokens)

        # حساب المطابقة وتقييم النتائج
        overlapping = {
            i for i in candidate_idxs
            if set(tokens) & set(tokenize(self._as_text(self.rows[i]["payload"])))
        }
        ranked = sorted(overlapping, key=lambda i: scores[i], reverse=True)
        return [self.rows[i] for i in ranked[:top_k]]
