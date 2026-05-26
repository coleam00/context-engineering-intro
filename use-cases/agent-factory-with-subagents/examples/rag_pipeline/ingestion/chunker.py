"""
Semantic chunking implementation for intelligent document splitting.
"""

import os
import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import asyncio

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Import flexible providers
try:
    from ..utils.providers import get_embedding_client, get_ingestion_model
except ImportError:
    # For direct execution or testing
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.providers import get_embedding_client, get_ingestion_model

# Initialize clients with flexible providers
embedding_client = get_embedding_client()
ingestion_model = get_ingestion_model()


@dataclass
class ChunkingConfig:
    """Configuration for chunking."""
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_chunk_size: int = 2000
    min_chunk_size: int = 100
    use_semantic_splitting: bool = True
    preserve_structure: bool = True
    
    def __post_init__(self):
        """Validate configuration."""
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("Chunk overlap must be less than chunk size")
        if self.min_chunk_size <= 0:
            raise ValueError("Minimum chunk size must be positive")


@dataclass
class DocumentChunk:
    """Represents a document chunk."""
    content: str
    index: int
    start_char: int
    end_char: int
    metadata: Dict[str, Any]
    token_count: Optional[int] = None
    
    def __post_init__(self):
        """Calculate token count if not provided."""
        if self.token_count is None:
            # Rough estimation: ~4 characters per token
            self.token_count = len(self.content) // 4


