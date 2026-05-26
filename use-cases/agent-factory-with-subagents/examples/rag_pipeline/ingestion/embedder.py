"""
Document embedding generation for vector search.
"""

import os
import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json

from openai import RateLimitError, APIError
from dotenv import load_dotenv

from .chunker import DocumentChunk

# Import flexible providers
try:
    from ..utils.providers import get_embedding_client, get_embedding_model
except ImportError:
    # For direct execution or testing
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.providers import get_embedding_client, get_embedding_model

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize client with flexible provider
embedding_client = get_embedding_client()
EMBEDDING_MODEL = get_embedding_model()


class EmbeddingGenerator:
    """Generates embeddings for document chunks."""
    
    def __init__(
        self,
        model: str = EMBEDDING_MODEL,
        batch_size: int = 100,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize embedding generator.
        
        Args:
            model: OpenAI embedding model to use
            batch_size: Number of texts to process in parallel
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.model = model
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Model-specific configurations
        self.model_configs = {
            "text-embedding-3-small": {"dimensions": 1536, "max_tokens": 8191},
            "text-embedding-3-large": {"dimensions": 3072, "max_tokens": 8191},
            "text-embedding-ada-002": {"dimensions": 1536, "max_tokens": 8191}
        }
        
        if model not in self.model_configs:
            logger.warning(f"Unknown model {model}, using default config")
            self.config = {"dimensions": 1536, "max_tokens": 8191}
        else:
            self.config = self.model_configs[model]
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        """
        # Truncate text if too long
        if len(text) > self.config["max_tokens"] * 4:  # Rough token estimation
            text = text[:self.config["max_tokens"] * 4]
        
        for attempt in range(self.max_retries):
            try:
                response = await embedding_client.embeddings.create(
                    model=self.model,
                    input=text
                )
                
                return response.data[0].embedding
                
            except RateLimitError as e:
                if attempt == self.max_retries - 1:
                    raise
                
                # Exponential backoff for rate limits
                delay = self.retry_delay * (2 ** attempt)
                logger.warning(f"Rate limit hit, retrying in {delay}s")
                await asyncio.sleep(delay)
                
            except APIError as e:
                logger.error(f"OpenAI API error: {e}")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(self.retry_delay)
                
            except Exception as e:
                logger.error(f"Unexpected error generating embedding: {e}")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(self.retry_delay)
    
    async def generate_embeddings_batch(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.
        
        Args:
            texts: List of texts to embed
        
        Returns:
            List of embedding vectors
        """
        # Filter and truncate texts
        processed_texts = []
        for text in texts:
            if not text or not text.strip():
                processed_texts.append("")
                continue
                
            # Truncate if too long
            if len(text) > self.config["max_tokens"] * 4:
                text = text[:self.config["max_tokens"] * 4]
            
            processed_texts.append(text)
        
        for attempt in range(self.max_retries):
            try:
                response = await embedding_client.embeddings.create(
                    model=self.model,
                    input=processed_texts
                )
                
                return [data.embedding for data in response.data]
                
            except RateLimitError as e:
                if attempt == self.max_retries - 1:
                    raise
                
                delay = self.retry_delay * (2 ** attempt)
                logger.warning(f"Rate limit hit, retrying batch in {delay}s")
                await asyncio.sleep(delay)
                
            except APIError as e:
                logger.error(f"OpenAI API error in batch: {e}")
                if attempt == self.max_retries - 1:
                    # Fallback to individual processing
                    return await self._process_individually(processed_texts)
                await asyncio.sleep(self.retry_delay)
                
            except Exception as e:
                logger.error(f"Unexpected error in batch embedding: {e}")
                if attempt == self.max_retries - 1:
                    return await self._process_individually(processed_texts)
                await asyncio.sleep(self.retry_delay)
    
    async def _process_individually(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Process texts individually as fallback.
        
        Args:
            texts: List of texts to embed
        
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        for text in texts:
            try:
                if not text or not text.strip():
                    embeddings.append([0.0] * self.config["dimensions"])
                    continue
                
                embedding = await self.generate_embedding(text)
                embeddings.append(embedding)
                
                # Small delay to avoid overwhelming the API
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Failed to embed text: {e}")
                # Use zero vector as fallback
                embeddings.append([0.0] * self.config["dimensions"])
        
        return embeddings
    
    async def embed_chunks(
        self,
        chunks: List[DocumentChunk],
        progress_callback: Optional[callable] = None
    ) -> List[DocumentChunk]:
        """
        Generate embeddings for document chunks.
        
        Args:
            chunks: List of document chunks
            progress_callback: Optional callback for progress updates
        
        Returns:
            Chunks with embeddings added
        """
        if not chunks:
            return chunks
        
        logger.info(f"Generating embeddings for {len(chunks)} chunks")
        
        # Process chunks in batches
        embedded_chunks = []
        total_batches = (len(chunks) + self.batch_size - 1) // self.batch_size
        
        for i in range(0, len(chunks), self.batch_size):
            batch_chunks = chunks[i:i + self.batch_size]
            batch_texts = [chunk.content for chunk in batch_chunks]
            
            try:
                # Generate embeddings for this batch
                embeddings = await self.generate_embeddings_batch(batch_texts)
                
                # Add embeddings to chunks
                for chunk, embedding in zip(batch_chunks, embeddings):
                    # Create a new chunk with embedding
                    embedded_chunk = DocumentChunk(
                        content=chunk.content,
                        index=chunk.index,
                        start_char=chunk.start_char,
                        end_char=chunk.end_char,
                        metadata={
                            **chunk.metadata,
                            "embedding_model": self.model,
                            "embedding_generated_at": datetime.now().isoformat()
                        },
                        token_count=chunk.token_count
                    )
                    
                    # Add embedding as a separate attribute
                    embedded_chunk.embedding = embedding
                    embedded_chunks.append(embedded_chunk)
                
                # Progress update
                current_batch = (i // self.batch_size) + 1
                if progress_callback:
                    progress_callback(current_batch, total_batches)
                
                logger.info(f"Processed batch {current_batch}/{total_batches}")
                
            except Exception as e:
                logger.error(f"Failed to process batch {i//self.batch_size + 1}: {e}")
                
                # Add chunks without embeddings as fallback
                for chunk in batch_chunks:
                    chunk.metadata.update({
                        "embedding_error": str(e),
                        "embedding_generated_at": datetime.now().isoformat()
                    })
                    chunk.embedding = [0.0] * self.config["dimensions"]
                    embedded_chunks.append(chunk)
        
        logger.info(f"Generated embeddings for {len(embedded_chunks)} chunks")
        return embedded_chunks
    
    async def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Search query
        
        Returns:
            Query embedding
        """
        return await self.generate_embedding(query)
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings for this model."""
        return self.config["dimensions"]


# Cache for embeddings
class EmbeddingCache:
    """Simple in-memory cache for embeddings."""
    
    def __init__(self, max_size: int = 1000):
        """Initialize cache."""
        self.cache: Dict[str, List[float]] = {}
        self.access_times: Dict[str, datetime] = {}
        self.max_size = max_size
    
    def get(self, text: str) -> Optional[List[float]]:
        """Get embedding from cache."""
        text_hash = self._hash_text(text)
        if text_hash in self.cache:
            self.access_times[text_hash] = datetime.now()
            return self.cache[text_hash]
        return None
    
    def put(self, text: str, embedding: List[float]):
        """Store embedding in cache."""
        text_hash = self._hash_text(text)
        
        # Evict oldest entries if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[text_hash] = embedding
        self.access_times[text_hash] = datetime.now()
    
    def _hash_text(self, text: str) -> str:
        """Generate hash for text."""
        import hashlib
        return hashlib.md5(text.encode()).hexdigest()


# Factory function
def create_embedder(
    model: str = EMBEDDING_MODEL,
    use_cache: bool = True,
    **kwargs
) -> EmbeddingGenerator:
    """
    Create embedding generator with optional caching.
    
    Args:
        model: Embedding model to use
        use_cache: Whether to use caching
        **kwargs: Additional arguments for EmbeddingGenerator
    
    Returns:
        EmbeddingGenerator instance
    """
    embedder = EmbeddingGenerator(model=model, **kwargs)
    
    if use_cache:
        # Add caching capability
        cache = EmbeddingCache()
        original_generate = embedder.generate_embedding
        
        async def cached_generate(text: str) -> List[float]:
            cached = cache.get(text)
            if cached is not None:
                return cached
            
            embedding = await original_generate(text)
            cache.put(text, embedding)
            return embedding
        
        embedder.generate_embedding = cached_generate
    
    return embedder


# Example usage
async def main():
    """Example usage of the embedder."""
    from .chunker import ChunkingConfig, create_chunker
    
    # Create chunker and embedder
    config = ChunkingConfig(chunk_size=200, use_semantic_splitting=False)
    chunker = create_chunker(config)
    embedder = create_embedder()
    
    sample_text = """
    Google's AI initiatives include advanced language models, computer vision,
    and machine learning research. The company has invested heavily in
    transformer architectures and neural network optimization.
    
    Microsoft's partnership with OpenAI has led to integration of GPT models
    into various products and services, making AI accessible to enterprise
    customers through Azure cloud services.
    """
    
    # Chunk the document
    chunks = chunker.chunk_document(
        content=sample_text,
        title="AI Initiatives",
        source="example.md"
    )
    
    print(f"Created {len(chunks)} chunks")
    
    # Generate embeddings
    def progress_callback(current, total):
        print(f"Processing batch {current}/{total}")
    
    embedded_chunks = await embedder.embed_chunks(chunks, progress_callback)
    
    for i, chunk in enumerate(embedded_chunks):
        print(f"Chunk {i}: {len(chunk.content)} chars, embedding dim: {len(chunk.embedding)}")
    
    # Test query embedding
    query_embedding = await embedder.embed_query("Google AI research")
    print(f"Query embedding dimension: {len(query_embedding)}")


if __name__ == "__main__":
    asyncio.run(main())