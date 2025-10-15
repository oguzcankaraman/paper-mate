"""
# noinspection PyMethodMayBeStatic class içinde private method olarak kullanmak istenilen methodların
static function olarak kullan uyarısını bastırmak için
# type: ignore[arg-type] IDE'nin verilen State classını beklenen fonksiyon olarak algılayamaması.
Önerilen kullanım benim yaptığım şekilde: https://python.langchain.com/docs/tutorials/rag/#overview
"""
import logging
from dataclasses import dataclass
from typing import List, Any, Annotated
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage
from typing_extensions import TypedDict
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from src.rag import VectorStore

class State(TypedDict, total=False):
    """
    graphta nodeler arası iletişimde kullanılması için custom bir State classı
    """
    question: str
    context: List[Document]
    answer: str | list[str] | Any
    messages: Annotated[list[BaseMessage], add_messages]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RAGConfig:
    model_name: str = "llama3:8b"
    system_prompt: str = "You are a helpful assistant."
    max_retries: int = 3
    timeout: int = 30

class RAG:
    def __init__(self, config: RAGConfig = None, user_id: str = "12345"):
        self.config = config or RAGConfig()
        self.env_loaded = self._get_env()
        if not self.env_loaded:
            raise Exception("Environment variables not loaded.")
        self.llm = ChatOllama(model=self.config.model_name)
        self.system_prompt = self.config.system_prompt
        self.app = None
        self.memory = MemorySaver()
        self.vector_store = VectorStore(user_id=user_id )
        logger.info(f"Initialized RAG with model: {self.config.model_name}")

    # noinspection PyMethodMayBeStatic
    def _get_env(self) -> bool:
        try:
            load_dotenv()
            return True
        except Exception as e:
            print(f"Error loading .env file: {e}")
            return False

    # noinspection PyMethodMayBeStatic
    def _search_context(self, state: State) -> State:
        try:
            documents = [self.vector_store.find_document(state["question"])]# Hali hazırda list of Document döndüren bir method/fonksiyon olmalı
            if not documents or not documents[0]:
                return {"context": []}
            return {"context": documents}
        except Exception as e:
            print(f"Error searching context: {e}")
            return {"context": []}

    def _get_answer(self, state: State) -> State:
        try:
            context_text = "\n".join([doc.page_content for doc in state["context"]])
            messages = state.get("messages", [])

            if not messages:
                messages = [
                    SystemMessage(content=self.system_prompt),
                    SystemMessage(content=f"Context: {context_text}")
                ]
            messages.append(HumanMessage(content=state['question']))

            answer = self.llm.invoke(messages)
            messages.append(answer)
            return {"answer": answer.content, "messages": messages}
        except Exception as e:
            return {"answer": f"Error: {str(e)}", "messages": messages}

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(State)# type: ignore[arg-type]

        graph.add_node("search", self._search_context)
        graph.add_node("answer", self._get_answer)

        graph.add_edge(START, "search")
        graph.add_edge("search", "answer")
        graph.add_edge("answer", END)

        return graph

    def _compile_graph(self) -> None:
        graph = self._build_graph()
        self.app = graph.compile(checkpointer=self.memory)

    def run_workflow(self, question: str, thread_id: str = "1") -> State:
        """
        Bütün süreci çalıştıran ana method. Sırasıyla verilen context üzerinde
        benzerlik araması yaparak benzer sonucu alır, bu sonucu kullanılan LLM'e gösterir ve
        çıktı alır
        :param question: client tarafından verilecek olan girdi
        :param thread_id: konuşma geçmişinin tutulduğu id
        :return: Statein tamamını döndürür
        :raise: ValueError: If inputs are invalid
        """
        logger.info(f"Processing question: {question[:50]}... (thread: {thread_id})")
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        if not thread_id:
            raise ValueError("Thread ID cannot be empty")
        if self.app is None:
            self._compile_graph()

        logger.info(f"Completed workflow (thread: {thread_id})")
        return self.app.invoke(
            {"question": question, "context": [], "answer": ""},
            config={"configurable": {"thread_id": thread_id}}
        )



if __name__ == "__main__":
    # RAG instance oluştur
    rag = RAG()

    # Test sorusu
    test_question = "Yapay zeka etiği neyi amaçlar?"

    print(f"Question: {test_question}")
    print("-" * 50)

    # Workflow'u çalıştır
    result = rag.run_workflow(test_question, "thread123")

    print(f"\nContext: {result['context']}")
    print(f"\nAnswer: {result['answer']}")

    print("-" * 50)

    test_question = "Oğuzla Yağız neden çok mutlu?"

    print(f"Question: {test_question}")
    print("-" * 50)

    # Workflow'u çalıştır
    result = rag.run_workflow(test_question, "thread123")

    print(f"\nContext: {result['context']}")
    print(f"\nAnswer: {result['answer']}")

    print("-" * 50)

    test_question = "Bir önceki sorduğum soru neydi?"

    print(f"Question: {test_question}")
    print("-" * 50)

    # Workflow'u çalıştır
    result = rag.run_workflow(test_question, "thread123")

    print(f"\nContext: {result['context']}")
    print(f"\nAnswer: {result['answer']}")