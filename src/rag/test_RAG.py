from typing import List
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict
from langgraph.graph import START, StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    messages: List


class TestRAG:
    def __init__(self):
        self.env_loaded = self.get_env()
        self.llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
        self.system_prompt = "You are a helpful assistant."
        self.app = None
        self.memory = MemorySaver()


    def get_env(self) -> bool:
        try:
            load_dotenv()
            return True
        except Exception as e:
            print(f"Error loading .env file: {e}")
            return False


    def search_context(self, state: State) -> State:
        # DB search fonksiyonu bekleniyor
        documents = [Document(page_content="The sea is a large body of saltwater.")]
        return {"context": documents}

    def get_answer(self, state: State) -> State:
        context_text = "\n".join([doc.page_content for doc in state["context"]])

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Context: {context_text}\n\nQuestion: {state['question']}")
        ]

        answer = self.llm.invoke(messages)
        return {"answer": answer.content}

    def build_graph(self):
        graph = StateGraph(State)

        graph.add_node("search", self.search_context)
        graph.add_node("answer", self.get_answer)

        graph.add_edge(START, "search")
        graph.add_edge("search", "answer")
        graph.add_edge("answer", END)

        return graph

    def compile_graph(self):
        graph = self.build_graph()
        self.app = graph.compile(checkpointer=self.memory)

    def run_workflow(self, question: str, thread_id: str = "1"):
        if self.app is None:
            self.compile_graph()

        result = self.app.invoke(
            {"question": question, "context": [], "answer": ""},
            config={"configurable": {"thread_id": "1"}}
        )

        return result


if __name__ == "__main__":
    # RAG instance oluştur
    rag = TestRAG()

    # Test sorusu
    test_question = "What is the sea?"

    print(f"Question: {test_question}")
    print("-" * 50)

    # Workflow'u çalıştır
    result = rag.run_workflow(test_question)

    print(f"\nContext: {result['context']}")
    print(f"\nAnswer: {result['answer']}")

    print("-" * 50)

    test_question = "What did I just ask?"

    print(f"Question: {test_question}")
    print("-" * 50)

    # Workflow'u çalıştır
    result = rag.run_workflow(test_question)

    print(f"\nContext: {result['context']}")
    print(f"\nAnswer: {result['answer']}")
