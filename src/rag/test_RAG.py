from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


class TestRAG:
    def __init__(self):
        self.env_loaded = self.get_env()
        self.llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
        print("RAG initialized")


    def get_env(self):
        try:
            load_dotenv()
            print(".env file loaded")
            return True
        except:
            print("Error loading .env file")
            return False

    def test_llm(self):
        llm_response = self.llm.invoke(
            [
                {
                    "role": "user",
                    "content": "Hello, how are you?",
                }
            ]
        )
        return llm_response


test_rag = TestRAG()
print(test_rag.test_llm())