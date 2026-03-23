import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from config import OPENAI_API_KEY, CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL

client = None
collection = None

def init_rag():
    global client, collection
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing.")
    client = OpenAI(api_key=OPENAI_API_KEY)

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    openai_ef     = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name=EMBEDDING_MODEL,
    )

    if COLLECTION_NAME in [c.name for c in chroma_client.list_collections()]:
        collection = chroma_client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=openai_ef
        )
    else:
        raise RuntimeError(f"ChromaDB collection '{COLLECTION_NAME}' not found.")