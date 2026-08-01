from rag_tool import search_knowledge_base_handler

if __name__ == "__main__":
    print("==========================================")
    print("DEMO: MCP Knowledge Base Search Tool (RAG)")
    print("==========================================\n")

    # سيناريو 1: مستخدم عادي (front_desk) يسأل عن زيارة أذن
    print("Scenario 1: Role='front_desk' searching for 'ear infection' for client_101")
    result1 = search_knowledge_base_handler(
        {"query": "ear infection drops", "entity_id": "client_101", "top_k": 2},
        session_role="front_desk"
    )
    print("Result:\n", result1)
    print("-" * 50)

    # سيناريو 2: مستخدم بعث عن دواء محكوم ولكن صلاحيته لا تسمح (Front Desk)
    print("\nScenario 2: Role='front_desk' searching for 'controlled pain medication'")
    result2 = search_knowledge_base_handler(
        {"query": "controlled pain medication",
            "entity_id": "client_101", "top_k": 2},
        session_role="front_desk"
    )
    print("Result:\n", result2)
    print("-" * 50)

    # سيناريو 3: نفس البحث السابق ولكن بصلاحية 'doctor'
    print("\nScenario 3: Role='doctor' searching for 'controlled pain medication'")
    result3 = search_knowledge_base_handler(
        {"query": "controlled pain medication",
            "entity_id": "client_101", "top_k": 2},
        session_role="doctor"
    )
    print("Result:\n", result3)
    print("==========================================")
