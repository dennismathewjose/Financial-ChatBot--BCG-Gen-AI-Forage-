def test_pinecone_import():
    import sys
    print("Python Path in pytest:")
    for p in sys.path:
        print(f"  {p}")
    
    import pinecone
    print(f"Pinecone path: {pinecone.__file__}")
    print(f"Pinecone version: {getattr(pinecone, '__version__', 'unknown')}")
    
    from pinecone import Pinecone
    print("Successfully imported Pinecone class")
    
    assert True