class SemanticChunker:
    """Semantic document chunker using LLM for intelligent splitting."""
    
    def __init__(self, config: ChunkingConfig):
        """
        Initialize chunker.
        
        Args:
            config: Chunking configuration
        """
        self.config = config
        self.client = embedding_client
        self.model = ingestion_model
    
    async def chunk_document(
        self,
        content: str,
        title: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[DocumentChunk]:
        """
        Chunk a document into semantically coherent pieces.
        
        Args:
            content: Document content
            title: Document title
            source: Document source
            metadata: Additional metadata
        
        Returns:
            List of document chunks
        """
        if not content.strip():
            return []
        
        base_metadata = {
            "title": title,
            "source": source,
            **(metadata or {})
        }
        
        # First, try semantic chunking if enabled
        if self.config.use_semantic_splitting and len(content) > self.config.chunk_size:
            try:
                semantic_chunks = await self._semantic_chunk(content)
                if semantic_chunks:
                    return self._create_chunk_objects(
                        semantic_chunks,
                        content,
                        base_metadata
                    )
            except Exception as e:
                logger.warning(f"Semantic chunking failed, falling back to simple chunking: {e}")
        
        # Fallback to rule-based chunking
        return self._simple_chunk(content, base_metadata)
    
    async def _semantic_chunk(self, content: str) -> List[str]:
        """
        Perform semantic chunking using LLM.
        
        Args:
            content: Content to chunk
        
        Returns:
            List of chunk boundaries
        """
        # First, split on natural boundaries
        sections = self._split_on_structure(content)
        
        # Group sections into semantic chunks
        chunks = []
        current_chunk = ""
        
        for section in sections:
            # Check if adding this section would exceed chunk size
            potential_chunk = current_chunk + "\n\n" + section if current_chunk else section
            
            if len(potential_chunk) <= self.config.chunk_size:
                current_chunk = potential_chunk
            else:
                # Current chunk is ready, decide if we should split the section
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # Handle oversized sections
                if len(section) > self.config.max_chunk_size:
                    # Split the section semantically
                    sub_chunks = await self._split_long_section(section)
                    chunks.extend(sub_chunks)
                else:
                    current_chunk = section
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk.strip()) >= self.config.min_chunk_size]
    
    def _split_on_structure(self, content: str) -> List[str]:
        """
        Split content on structural boundaries.
        
        Args:
            content: Content to split
        
        Returns:
            List of sections
        """
        # Split on markdown headers, paragraphs, and other structural elements
        patterns = [
            r'\n#{1,6}\s+.+?\n',  # Markdown headers
            r'\n\n+',            # Multiple newlines (paragraph breaks)
            r'\n[-*+]\s+',       # List items
            r'\n\d+\.\s+',       # Numbered lists
            r'\n```.*?```\n',    # Code blocks
            r'\n\|\s*.+?\|\s*\n', # Tables
        ]
        
        # Split by patterns but keep the separators
        sections = [content]
        
        for pattern in patterns:
            new_sections = []
            for section in sections:
                parts = re.split(f'({pattern})', section, flags=re.MULTILINE | re.DOTALL)
                new_sections.extend([part for part in parts if part.strip()])
            sections = new_sections
        
        return sections
    
    async def _split_long_section(self, section: str) -> List[str]:
        """
        Split a long section using LLM for semantic boundaries.
        
        Args:
            section: Section to split
        
        Returns:
            List of sub-chunks
        """
        try:
            prompt = f"""
            Split the following text into semantically coherent chunks. Each chunk should:
            1. Be roughly {self.config.chunk_size} characters long
            2. End at natural semantic boundaries
            3. Maintain context and readability
            4. Not exceed {self.config.max_chunk_size} characters
            
            Return only the split text with "---CHUNK---" as separator between chunks.
            
            Text to split:
            {section}
            """
            
            # Use Pydantic AI for LLM calls
            from pydantic_ai import Agent
            temp_agent = Agent(self.model)
            
            response = await temp_agent.run(prompt)
            result = response.data
            chunks = [chunk.strip() for chunk in result.split("---CHUNK---")]
            
            # Validate chunks
            valid_chunks = []
            for chunk in chunks:
                if (self.config.min_chunk_size <= len(chunk) <= self.config.max_chunk_size):
                    valid_chunks.append(chunk)
            
            return valid_chunks if valid_chunks else self._simple_split(section)
            
        except Exception as e:
            logger.error(f"LLM chunking failed: {e}")
            return self._simple_split(section)
    
    def _simple_split(self, text: str) -> List[str]:
        """
        Simple text splitting as fallback.
        
        Args:
            text: Text to split
        
        Returns:
            List of chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.config.chunk_size
            
            if end >= len(text):
                # Last chunk
                chunks.append(text[start:])
                break
            
            # Try to end at a sentence boundary
            chunk_end = end
            for i in range(end, max(start + self.config.min_chunk_size, end - 200), -1):
                if text[i] in '.!?\n':
                    chunk_end = i + 1
                    break
            
            chunks.append(text[start:chunk_end])
            start = chunk_end - self.config.chunk_overlap
        
        return chunks
    
    def _simple_chunk(
        self,
        content: str,
        base_metadata: Dict[str, Any]
    ) -> List[DocumentChunk]:
        """
        Simple rule-based chunking.
        
        Args:
            content: Content to chunk
            base_metadata: Base metadata for chunks
        
        Returns:
            List of document chunks
        """
        chunks = self._simple_split(content)
        return self._create_chunk_objects(chunks, content, base_metadata)
    
    def _create_chunk_objects(
        self,
        chunks: List[str],
        original_content: str,
        base_metadata: Dict[str, Any]
    ) -> List[DocumentChunk]:
        """
        Create DocumentChunk objects from text chunks.
        
        Args:
            chunks: List of chunk texts
            original_content: Original document content
            base_metadata: Base metadata
        
        Returns:
            List of DocumentChunk objects
        """
        chunk_objects = []
        current_pos = 0
        
        for i, chunk_text in enumerate(chunks):
            # Find the position of this chunk in the original content
            start_pos = original_content.find(chunk_text, current_pos)
            if start_pos == -1:
                # Fallback: estimate position
                start_pos = current_pos
            
            end_pos = start_pos + len(chunk_text)
            
            # Create chunk metadata
            chunk_metadata = {
                **base_metadata,
                "chunk_method": "semantic" if self.config.use_semantic_splitting else "simple",
                "total_chunks": len(chunks)
            }
            
            chunk_objects.append(DocumentChunk(
                content=chunk_text.strip(),
                index=i,
                start_char=start_pos,
                end_char=end_pos,
                metadata=chunk_metadata
            ))
            
            current_pos = end_pos
        
        return chunk_objects


class SimpleChunker:
    """Simple non-semantic chunker for faster processing."""
    
    def __init__(self, config: ChunkingConfig):
        """Initialize simple chunker."""
        self.config = config
    
    def chunk_document(
        self,
        content: str,
        title: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[DocumentChunk]:
        """
        Chunk document using simple rules.
        
        Args:
            content: Document content
            title: Document title
            source: Document source
            metadata: Additional metadata
        
        Returns:
            List of document chunks
        """
        if not content.strip():
            return []
        
        base_metadata = {
            "title": title,
            "source": source,
            "chunk_method": "simple",
            **(metadata or {})
        }
        
        # Split on paragraphs first
        paragraphs = re.split(r'\n\s*\n', content)
        chunks = []
        current_chunk = ""
        current_pos = 0
        chunk_index = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Check if adding this paragraph exceeds chunk size
            potential_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
            
            if len(potential_chunk) <= self.config.chunk_size:
                current_chunk = potential_chunk
            else:
                # Save current chunk if it exists
                if current_chunk:
                    chunks.append(self._create_chunk(
                        current_chunk,
                        chunk_index,
                        current_pos,
                        current_pos + len(current_chunk),
                        base_metadata.copy()
                    ))
                    
                    # Move position, but ensure overlap is respected
                    overlap_start = max(0, len(current_chunk) - self.config.chunk_overlap)
                    current_pos += overlap_start
                    chunk_index += 1
                
                # Start new chunk with current paragraph
                current_chunk = paragraph
        
        # Add final chunk
        if current_chunk:
            chunks.append(self._create_chunk(
                current_chunk,
                chunk_index,
                current_pos,
                current_pos + len(current_chunk),
                base_metadata.copy()
            ))
        
        # Update total chunks in metadata
        for chunk in chunks:
            chunk.metadata["total_chunks"] = len(chunks)
        
        return chunks
    
    def _create_chunk(
        self,
        content: str,
        index: int,
        start_pos: int,
        end_pos: int,
        metadata: Dict[str, Any]
    ) -> DocumentChunk:
        """Create a DocumentChunk object."""
        return DocumentChunk(
            content=content.strip(),
            index=index,
            start_char=start_pos,
            end_char=end_pos,
            metadata=metadata
        )


# Factory function
def create_chunker(config: ChunkingConfig):
    """
    Create appropriate chunker based on configuration.
    
    Args:
        config: Chunking configuration
    
    Returns:
        Chunker instance
    """
    if config.use_semantic_splitting:
        return SemanticChunker(config)
    else:
        return SimpleChunker(config)


# Example usage
async def main():
    """Example usage of the chunker."""
    config = ChunkingConfig(
        chunk_size=500,
        chunk_overlap=50,
        use_semantic_splitting=True
    )
    
    chunker = create_chunker(config)
    
    sample_text = """
    # Big Tech AI Initiatives
    
    ## Google's AI Strategy
    Google has been investing heavily in artificial intelligence research and development.
    Their main focus areas include:
    
    - Large language models (LaMDA, PaLM, Gemini)
    - Computer vision and image recognition
    - Natural language processing
    - AI-powered search improvements
    
    The company's DeepMind division continues to push the boundaries of AI research,
    with breakthrough achievements in protein folding prediction and game playing.
    
    ## Microsoft's Partnership with OpenAI
    Microsoft's strategic partnership with OpenAI has positioned them as a leader
    in the generative AI space. Key developments include:
    
    1. Integration of GPT models into Office 365
    2. Azure OpenAI Service for enterprise customers
    3. Investment in OpenAI's continued research
    """
    
    chunks = await chunker.chunk_document(
        content=sample_text,
        title="Big Tech AI Report",
        source="example.md"
    )
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {len(chunk.content)} chars")
        print(f"Content: {chunk.content[:100]}...")
        print(f"Metadata: {chunk.metadata}")
        print("---")


if __name__ == "__main__":
    asyncio.run(main())