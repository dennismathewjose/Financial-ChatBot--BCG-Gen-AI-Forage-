import os
from dotenv import load_dotenv
# Import explicitly from the new package to ensure we're using the correct one
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "financial-chatbot")
DIMENSION = 768  # adjust if your embedding dimension differs

def init_pinecone():
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Check if index exists, create if it doesn't
        existing_indexes = pc.list_indexes().names()
        if INDEX_NAME not in existing_indexes:
            print(f"Creating index: {INDEX_NAME}")
            pc.create_index(
                name=INDEX_NAME,
                dimension=DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-west-2")
            )
        
        index = pc.Index(INDEX_NAME)
        print(f"Pinecone index initialized: {index.describe_index_stats()}")
        return index
    except Exception as e:
        print(f"Error initializing Pinecone: {str(e)}")
        raise