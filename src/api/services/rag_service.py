from src.rag.rag import RAG


class RagService:
    def __init__(self):
        self.rag = RAG()

    async def make_conversation(self, question: str, user_id: str):
        try:
            result = await self.rag.run_workflow(question=question, user_id=user_id)
            return {
                "success": True,
                "answer": result["answer"]
            }
        except Exception as e:
            return {"error": str(e)}