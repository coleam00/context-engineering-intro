"""
Data models for novel structure extraction.
"""

from pydantic import BaseModel
from typing import List, Dict, Optional


class NovelMetadata(BaseModel):
    """
    Metadata about the novel being analyzed.
    """

    title: str
    author: Optional[str] = None
    word_count: int
    file_path: str


class Character(BaseModel):
    """
    Character information extracted from the novel.
    """

    name: str
    description: str
    role: str  # protagonist, antagonist, supporting
    relationships: Dict[str, str]  # character_name -> relationship_type


class PlotPoint(BaseModel):
    """
    Key plot event in the novel.
    """

    chapter: int
    event: str
    significance: str
    characters_involved: List[str]


class NovelStructure(BaseModel):
    """
    Complete novel structure extracted from analysis.
    """

    metadata: NovelMetadata
    theme: str
    setting: str
    timeline: str
    narrative_style: str
    point_of_view: str
    characters: List[Character]
    plot_points: List[PlotPoint]
