# save as simple_test.py
try:
    from pinecone import Pinecone
    print("Successfully imported Pinecone")
except Exception as e:
    print(f"Error importing: {e}")

try:
    from embedding.pinecone_client import init_pinecone
    print("Successfully imported init_pinecone")
except Exception as e:
    print(f"Error importing init_pinecone: {e}")