from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Ultra-fast local model
model = OllamaLLM(
    model="qwen2.5:1.5b",        # FASTEST model for parsing/extraction
    temperature=0,               # consistent output (no creativity)
    options={
        "num_predict": 200       # restrict output length = faster
    }
)

template = (
    "Extract ONLY the information from this text: {dom_content}\n\n"
    "Extraction instructions:\n"
    "1. Extract ONLY the data that matches: {parse_description}\n"
    "2. Do NOT add explanations, commentary, or extra text\n"
    "3. If nothing matches, respond with an empty string ('')\n"
    "4. Output ONLY the extracted raw data\n"
)

prompt = ChatPromptTemplate.from_template(template)


# parse.py (important part)
def prase_with_ollama(dom_chunks, parse_description):
    chain = prompt | model
    parsed_results = []

    total = len(dom_chunks)

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            response = chain.invoke({
                "dom_content": chunk,
                "parse_description": parse_description
            })
            print(f"Parsed chunk {i}/{total}")

            # make sure you append the textual content (string)
            # If response is a string already, this is fine; if it's an object, convert appropriately:
            parsed_results.append(str(response))

        except Exception as e:
            print("\n--- ERROR OCCURRED ---")
            print(f"Chunk index: {i}")
            print(f"Error: {str(e)}")
            raise

    return "\n".join(parsed_results)

