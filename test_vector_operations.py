"""
Comprehensive Vector Operations Test
Test all vector database operations with realistic call centre data
"""

import asyncio
from datetime import datetime, UTC
from typing import List
from dotenv import load_dotenv

from src.vector_db.pinecone_client import PineconeClient

# Load environment variables
load_dotenv()

# Sample call centre ticket data for testing
SAMPLE_TICKETS = [
    {
        "id": "TICKET-001",
        "text": "My internet connection keeps dropping every few minutes. Very frustrating!",
        "department": "technical",
        "urgency": "high",
        "sentiment": "negative"
    },
    {
        "id": "TICKET-002", 
        "text": "I received duplicate charges on my monthly bill. Please help resolve this.",
        "department": "billing",
        "urgency": "medium",
        "sentiment": "neutral"
    },
    {
        "id": "TICKET-003",
        "text": "Thank you for the excellent customer service. Issue resolved quickly!",
        "department": "customer_service",
        "urgency": "low",
        "sentiment": "positive"
    },
    {
        "id": "TICKET-004",
        "text": "Cannot access my account online. Password reset not working.",
        "department": "technical",
        "urgency": "medium",
        "sentiment": "frustrated"
    },
    {
        "id": "TICKET-005",
        "text": "Billing inquiry about international roaming charges from last month.",
        "department": "billing",
        "urgency": "low",
        "sentiment": "neutral"
    }
]

def generate_mock_embedding(text: str, dimension: int = 1536) -> List[float]:
    """Generate a mock embedding based on text content"""
    import hashlib
    import random
    import math
    
    # Create a seed from the text
    seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    # Generate random embedding
    embedding = [random.gauss(0, 1) for _ in range(dimension)]
    
    # Normalize to unit vector (common for embeddings)
    norm = math.sqrt(sum(x * x for x in embedding))
    if norm > 0:
        embedding = [x / norm for x in embedding]
        
    return embedding

async def test_vector_upload_operations():
    """Test uploading vectors to Pinecone"""
    print("🔄 Testing Vector Upload Operations...")
    
    try:
        # Create client
        client = PineconeClient()
        await client.initialize_index(create_if_not_exists=True)
        
        # Prepare vectors for upload
        vectors_to_upload = []
        
        for ticket in SAMPLE_TICKETS:
            # Generate mock embedding
            embedding = generate_mock_embedding(ticket["text"])
            
            # Create metadata
            metadata = {
                "ticket_id": ticket["id"],
                "department": ticket["department"],
                "urgency": ticket["urgency"],
                "sentiment": ticket["sentiment"],
                "text": ticket["text"][:500],  # Truncate for metadata
                "created_at": datetime.now(UTC).isoformat(),
                "resolved": False
            }
            
            vectors_to_upload.append((ticket["id"], embedding, metadata))
        
        print(f"   Uploading {len(vectors_to_upload)} vectors...")
        
        # Upload vectors
        result = await client.upsert_vectors(vectors_to_upload)
        
        print(f"   ✅ Upload result: {result}")
        
        # Verify upload by getting stats
        stats = await client.get_index_stats()
        print(f"   ✅ Index now contains {stats['total_vector_count']} vectors")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Upload failed: {e}")
        return False

async def test_vector_similarity_search():
    """Test similarity search functionality"""
    print("🔄 Testing Vector Similarity Search...")
    
    try:
        client = PineconeClient()
        await client.initialize_index()
        
        # Create a query vector for billing-related issues
        query_text = "I have a problem with my monthly charges and billing"
        query_vector = generate_mock_embedding(query_text)
        
        print(f"   Searching for: '{query_text}'")
        
        # Perform similarity search
        results = await client.query_vectors(
            query_vector=query_vector,
            top_k=3,
            include_metadata=True,
            filter_metadata=None  # No filtering for now
        )
        
        matches = getattr(results, 'matches', results.get('matches', []))
        print(f"   ✅ Found {len(matches)} similar tickets:")
        
        for i, match in enumerate(matches[:3], 1):
            score = match.score
            metadata = match.metadata or {}
            ticket_text = metadata.get("text", "No text available")[:100]
            department = metadata.get("department", "unknown")
            
            print(f"      {i}. Score: {score:.3f} | Dept: {department}")
            print(f"         Text: {ticket_text}...")
        
        # Test with department filtering
        print("   🔄 Testing filtered search (billing department only)...")
        
        billing_results = await client.query_vectors(
            query_vector=query_vector,
            top_k=5,
            include_metadata=True,
            filter_metadata={"department": "billing"}
        )
        
        billing_matches = getattr(billing_results, 'matches', billing_results.get('matches', []))
        print(f"   ✅ Billing-only results: {len(billing_matches)} matches")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Search failed: {e}")
        return False

