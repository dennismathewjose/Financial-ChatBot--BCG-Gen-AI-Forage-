import sys
print("Python Path:")
for p in sys.path:
    print(f"  {p}")
print("\nTrying imports:")
try:
    import pinecone
    print(f"Successfully imported pinecone module")
    print(f"Pinecone path: {pinecone.__file__}")
    print(f"Pinecone version: {pinecone.__version__ if hasattr(pinecone, '__version__') else 'unknown'}")
except Exception as e:
    print(f"Error importing pinecone: {e}")

try:
    from pinecone import Pinecone
    print("Successfully imported Pinecone class")
except Exception as e:
    print(f"Error importing Pinecone class: {e}")
