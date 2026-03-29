from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from app.services.vector_store import get_or_create_vector_store


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(video_id: str):
    """
    Build RAG chain for a specific video
    """
    vector_store = get_or_create_vector_store(video_id)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    prompt = PromptTemplate(
        template="""
You are a helpful assistant.
Answer ONLY using the provided transcript context.
and formate answer with pragraph and spaces properly.
If the answer is not present in the transcript, say:
"I cannot find this information in the video."

Context:
{context}

Question: {question}
""",
        input_variables=["context", "question"]
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = (
        RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        })
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