async def test_vector_deletion_operations():
    """Test vector deletion functionality"""
    print("🔄 Testing Vector Deletion Operations...")
    
    try:
        client = PineconeClient()
        await client.initialize_index()
        
        # Get stats before deletion
        stats_before = await client.get_index_stats()
        print(f"   Vectors before deletion: {stats_before['total_vector_count']}")
        
        # Delete specific tickets
        tickets_to_delete = ["TICKET-004", "TICKET-005"]
        
        print(f"   Deleting tickets: {tickets_to_delete}")
        
        delete_result = await client.delete_vectors(tickets_to_delete)
        print(f"   ✅ Delete result: {delete_result}")
        
        # Wait a moment for deletion to propagate
        await asyncio.sleep(2)
        
        # Get stats after deletion
        stats_after = await client.get_index_stats()
        print(f"   Vectors after deletion: {stats_after['total_vector_count']}")
        
        # Verify deletion worked
        deleted_count = stats_before['total_vector_count'] - stats_after['total_vector_count']
        print(f"   ✅ Successfully deleted {deleted_count} vectors")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Deletion failed: {e}")
        return False

async def test_end_to_end_workflow():
    """Test complete end-to-end workflow"""
    print("🔄 Testing End-to-End Vector Workflow...")
    
    try:
        client = PineconeClient()
        
        # 1. Initialize and check health
        await client.initialize_index()
        health = await client.health_check()
        print(f"   ✅ System health: {health}")
        
        # 2. Upload a new ticket
        new_ticket = {
            "id": "TICKET-TEST-001",
            "text": "My mobile data is not working properly in the city center area",
            "department": "technical",
            "urgency": "high", 
            "sentiment": "frustrated"
        }
        
        embedding = generate_mock_embedding(new_ticket["text"])
        metadata = {
            "ticket_id": new_ticket["id"],
            "department": new_ticket["department"],
            "urgency": new_ticket["urgency"],
            "sentiment": new_ticket["sentiment"],
            "text": new_ticket["text"],
            "created_at": datetime.now(UTC).isoformat(),
            "resolved": False
        }
        
        print(f"   📤 Uploading new ticket: {new_ticket['id']}")
        await client.upsert_vectors([(new_ticket["id"], embedding, metadata)])
        
        # 3. Search for similar tickets
        print("   🔍 Finding similar tickets...")
        search_results = await client.query_vectors(
            query_vector=embedding,
            top_k=3,
            include_metadata=True
        )
        
        search_matches = getattr(search_results, 'matches', search_results.get('matches', []))
        print(f"   ✅ Found {len(search_matches)} similar tickets")
        
        # 4. Mark ticket as resolved (update metadata)
        resolved_metadata = metadata.copy()
        resolved_metadata["resolved"] = True
        resolved_metadata["resolved_at"] = datetime.now(UTC).isoformat()
        
        print("   ✅ Marking ticket as resolved...")
        await client.upsert_vectors([(new_ticket["id"], embedding, resolved_metadata)])
        
        # 5. Clean up test ticket
        print("   🧹 Cleaning up test data...")
        await client.delete_vectors([new_ticket["id"]])
        
        # 6. Final stats
        final_stats = await client.get_index_stats()
        print(f"   ✅ Final index stats: {final_stats}")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"   ❌ End-to-end test failed: {e}")
        return False

async def run_comprehensive_vector_tests():
    """Run all vector operation tests"""
    print("🚀 Starting Comprehensive Vector Operations Test Suite\n")
    
    test_results = {}
    
    # Test 1: Vector Upload
    test_results["upload"] = await test_vector_upload_operations()
    print()
    
    # Test 2: Similarity Search
    if test_results["upload"]:
        test_results["search"] = await test_vector_similarity_search()
        print()
    else:
        test_results["search"] = False
        print("⏭️  Skipping search tests (upload failed)")
    
    # Test 3: Vector Deletion
    if test_results["search"]:
        test_results["deletion"] = await test_vector_deletion_operations()
        print()
    else:
        test_results["deletion"] = False
        print("⏭️  Skipping deletion tests (search failed)")
    
    # Test 4: End-to-End Workflow
    test_results["e2e"] = await test_end_to_end_workflow()
    print()
    
    # Summary
    print("📊 TEST RESULTS SUMMARY:")
    print("=" * 40)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name.upper():15} {status}")
    
    print("=" * 40)
    print(f"   TOTAL: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Vector database is fully functional!")
        print("🚀 Ready to proceed with production features!")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed. Review errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_comprehensive_vector_tests())