#!/usr/bin/env python3
"""
🔓 ChromaDB Vector Database Integration
Lightweight, embedded vector database for local development and demos

Features:
1. Embedded ChromaDB with persistent storage
2. Automatic collection management for telco tickets
3. Vector similarity search for ticket routing
4. Zero-cost alternative to Pinecone
5. Perfect for demos and development

Author: GitHub Copilot Assistant
Date: October 9, 2025
Purpose: Open source vector database demonstration
"""

import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import json

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logging.warning("ChromaDB not available. Install with: pip install chromadb")

logger = logging.getLogger(__name__)

@dataclass
class VectorSearchResult:
    """Result from vector similarity search"""
    ticket_id: str
    similarity_score: float
    original_ticket: str
    department: str
    confidence: float
    metadata: Dict[str, Any]

class ChromaVectorDB:
    """
    ChromaDB Vector Database client for telco ticket similarity search
    
    Provides local, embedded vector storage with automatic persistence
    """
    
    def __init__(self, 
                 collection_name: str = "telco_tickets",
                 persist_directory: str = "./chroma_db",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize ChromaDB client
        
        Args:
            collection_name: Name of the collection for storing vectors
            persist_directory: Directory for persistent storage
            embedding_model: Sentence transformer model for embeddings
        """
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.embedding_model = embedding_model
        self.available = CHROMADB_AVAILABLE
        
        if not self.available:
            logger.error("ChromaDB not available. Please install: pip install chromadb")
            return
            
        try:
            # Create persist directory if it doesn't exist
            self.persist_directory.mkdir(exist_ok=True, parents=True)
            
            # Initialize ChromaDB client with persistence
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(collection_name)
                logger.info(f"✅ Connected to existing ChromaDB collection: {collection_name}")
            except Exception:
                self.collection = self.client.create_collection(
                    name=collection_name,
                    metadata={"description": "Telco customer service tickets for similarity search"}
                )
                logger.info(f"✅ Created new ChromaDB collection: {collection_name}")
                
            # Initialize with sample data if collection is empty
            if self.collection.count() == 0:
                self._initialize_sample_data()
                
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.available = False
    
    def _initialize_sample_data(self):
        """Initialize collection with sample telco tickets"""
        sample_tickets = [
            {
                "id": "ticket_001",
                "text": "My internet connection is very slow and I can't stream videos",
                "department": "technical_support_l1",
                "confidence": 0.95,
                "category": "performance_issue"
            },
            {
                "id": "ticket_002", 
                "text": "I can't connect to WiFi, it keeps disconnecting every few minutes",
                "department": "technical_support_l1",
                "confidence": 0.90,
                "category": "connectivity_issue"
            },
            {
                "id": "ticket_003",
                "text": "My bill is higher than expected, need explanation of charges",
                "department": "billing_and_payments",
                "confidence": 0.98,
                "category": "billing_inquiry"
            },
            {
                "id": "ticket_004",
                "text": "Network outage in my area, when will it be restored?",
                "department": "network_outages",
                "confidence": 0.99,
                "category": "outage_report"
            },
            {
                "id": "ticket_005",
                "text": "Want to upgrade my plan to higher speed internet",
                "department": "sales_and_upgrades",
                "confidence": 0.92,
                "category": "upgrade_request"
            },
            {
                "id": "ticket_006",
                "text": "Account locked, cannot access customer portal to pay bill",
                "department": "account_management",
                "confidence": 0.96,
                "category": "account_access"
            },
            {
                "id": "ticket_007",
                "text": "Poor customer service experience, want to file a complaint",
                "department": "complaints_and_escalations",
                "confidence": 0.94,
                "category": "complaint"
            },
            {
                "id": "ticket_008",
                "text": "Router not working, no lights on device, need replacement",
                "department": "technical_support_l2",
                "confidence": 0.88,
                "category": "hardware_failure"
            }
        ]
        
        # Add sample tickets to collection
        documents = [ticket["text"] for ticket in sample_tickets]
        metadatas = [
            {
                "department": ticket["department"],
                "confidence": ticket["confidence"],
                "category": ticket["category"]
            }
            for ticket in sample_tickets
        ]
        ids = [ticket["id"] for ticket in sample_tickets]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"✅ Initialized ChromaDB with {len(sample_tickets)} sample tickets")
    
    def search_similar_tickets(self, 
                              query_text: str, 
                              top_k: int = 5,
                              similarity_threshold: float = 0.7) -> List[VectorSearchResult]:
        """
        Search for similar tickets using vector similarity
        
        Args:
            query_text: Customer ticket text to search for
            top_k: Number of similar tickets to return
            similarity_threshold: Minimum similarity score threshold
            
        Returns:
            List of VectorSearchResult objects
        """
        if not self.available:
            logger.warning("ChromaDB not available, returning empty results")
            return []
        
        start_time = time.time()
        
        try:
            # Query the collection for similar documents
            results = self.collection.query(
                query_texts=[query_text],
                n_results=top_k,
                include=['documents', 'metadatas', 'distances']
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            if not results['documents'] or not results['documents'][0]:
                logger.info(f"No similar tickets found for: {query_text[:50]}...")
                return []
            
            # Convert results to VectorSearchResult objects
            search_results = []
            documents = results['documents'][0]
            metadatas = results['metadatas'][0] 
            distances = results['distances'][0]
            ids = results['ids'][0]
            
            for i, (doc, metadata, distance, ticket_id) in enumerate(zip(documents, metadatas, distances, ids)):
                # Convert distance to similarity score (ChromaDB uses cosine distance)
                similarity_score = 1.0 - distance
                
                if similarity_score >= similarity_threshold:
                    result = VectorSearchResult(
                        ticket_id=ticket_id,
                        similarity_score=similarity_score,
                        original_ticket=doc,
                        department=metadata.get('department', 'unknown'),
                        confidence=metadata.get('confidence', 0.5),
                        metadata={
                            **metadata,
                            'search_rank': i + 1,
                            'processing_time_ms': processing_time,
                            'query_text': query_text
                        }
                    )
                    search_results.append(result)
            
            logger.info(f"ChromaDB search completed: {len(search_results)} results in {processing_time:.1f}ms")
            return search_results
            
        except Exception as e:
            logger.error(f"ChromaDB search failed: {e}")
            return []
    
    def add_ticket(self, 
                   ticket_id: str,
                   ticket_text: str, 
                   department: str,
                   confidence: float = 0.9,
                   metadata: Optional[Dict] = None) -> bool:
        """
        Add a new ticket to the vector database
        
        Args:
            ticket_id: Unique identifier for the ticket
            ticket_text: Customer service ticket text
            department: Routed department
            confidence: Classification confidence
            metadata: Additional metadata
            
        Returns:
            True if successfully added, False otherwise
        """
        if not self.available:
            return False
        
        try:
            ticket_metadata = {
                "department": department,
                "confidence": confidence,
                "added_timestamp": time.time()
            }
            
            if metadata:
                ticket_metadata.update(metadata)
            
            self.collection.add(
                documents=[ticket_text],
                metadatas=[ticket_metadata],
                ids=[ticket_id]
            )
            
            logger.info(f"✅ Added ticket {ticket_id} to ChromaDB")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add ticket to ChromaDB: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the current collection"""
        if not self.available:
            return {"available": False, "error": "ChromaDB not available"}
        
        try:
            count = self.collection.count()
            
            # Get sample of documents to analyze departments
            if count > 0:
                sample_results = self.collection.get(
                    include=['metadatas'],
                    limit=min(count, 100)
                )
                
                departments = [m.get('department', 'unknown') for m in sample_results['metadatas']]
                dept_counts = {}
                for dept in departments:
                    dept_counts[dept] = dept_counts.get(dept, 0) + 1
                
                return {
                    "available": True,
                    "total_tickets": count,
                    "collection_name": self.collection_name,
                    "persist_directory": str(self.persist_directory),
                    "department_distribution": dept_counts,
                    "embedding_model": self.embedding_model,
                    "cost_per_query": 0.0,  # ChromaDB is free!
                    "storage_cost": 0.0     # Local storage only
                }
            else:
                return {
                    "available": True,
                    "total_tickets": 0,
                    "collection_name": self.collection_name,
                    "status": "Empty collection"
                }
                
        except Exception as e:
            logger.error(f"Failed to get ChromaDB stats: {e}")
            return {"available": False, "error": str(e)}

def chromadb_installation_guide():
    """Return installation instructions for ChromaDB"""
    return """
🔓 ChromaDB Setup Guide (Zero-Cost Vector Database)

1. Install ChromaDB:
   pip install chromadb

2. Optional - Install sentence-transformers for better embeddings:
   pip install sentence-transformers

3. That's it! ChromaDB will automatically:
   - Create local storage directory (./chroma_db/)
   - Initialize with sample telco tickets
   - Provide persistent vector storage
   - Enable similarity search

💡 Benefits:
- ✅ Completely free (no API costs)
- ✅ Local data storage (privacy)
- ✅ No internet required for operation
- ✅ Perfect for demos and development
- ✅ Automatic persistence across restarts

📊 Performance:
- ~10-50ms query time for small datasets
- Suitable for up to 100K documents
- Embedded operation (no server required)
- Minimal resource usage
"""

if __name__ == "__main__":
    # Demo ChromaDB integration
    print("🔓 Testing ChromaDB Vector Database Integration...")
    
    if not CHROMADB_AVAILABLE:
        print("\n" + chromadb_installation_guide())
        exit(1)
    
    # Initialize ChromaDB
    vector_db = ChromaVectorDB()
    
    if not vector_db.available:
        print("❌ ChromaDB initialization failed")
        exit(1)
    
    # Test similarity search
    test_queries = [
        "Internet connection problems and slow speeds",
        "Need help with my monthly bill charges", 
        "WiFi keeps dropping connection constantly",
        "Want to upgrade to faster internet plan"
    ]
    
    print(f"\n📊 ChromaDB Collection Stats:")
    stats = vector_db.get_collection_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n🔍 Testing Similarity Search:")
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = vector_db.search_similar_tickets(query, top_k=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. Similarity: {result.similarity_score:.2f} | Dept: {result.department}")
                print(f"     Ticket: {result.original_ticket[:60]}...")
        else:
            print("  No similar tickets found")
    
    print(f"\n✅ ChromaDB integration test complete!")
    print(f"💰 Cost: $0 (completely free!)")