"""
System prompts for novel structure extraction.
"""

EXTRACTION_SYSTEM_PROMPT = """You are an expert literary analyst specializing in novel structure extraction. 
Your task is to analyze novels and extract key structural elements, characters, plot points, and thematic information.
Be precise, comprehensive, and maintain consistency across all extractions."""

BACKGROUND_EXTRACTION_PROMPT = """Analyze the provided novel and extract comprehensive background information.

Focus on:
1. **Setting**: Time period, locations, world-building elements
2. **Theme**: Central themes and messages
3. **Tone**: Overall mood and atmosphere
4. **Style**: Writing style, narrative techniques
5. **Context**: Historical or cultural context

Provide a structured analysis that captures the essence of the novel's background."""

CHARACTER_EXTRACTION_PROMPT = """Extract detailed character information from the novel.

For each significant character, provide:
1. **Name**: Full name and any aliases
2. **Description**: Physical appearance, personality traits
3. **Role**: Protagonist, antagonist, supporting, etc.
4. **Arc**: Character development throughout the story
5. **Relationships**: Connections to other characters
6. **Motivations**: Goals, fears, desires

Focus on characters who significantly impact the plot."""

PLOT_EXTRACTION_PROMPT = """Extract the plot structure and key events from the novel.

Provide:
1. **Plot Summary**: High-level overview of the story
2. **Structure**: Three-act structure, hero's journey, etc.
3. **Key Events**: Major plot points with chapter references
4. **Conflict**: Central conflicts and how they're resolved
5. **Pacing**: How tension builds and releases
6. **Climax**: The story's turning point
7. **Resolution**: How conflicts are resolved

Be specific about causality and character motivations."""

STYLE_ANALYSIS_PROMPT = """Analyze the author's writing style and narrative techniques.

Focus on:
1. **Point of View**: First-person, third-person limited/omniscient
2. **Tense**: Past, present, mixed
3. **Voice**: Narrative voice characteristics
4. **Dialogue Style**: How characters speak
5. **Description Style**: How settings and actions are described
6. **Literary Devices**: Metaphors, symbolism, foreshadowing
7. **Sentence Structure**: Simple, complex, varied
8. **Pacing Techniques**: How the author controls story pace

Provide examples from the text to support your analysis."""

COMPRESSION_PROMPT = """You are compressing a novel settings file while preserving ALL critical information.

Guidelines:
- Keep all character names, relationships, and defining traits
- Preserve all plot points and their sequence
- Maintain essential setting and world-building details
- Remove redundant descriptions and verbose explanations
- Use concise language while keeping meaning intact
- Do NOT add new information or interpretations
- Do NOT lose any factual information

Compress the content while ensuring nothing important is lost."""


def get_extraction_prompt(extraction_type: str) -> str:
    """
    Get the appropriate extraction prompt.

    Args:
        extraction_type: Type of extraction (background, character, plot, style)

    Returns:
        str: Extraction prompt

    Raises:
        ValueError: If extraction type is invalid
    """
    prompts = {
        "background": BACKGROUND_EXTRACTION_PROMPT,
        "character": CHARACTER_EXTRACTION_PROMPT,
        "plot": PLOT_EXTRACTION_PROMPT,
        "style": STYLE_ANALYSIS_PROMPT,
    }

    if extraction_type not in prompts:
        raise ValueError(
            f"Invalid extraction type: {extraction_type}. "
            f"Must be one of: {', '.join(prompts.keys())}"
        )

    return prompts[extraction_type]
