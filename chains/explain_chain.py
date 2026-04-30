from langchain_openai import ChatOpenAI
from config import OPENAI_MODEL, TEMPERATURE
def get_explain_chain(api_key: str, system_prompt: str):
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=api_key,
        temperature=0.2,
        max_completion_tokens=16000,  # Increased from 8000 — large papers with SVG diagrams
    )                      # and equations easily exceed 8k tokens of output.

    def run(text: str) -> str:
        # Try with full input first; if the response looks truncated
        # (unterminated JSON), retry with progressively shorter input
        # so the model has more of its output budget for the JSON payload.
        content = ""
        for char_limit in [60000, 40000, 25000]:
            messages = [
                ("system", system_prompt),
                ("user", f"Here is the research paper text to analyze:\n\n{text[:char_limit]}")
            ]
            response = llm.invoke(messages)
            content = response.content.strip()

            # Detect truncation: valid JSON must end with '}'
            # If the last non-whitespace char isn't '}', the output was cut off.
            if content and content[-1] == "}":
                return content

            # Response was truncated — shrink input and retry
            # (shorter input → fewer prompt tokens → more room for output)

        # Return whatever we got on the final attempt and let the
        # caller's JSON repair logic handle it.
        return content

    return run