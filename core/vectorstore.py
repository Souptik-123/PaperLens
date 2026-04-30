from langchain_community.vectorstores import FAISS
from config import TOP_K
def build_vectorstore(chunks, embeddings):
    return FAISS.from_documents(chunks, embeddings)

def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": TOP_K})