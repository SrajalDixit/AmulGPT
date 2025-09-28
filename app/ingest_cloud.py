import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Load environment variables
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")  # e.g., "us-east-1"

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

# Create index if it doesn't exist
index_name = "amul-docs"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # all-MiniLM-L6-v2 embedding size
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=pinecone_env)
    )

# Load and split documents
loader = TextLoader("../Data/Amul_Doc.md")
docs = loader.load()
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(docs)

# Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = [model.encode(d.page_content).tolist() for d in docs]

# Prepare data for upsert
vectors = [(str(i), emb, {"text": d.page_content}) for i, (emb, d) in enumerate(zip(embeddings, docs))]

# Upsert into Pinecone
index = pc.Index(index_name)
index.upsert(vectors=vectors)

print("✅ Data ingested into Pinecone!")
