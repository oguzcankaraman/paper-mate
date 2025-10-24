"""
# noinspection PyMethodMayBeStatic class içinde private method olarak kullanmak istenilen methodların
static function olarak kullan uyarısını bastırmak için
# type: ignore[arg-type] IDE'nin verilen State classını beklenen fonksiyon olarak algılayamaması.
Önerilen kullanım benim yaptığım şekilde: https://python.langchain.com/docs/tutorials/rag/#overview
"""
import logging
from dataclasses import dataclass
from typing import List, Annotated
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from typing_extensions import TypedDict
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from src.api.database.crud import (
    create_conversation,
    create_message,
    update_conversation
)
from src.api.database.database import SessionLocal


from src.rag import VectorStore

class State(TypedDict, total=False):
    question: str
    context: List[Document]
    answer: str
    messages: Annotated[list[BaseMessage], add_messages]
    user_id: int
    conversation_id: int

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RAGConfig:
    model_name: str = "llama3:8b"
    system_prompt: str = "You are a helpful assistant."
    max_retries: int = 3
    timeout: int = 30

class RAG:
    def __init__(self, config: RAGConfig = None):
        self.config = config or RAGConfig()
        self.env_loaded = self._get_env()
        if not self.env_loaded:
            raise Exception("Environment variables not loaded.")
        self.llm = ChatOllama(model=self.config.model_name)
        self.system_prompt = self.config.system_prompt
        self.app = None
        self.memory = MemorySaver()
        self.vector_store = VectorStore()
        from src.api.database.database import init_db
        init_db()
        self.db = SessionLocal()
        logger.info(f"Initialized RAG with model: {self.config.model_name}")

    def __del__(self):
        if hasattr(self, "db"):
            self.db.close()

    # noinspection PyMethodMayBeStatic
    def _get_env(self) -> bool:
        try:
            load_dotenv()
            return True
        except Exception as e:
            print(f"Error loading .env file: {e}")
            return False

    # noinspection PyMethodMayBeStatic
    async def _search_context(self, state: State) -> State:
        try:
            user_id = state.get("user_id")
            if not user_id:
                return {"context": []}

            document = await self.vector_store.find_document(user_id, state["question"])

            if not document:
                return {"context": []}

            return {"context": document}
        except Exception as e:
            logger.error(f"Error searching context: {e}")
            return {"context": []}

    async def _get_answer(self, state: State) -> State:
        try:
            from src.api.database.crud import get_messages_by_conversation
            from langchain_core.messages import AIMessage

            context_text = "\n".join([doc.page_content for doc in state["context"]])

            db_messages = get_messages_by_conversation(self.db, state["conversation_id"])
            messages = state.get("messages", [])

            if not messages:
                messages.append(SystemMessage(content=self.system_prompt))

            if context_text:
                messages.append(SystemMessage(content=f"Context: {context_text}"))

            for msg in db_messages:
                role = str(msg.role)
                content = str(msg.content)

                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))

            # Yeni kullanıcı mesajını ekle
            create_message(self.db, state["conversation_id"], "user", state["question"])
            messages.append(HumanMessage(content=state['question']))

            # LLM'den cevap al
            answer = await self.llm.ainvoke(messages)

            # Cevabı kaydet
            create_message(self.db, state["conversation_id"], "assistant", answer.content)
            update_conversation(self.db, state["conversation_id"])

            # State'e ekle
            messages.append(answer)

            return {"answer": str(answer.content), "messages": messages}
        except Exception as e:
            logger.error(f"Error in _get_answer: {e}")
            return {"answer": f"Error: {str(e)}", "messages": []}

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

    async def run_workflow(self, question: str, user_id: int, conversation_id: int = None) -> State:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        if not user_id:
            raise ValueError("User ID cannot be empty")

        # Yeni conversation oluştur
        if conversation_id is None:
            conversation = create_conversation(self.db, user_id)
            if not conversation:
                raise ValueError(f"User with ID {user_id} not found")
            conversation_id = conversation.id
            logger.info(f"Created new conversation: {conversation_id}")

        if self.app is None:
            self._compile_graph()

        logger.info(f"Running workflow (user: {user_id}, conversation: {conversation_id})")

        return await self.app.ainvoke(
            {
                "question": question,
                "context": [],
                "answer": "",
                "user_id": str(user_id),  # VectorStore için string
                "conversation_id": conversation_id
            },
            config={"configurable": {"thread_id": str(conversation_id)}}  # conversation_id kullan!
        )



import asyncio


async def main():
    from src.api.database.crud import create_user, get_user_by_email, get_conversations_by_user, get_messages_by_conversation

    rag = RAG()

    test_email = "test@example.com"
    user = get_user_by_email(rag.db, test_email)
    if not user:
        user = create_user(rag.db, "Test User", test_email, "test123")

    print(f"User ID: {user.id}")
    print("-" * 50)

    # ✅ SON CONVERSATION'I BUL
    existing_conversations = get_conversations_by_user(rag.db, user.id)
    conv_id = existing_conversations[0].id if existing_conversations else None

    if conv_id:
        print(f"📌 Mevcut conversation kullanılıyor: {conv_id}")
    else:
        print("📌 Yeni conversation oluşturulacak")

    # İLK SORU
    result1 = await rag.run_workflow(
        "Hi, I am Oğuz and I am 20 years old",
        user_id=user.id,
        conversation_id=conv_id  # ← SON CONVERSATION'I KULLAN
    )
    conv_id = result1["conversation_id"]
    print(f"Answer 1: {result1['answer']}\n")

    # ✅ VERİTABANINDAKİ MESAJLARI KONTROL ET
    messages = get_messages_by_conversation(rag.db, conv_id)
    print("📌 Veritabanındaki Mesajlar:")
    for msg in messages:
        print(f"  [{msg.role}]: {msg.content[:50]}...")
    print("-" * 50)

    # İKİNCİ SORU
    result2 = await rag.run_workflow(
        "What's my name and age?",
        user_id=user.id,
        conversation_id=conv_id  # ← AYNI CONVERSATION
    )
    print(f"Answer 2: {result2['answer']}")

    # ✅ GÜNCEL MESAJLARI KONTROL ET
    messages = get_messages_by_conversation(rag.db, conv_id)
    print("\n📌 Güncellenmiş Veritabanı Mesajları:")
    for msg in messages:
        print(f"  [{msg.role}]: {msg.content[:50]}...")




if __name__ == "__main__":
    asyncio.run(main())