from langchain_community.document_loaders import PyPDFLoader

def load_pdf(path):
    loader = PyPDFLoader(path)
    docs = loader.load()
    full_text = "\n\n".join(d.page_content for d in docs)
    return docs, full_text