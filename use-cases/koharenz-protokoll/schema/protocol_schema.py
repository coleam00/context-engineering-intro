"""
Kohärenz Protocol - Pydantic Schema Definitions.

This module defines the core data structures for the Kohärenz Protocol narrative
system, providing type-safe models for agents, scenes, narrative mechanics, and
ontological analysis.

Author: Kohärenz Protocol Engineering Team
Version: 1.0.0
"""

from typing import List, Dict, Optional, Literal, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class TruthTheory(str, Enum):
    """Enumeration of truth theories used in the Foundation Protocol."""

    COHERENCE = "coherence"  # AEGIS: truth = internal consistency
    CORRESPONDENCE = "correspondence"  # Foundation: truth = external alignment
    PARACONSISTENT = "paraconsistent"  # KW2: contradictions can coexist


class Kernwelt(str, Enum):
    """
    Kernwelt (Core World) levels defining ontological rulesets.

    Each level represents a different logical framework governing reality.
    """

    KW0 = "KW0"  # Pre-collapse, undefined
    KW1 = "KW1"  # Classical logic (Law of Non-Contradiction enforced)
    KW2 = "KW2"  # Paraconsistent logic (contradictions permitted)
    KW3 = "KW3"  # Emergent integration (high-Φ states)
    KW4 = "KW4"  # Post-Bruchpunkt (Foundation-aligned)


class RissType(str, Enum):
    """Types of reality fractures (Risse) based on trauma-response systems."""

    KINETIC = "kinetic"  # Fight response: objects flung, space warps
    TEMPORAL = "temporal"  # Freeze response: time loops, stutters
    SENSORY_VOID = "sensory_void"  # Collapse response: sensory deprivation
    SPATIAL = "spatial"  # Flight response: distance distortion
    ONTOLOGICAL = "ontological"  # System-level coherence failure


class AlterDef(BaseModel):
    """Definition of a dissociative alter/part within a TSDP system."""

    name: str = Field(..., description="Name of the alter")
    role: str = Field(..., description="Functional role (e.g., protector, child EP)")
    action_system: str = Field(
        ...,
        description="Primary trauma-response system (fight/flight/freeze/collapse/social)"
    )
    riss_type: Optional[RissType] = Field(
        None,
        description="Type of Riss this alter generates when activated"
    )
    voice_characteristics: str = Field(
        ...,
        description="Linguistic/stylistic markers for this alter's voice"
    )
    integration_stage: int = Field(
        default=0,
        ge=0,
        le=10,
        description="Integration level (0=dissociated, 10=fully integrated)"
    )


class AgentDef(BaseModel):
    """Definition of a narrative agent with ontological properties."""

    id: str = Field(..., description="Unique agent identifier")
    name: str = Field(..., description="Agent display name")
    role: str = Field(..., description="Narrative function")
    ontology_type: str = Field(..., description="Ontological classification")
    truth_theory: TruthTheory = Field(..., description="Operating truth theory")
    system_prompt: str = Field(..., description="Base system prompt for LLM")
    alters: Optional[List[AlterDef]] = Field(
        None,
        description="List of alters (for TSDP multiplicity agents like Kael)"
    )
    constraints: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Behavioral constraints (never_x, always_x)"
    )
    response_preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tone, structure, linguistic preferences"
    )


class RissEvent(BaseModel):
    """A reality fracture event with causal linkage to internal state."""

    riss_id: str = Field(..., description="Unique Riss identifier")
    riss_type: RissType = Field(..., description="Type of reality fracture")
    trigger: str = Field(..., description="External trigger description")
    activated_alter: str = Field(..., description="Name of alter whose activation caused this Riss")
    internal_conflict: str = Field(
        ...,
        description="Description of ANP-EP phobia or internal coherence failure"
    )
    manifestation: str = Field(
        ...,
        description="Observable external manifestation of the fracture"
    )
    coherence_cost: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="K₁ coherence degradation (0=no impact, 1=total collapse)"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class SceneSpec(BaseModel):
    """Specification for generating or analyzing a narrative scene."""

    scene_id: str = Field(..., description="Unique scene identifier")
    title: str = Field(..., description="Scene title")
    kernwelt: Kernwelt = Field(..., description="Active Kernwelt for this scene")
    act: int = Field(..., ge=1, le=5, description="Act number (1-5)")
    participating_agents: List[str] = Field(
        ...,
        description="Agent IDs participating in this scene"
    )
    emotional_register: str = Field(
        ...,
        description="Target emotional tone (e.g., 'luminous despair', 'cold logic')"
    )
    narrative_beats: List[str] = Field(
        ...,
        description="Key narrative beats/events to include"
    )
    target_contradiction_density: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Target ratio of contradictory propositions (for KW2 scenes)"
    )
    riss_events: List[RissEvent] = Field(
        default_factory=list,
        description="Riss events occurring in this scene"
    )


class SceneFragment(BaseModel):
    """A generated narrative fragment with metadata."""

    fragment_id: str = Field(..., description="Unique fragment identifier")
    scene_id: str = Field(..., description="Parent scene ID")
    speaker: str = Field(..., description="Primary speaker (alter or agent)")
    secondary_speakers: List[str] = Field(
        default_factory=list,
        description="Additional voices in polyphonic fragments"
    )
    content: str = Field(..., description="The actual narrative text")
    voice_markers: List[str] = Field(
        default_factory=list,
        description="Linguistic markers present (brackets, em-dashes, etc.)"
    )
    coherence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="K₁ coherence metric (0=total entropy, 1=perfect order)"
    )
    integration_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Φ (phi) integration metric (0=dissociated, 1=unified)"
    )


