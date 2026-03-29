
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.services.chunker import chunk_transcript
from app.services.transcript import fetch_transcript


INDEX_DIR = "indexes"


def get_or_create_vector_store(video_id: str) -> FAISS:
    """
    Load FAISS index from disk if exists,
    otherwise create it from transcript and save.
    """
    index_path = os.path.join(INDEX_DIR, video_id)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # ✅ Load if exists
    if os.path.exists(index_path):
        return FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    # ❌ Else create
    transcript = fetch_transcript(video_id)
    documents = chunk_transcript(transcript)

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    os.makedirs(index_path, exist_ok=True)
    vector_store.save_local(index_path)

    return vector_store














# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS

# from app.services.chunker import chunk_transcript
# from app.services.transcript import fetch_transcript

# # In-memory cache (clears automatically on server restart)
# _VECTOR_STORE_CACHE: dict[str, FAISS] = {}


# def get_or_create_vector_store(video_id: str) -> FAISS:
#     """
#     Create FAISS index in memory only.
#     Index is cleared automatically when server restarts.
#     """

#     # ✅ Return from RAM if already created
#     if video_id in _VECTOR_STORE_CACHE:
#         return _VECTOR_STORE_CACHE[video_id]

#     embeddings = OpenAIEmbeddings(
#         model="text-embedding-3-small"
#     )

#     # Fetch transcript
#     transcript = fetch_transcript(video_id)

#     # Chunk transcript
#     documents = chunk_transcript(transcript)

#     # Create FAISS index (RAM only)
#     vector_store = FAISS.from_documents(
#         documents,
#         embeddings
#     )

#     # Cache in memory
#     _VECTOR_STORE_CACHE[video_id] = vector_store

#     return vector_store






