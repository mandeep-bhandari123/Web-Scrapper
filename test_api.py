from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

print(f"API Key: {os.getenv('DEEPSEEK_API_KEY')[:10]}..." if os.getenv('DEEPSEEK_API_KEY') else "No API Key")
print(f"Base URL: {os.getenv('DEEPSEEK_BASE_URL')}")

try:
    model = ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        model="deepseek-chat",
    )
    
    response = model.invoke("Say hello")
    print(f"Success! Response: {response.content}")
except Exception as e:
    print(f"Error: {type(e).__name__}")
    print(f"Error message: {str(e)}")