class OntologyReport(BaseModel):
    """Analysis report for ontological consistency and narrative metrics."""

    report_id: str = Field(..., description="Unique report identifier")
    scene_id: str = Field(..., description="Analyzed scene ID")
    timestamp: datetime = Field(default_factory=datetime.now)

    # Coherence metrics
    contradiction_density: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Ratio of contradictory propositions detected"
    )
    alter_balance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Distribution entropy across alters (0=monopoly, 1=balanced)"
    )
    riss_progression_index: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Cumulative Riss intensity (0=stable, 1=total fracture)"
    )

    # Integration metrics
    integration_trajectory: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Progress toward functional multiplicity (0=fragmented, 1=integrated)"
    )
    phi_estimate: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated Φ (integrated information) for Kael's system"
    )

    # Violations and suggestions
    violations: List[str] = Field(
        default_factory=list,
        description="Foundation Protocol violations detected"
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improving ontological consistency"
    )

    # Gödel analysis
    godel_vulnerabilities: List[str] = Field(
        default_factory=list,
        description="Detected Gödel-incompleteness points (unprovable truths)"
    )


class KernelState(BaseModel):
    """State of the dual kernel system (K₁/K₀) at a given moment."""

    k1_coherence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="K₁ (Coherence Kernel) strength"
    )
    k0_entropy: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="K₀ (Collapse Kernel) pressure"
    )
    overhead_cost: float = Field(
        ...,
        ge=0.0,
        description="Energy cost to maintain coherence against K₀"
    )
    corrective_wavelets_active: int = Field(
        default=0,
        ge=0,
        description="Number of active corrective wavelets being emitted"
    )
    system_stability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall system stability (0=collapsing, 1=stable)"
    )


class ProtocolConfig(BaseModel):
    """Complete configuration for a Kohärenz Protocol implementation."""

    version: str = Field(..., description="Protocol version")
    agents: List[AgentDef] = Field(..., description="All agents in the system")
    default_kernwelt: Kernwelt = Field(
        default=Kernwelt.KW2,
        description="Default Kernwelt for unspecified contexts"
    )
    enable_riss_generation: bool = Field(
        default=True,
        description="Whether to generate Riss events dynamically"
    )
    enable_godel_checks: bool = Field(
        default=True,
        description="Whether to check for Gödel-incompleteness patterns"
    )
    metaphysical_constants: Dict[str, float] = Field(
        default_factory=lambda: {
            "k1_base_strength": 0.6,
            "k0_base_pressure": 0.4,
            "phi_integration_threshold": 0.7,
            "bruchpunkt_threshold": 0.85
        },
        description="Tunable constants for Foundation Protocol physics"
    )

    @field_validator("agents")
    @classmethod
    def validate_agent_ids_unique(cls, agents: List[AgentDef]) -> List[AgentDef]:
        """Ensure all agent IDs are unique."""
        ids = [agent.id for agent in agents]
        if len(ids) != len(set(ids)):
            raise ValueError("Agent IDs must be unique")
        return agents


class GenerationRequest(BaseModel):
    """Request for generating narrative content."""

    scene_spec: SceneSpec = Field(..., description="Scene specification")
    num_fragments: int = Field(
        default=3,
        ge=1,
        le=20,
        description="Number of fragments to generate"
    )
    temperature: float = Field(
        default=0.8,
        ge=0.0,
        le=2.0,
        description="LLM temperature for generation"
    )
    seed: Optional[int] = Field(
        None,
        description="Random seed for deterministic generation (testing)"
    )


class GenerationResponse(BaseModel):
    """Response containing generated narrative fragments."""

    request_id: str = Field(..., description="Request identifier")
    scene_id: str = Field(..., description="Scene ID")
    fragments: List[SceneFragment] = Field(..., description="Generated fragments")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Generation metadata (model, timestamp, etc.)"
    )
    ontology_report: Optional[OntologyReport] = Field(
        None,
        description="Automatic ontology analysis of generated content"
    )


# Example instantiation for testing/documentation
if __name__ == "__main__":
    # Example: Create a Kael alter definition
    kael_host = AlterDef(
        name="Kael",
        role="Host ANP",
        action_system="social/mediator",
        voice_characteristics="measured, introspective, attempts coherence",
        integration_stage=3
    )

    # Example: Create a Riss event
    riss = RissEvent(
        riss_id="riss_001",
        riss_type=RissType.TEMPORAL,
        trigger="memory of abandonment",
        activated_alter="Kiko",
        internal_conflict="Kael (ANP) attempting to suppress Kiko's (EP) freeze response",
        manifestation="time loop: 3.7 seconds repeating, sound distortion",
        coherence_cost=0.42
    )

    # Example: Create a scene spec
    scene = SceneSpec(
        scene_id="act1_scene3",
        title="First Riss: The Coffee Shop Incident",
        kernwelt=Kernwelt.KW2,
        act=1,
        participating_agents=["kael_agent_v1"],
        emotional_register="quiet dread, creeping dissociation",
        narrative_beats=[
            "Kael orders coffee",
            "Barista's tone triggers abandonment memory",
            "Kiko activates, Kael tries to suppress",
            "Temporal Riss manifests: time stutters"
        ],
        target_contradiction_density=0.35,
        riss_events=[riss]
    )

    print("✓ Schema validation successful")
    print(f"Scene: {scene.title}")
    print(f"Kernwelt: {scene.kernwelt.value}")
    print(f"Riss count: {len(scene.riss_events)}")
