"""
Test Pinecone with Different Regions
"""
import asyncio
from src.vector_db.pinecone_client import PineconeConfig, PineconeClient

async def test_regions():
    # Common regions to try
    regions_to_try = [
        {"cloud": "aws", "region": "us-east-1", "environment": "us-east-1-aws"},
        {"cloud": "gcp", "region": "us-central1", "environment": "gcp-starter"},
        {"cloud": "aws", "region": "us-west-2", "environment": "us-west-2-aws"},
    ]
    
    api_key = "pcsk_4L1Em2_Ux2gVf26ThrhGYzt9BuhuvsFs1a5kUdo9s2bwn38YrJjSrsc15zTPWGhQHqQvpb"
    
    for region_config in regions_to_try:
        print(f"🔄 Testing {region_config['cloud']}/{region_config['region']}...")
        
        try:
            config = PineconeConfig(
                api_key=api_key,
                environment=region_config["environment"],
                index_name="call-centre-tickets",
                cloud=region_config["cloud"],
                region=region_config["region"]
            )
            
            client = PineconeClient(config)
            await client.initialize_index(create_if_not_exists=True)
            
            print(f"✅ SUCCESS with {region_config['cloud']}/{region_config['region']}!")
            
            # Test basic operations
            stats = await client.get_index_stats()
            print(f"   Index stats: {stats}")
            
            await client.close()
            return region_config
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)[:100]}...")
            continue
    
    print("❌ No regions worked. Let's check what's available for your account.")
    return None

if __name__ == "__main__":
    result = asyncio.run(test_regions())
    if result:
        print(f"\n🎉 SUCCESS! Use this configuration:")
        print(f"   PINECONE_ENVIRONMENT={result['environment']}")
        print(f"   Cloud: {result['cloud']}")
        print(f"   Region: {result['region']}")
    else:
        print("\n🔍 Let's check what regions are available for your account...")