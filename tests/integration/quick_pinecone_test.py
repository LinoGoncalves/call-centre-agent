"""
Quick Pinecone Test with Direct API Key
"""
import asyncio
from src.vector_db.pinecone_client import PineconeConfig, PineconeClient

async def quick_test():
    # Use your API key directly (just for testing)
    config = PineconeConfig(
        api_key="pcsk_4L1Em2_Ux2gVf26ThrhGYzt9BuhuvsFs1a5kUdo9s2bwn38YrJjSrsc15zTPWGhQHqQvpb",
        environment="us-west1-gcp",
        index_name="call-centre-tickets"
    )
    
    client = PineconeClient(config)
    print("🔄 Testing with your actual API key...")
    
    try:
        await client.initialize_index(create_if_not_exists=True)
        health = await client.health_check(force_check=True)
        stats = await client.get_index_stats()
        
        print(f"✅ SUCCESS! Health: {health}")
        print(f"✅ Index stats: {stats}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(quick_test())