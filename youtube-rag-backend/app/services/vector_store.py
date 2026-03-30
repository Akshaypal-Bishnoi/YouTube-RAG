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
    index_file = os.path.join(index_path, "index.pkl")

    print(f"[INFO] Video ID: {video_id}")
    print(f"[INFO] Index path: {index_path}")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # ✅ Try loading existing index
    try:
        if os.path.exists(index_file):
            print("[INFO] Loading existing FAISS index...")
            return FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True
            )
    except Exception as e:
        print(f"[WARNING] Failed to load index. Recreating... Error: {e}")

    # 🔥 Create new index if not found or failed
    print("[INFO] Creating new FAISS index...")

    # Fetch transcript
    transcript = fetch_transcript(video_id)

    if not transcript:
        raise ValueError("Transcript not found or empty.")

    # Chunk transcript
    documents = chunk_transcript(transcript)

    if not documents:
        raise ValueError("No documents created from transcript.")

    # Create FAISS index
    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    # Save index locally
    os.makedirs(index_path, exist_ok=True)
    vector_store.save_local(index_path)

    print("[INFO] FAISS index created and saved successfully.")

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






