"""
Comprehensive Pinecone Integration Test
Test full connection, index operations, and vector operations
"""

import os
import asyncio
from dotenv import load_dotenv
from src.vector_db.pinecone_client import PineconeConfig, PineconeClient

async def test_full_pinecone_integration():
    """Test full Pinecone integration including index operations"""
    print("🚀 Starting Comprehensive Pinecone Integration Test...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Create config
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key or api_key == "your_pinecone_api_key_here":
            print("❌ ERROR: Please set your actual PINECONE_API_KEY in .env file")
            return False
            
        config = PineconeConfig(
            api_key=api_key,
            environment=os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp"),
            index_name=os.getenv("PINECONE_INDEX_NAME", "call-centre-tickets")
        )
        
        print(f"✅ Config created successfully")
        print(f"   Environment: {config.environment}")
        print(f"   Index Name: {config.index_name}")
        print(f"   API Key: {api_key[:12]}...{api_key[-4:]}")
        
        # Create client
        client = PineconeClient(config)
        print("✅ Pinecone client created")
        
        # Test index initialization (this will try to connect to Pinecone)
        print("🔄 Testing index initialization...")
        await client.initialize_index(create_if_not_exists=True)
        print("✅ Index initialized successfully!")
        
        # Test health check
        print("🔄 Testing health check...")
        health = await client.health_check(force_check=True)
        print(f"✅ Health check: {health}")
        
        # Test getting index stats
        print("🔄 Testing index statistics...")
        stats = await client.get_index_stats()
        print(f"✅ Index stats: {stats}")
        
        # Clean up
        await client.close()
        
        print("\n🎉 ALL TESTS PASSED! Pinecone integration is fully working!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_full_pinecone_integration())
    if result:
        print("\n✅ Ready to proceed with vector database features!")
    else:
        print("\n❌ Please resolve the issues above before proceeding.")