from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document



def chunk_transcript(
    transcript_text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[Document]:
    """
    Clean transcript and split into LangChain Documents
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return splitter.create_documents([transcript_text])
