from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from keyword_search import KeywordStore

# 1. إنشاء مخزن البيانات
knowledge_store = KeywordStore()

# 2. إدخال مستندات البيانات (ملاحظات زيارات سابقة أو سياسات)


def index_domain_documents():
    docs = [
        {
            "text": "Visit 2026-03-01: Patient reported mild ear infection. Prescribed antibiotic drops.",
            "entity_id": "client_101",
            "role_required": "any",
        },
        {
            "text": "Visit 2026-05-14: Administered controlled pain medication. Requires doctor sign-off.",
            "entity_id": "client_101",
            "role_required": "doctor",
        },
        {
            "text": "Visit 2026-01-10: Annual routine checkup. Everything normal.",
            "entity_id": "client_202",
            "role_required": "any",
        },
    ]
    for doc in docs:
        knowledge_store.upsert(
            payload=doc["text"],
            metadata={
                "entity_id": doc["entity_id"],
                "role_required": doc["role_required"],
            },
        )


# فهرسة المستندات عند التشغيل
index_domain_documents()

# 3. تعريف الـ Schema الخاصة بالأداة (Pydantic Model)


class SearchKnowledgeBaseInput(BaseModel):
    query: str = Field(...,
                       description="Keywords or questions to search for in knowledge base")
    entity_id: str = Field(...,
                           description="Scope search to a specific client/entity ID")
    top_k: int = Field(default=3, ge=1, le=10,
                       description="Number of top results to return")

    # يمنع أي بمتغيرات إضافية غير معرفة
    model_config = ConfigDict(extra="forbid")

# 4. الـ Handler الوظيفي للأداة مع التحقق من الصلاحيات


def search_knowledge_base_handler(args: dict, session_role: str) -> str:
    # التحقق من المدخلات عبر الـ Schema
    parsed = SearchKnowledgeBaseInput.model_validate(args)

    # البحث في الـ Store
    matches = knowledge_store.query(
        query_text=parsed.query,
        top_k=parsed.top_k,
        filter={"entity_id": parsed.entity_id},
    )

    # التحقق من صلاحية المستخدم (Authorization Check)
    visible_results = [
        m for m in matches
        if m["metadata"]["role_required"] in ("any", session_role)
    ]

    if not visible_results:
        return "No relevant records or policy docs found for this query/role."

    return "\n\n".join(m["payload"] for m in visible_results)
