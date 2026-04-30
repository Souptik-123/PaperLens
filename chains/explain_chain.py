from langchain_openai import ChatOpenAI

def get_explain_chain(api_key: str, system_prompt: str):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key,
        temperature=0.2,
        max_tokens=8000,
    )

    def run(text: str):
        messages = [
            ("system", system_prompt),
            ("user", f"Here is the research paper text to analyze:\n\n{text[:60000]}")
        ]
        response = llm.invoke(messages)
        return response.content

    return run # step 4: parsing
