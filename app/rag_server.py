import os
import getpass
from dotenv import load_dotenv
from ollama import Client
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from prompt_file import PROMPT  # keep your witty Amul prompt template

# 1. Load environment variables
load_dotenv()

if not os.getenv("PINECONE_API_KEY"):
    os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter your Pinecone API key: ")

pinecone_api_key = os.environ["PINECONE_API_KEY"]

# 2. Initialize Pinecone client + index
pc = Pinecone(api_key=pinecone_api_key)
index_name = "amul-docs"   # must already exist
index = pc.Index(index_name)

# 3. Embeddings model

embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. LangChain wrapper around Pinecone
vectorstore = PineconeVectorStore(index=index, embedding=embedding)

# 5. Ollama client
ollama_client = Client()

import re

def clean_context(text: str) -> str:
    """Remove only unnecessary markdown formatting while keeping contact details intact."""
    # Remove bold/italic symbols but preserve #, -, +, etc.
    text = re.sub(r"\*\*|\*", "", text)
    # Optionally remove only Table of Contents heading
    text = re.sub(r"^Table of Contents.*?$", "", text, flags=re.MULTILINE)
    return text.strip()



def ask_amul(question: str):
    """Retrieve context from Pinecone and query Ollama with AmulGPT prompt."""
    try:
        # Retrieve docs from Pinecone
        docs = vectorstore.similarity_search(question, k=5)
        raw_context = "\n\n".join([doc.page_content for doc in docs])
        context = clean_context(raw_context)

        # Format prompt with both question + context
        full_prompt = PROMPT.format(question=question, context=context)

        # Send to Ollama
        result = ollama_client.generate(model="llama3.2:1b", prompt=full_prompt)
        return result["response"]

    except Exception as e:
        return f"⚠️ Error: {e}"

def main():
    print("🧈 Welcome to AmulGPT (RAG + Ollama + Pinecone)!")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("❓ Ask AmulGPT: ").strip()

        if question.lower() == "exit":
            print("🙏 Thanks for chatting! Have a buttery day!")
            break

        if not question:
            print("⚠️ Please type a question.")
            continue

        print("\n🔄 Thinking...\n")
        answer = ask_amul(question)

        print("🧈 AmulGPT says:")
        print(answer)
        print("-" * 50)

if __name__ == "__main__":
    main()
