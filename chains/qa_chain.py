from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


def build_qa_chain(vector_store, api_key: str, qa_prompt_template: str):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key,
        temperature=0.3,
        max_tokens=2000,
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=qa_prompt_template,
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 10},
        ),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False,
    )