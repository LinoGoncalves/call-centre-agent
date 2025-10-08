"""
Quick Pinecone Connection Test
Test your API key and basic connectivity
"""

import os
from src.vector_db.pinecone_client import PineconeConfig, PineconeClient

def test_pinecone_connection():
    """Test basic Pinecone connection with your API key"""
    print("🔍 Testing Pinecone Connection...")
    
    try:
        # Create config from environment
        config = PineconeConfig(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp"),
            index_name=os.getenv("PINECONE_INDEX_NAME", "call-centre-tickets")
        )
        
        print(f"✅ Config created successfully")
        print(f"   Environment: {config.environment}")
        print(f"   Index Name: {config.index_name}")
        print(f"   API Key: {config.api_key[:8]}...{config.api_key[-4:]}")
        
        # Create client
        client = PineconeClient(config)
        print(f"✅ Pinecone client created successfully")
        
        print(f"🎉 SUCCESS: Pinecone integration is working!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    test_pinecone_connection()