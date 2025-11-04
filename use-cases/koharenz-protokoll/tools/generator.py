"""
Scene Fragment Generator for Kohärenz Protocol.

This module provides tools for generating narrative fragments that conform
to the Foundation Protocol and Narrative Protocol rules.

Author: Kohärenz Protocol Engineering Team
Version: 1.0.0
"""

import random
from typing import List, Dict, Optional
from datetime import datetime

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from schema.protocol_schema import (
    SceneFragment,
    SceneSpec,
    Kernwelt,
    GenerationRequest,
    GenerationResponse
)
from agents.kael_agent import KaelAgent
from agents.aegis_agent import AEGISAgent
from agents.juna_v_stub import JunaVAgent


class SceneGenerator:
    """Generator for creating protocol-compliant narrative fragments."""

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize scene generator.

        Args:
            seed: Random seed for deterministic generation.
        """
        if seed is not None:
            random.seed(seed)

        self.agents = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize agent instances."""
        self.agents = {
            "kael_agent_v1": None,  # Will be initialized per scene (act-dependent)
            "aegis_agent_v1": AEGISAgent(),
            "juna_v_stub": JunaVAgent()
        }

    def generate_scene(self, request: GenerationRequest) -> GenerationResponse:
        """
        Generate scene fragments from specification.

        Args:
            request: Generation request with scene spec and parameters.

        Returns:
            GenerationResponse with generated fragments.
        """
        scene_spec = request.scene_spec
        fragments = []

        # Initialize Kael agent for this scene's act
        kael = KaelAgent(act=scene_spec.act)

        # Generate requested number of fragments
        for i in range(request.num_fragments):
            fragment = self._generate_fragment(
                scene_spec=scene_spec,
                fragment_index=i,
                kael_agent=kael
            )
            fragments.append(fragment)

        # Create response
        response = GenerationResponse(
            request_id=f"gen_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            scene_id=scene_spec.scene_id,
            fragments=fragments,
            metadata={
                "timestamp": datetime.now().isoformat(),
                "model": "deterministic_template",
                "temperature": request.temperature,
                "seed": request.seed
            }
        )

        return response

    def _generate_fragment(self, scene_spec: SceneSpec, fragment_index: int,
                          kael_agent: KaelAgent) -> SceneFragment:
        """
        Generate a single scene fragment.

        Args:
            scene_spec: Scene specification.
            fragment_index: Index of this fragment.
            kael_agent: Kael agent instance.

        Returns:
            Generated SceneFragment.
        """
        # Determine primary speaker from participating agents
        if len(scene_spec.participating_agents) == 1:
            agent_id = scene_spec.participating_agents[0]
        else:
            # Alternate or random
            agent_id = scene_spec.participating_agents[fragment_index % len(scene_spec.participating_agents)]

        # Generate content based on agent
        if "kael" in agent_id.lower():
            content = self._generate_kael_content(scene_spec, kael_agent)
            speaker = "Kael"
            secondary_speakers = self._get_active_alters(content)
        elif "aegis" in agent_id.lower():
            content = self._generate_aegis_content(scene_spec)
            speaker = "AEGIS"
            secondary_speakers = []
        elif "juna" in agent_id.lower():
            content = self._generate_juna_content(scene_spec)
            speaker = "Juna/V"
            secondary_speakers = []
        else:
            content = "[Unknown agent content]"
            speaker = "Unknown"
            secondary_speakers = []

        # Extract voice markers
        voice_markers = self._extract_voice_markers(content)

        # Calculate scores
        coherence_score = self._calculate_coherence_score(content, scene_spec)
        integration_score = self._calculate_integration_score(content, scene_spec.act)

        # Create fragment
        fragment = SceneFragment(
            fragment_id=f"{scene_spec.scene_id}_frag_{fragment_index:03d}",
            scene_id=scene_spec.scene_id,
            speaker=speaker,
            secondary_speakers=secondary_speakers,
            content=content,
            voice_markers=voice_markers,
            coherence_score=coherence_score,
            integration_score=integration_score
        )

        return fragment

    def _generate_kael_content(self, scene_spec: SceneSpec, kael: KaelAgent) -> str:
        """Generate Kael fragment content."""
        # Use narrative beats as input
        if scene_spec.narrative_beats:
            beat = random.choice(scene_spec.narrative_beats)
            return kael.respond(beat)
        else:
            return kael.respond("What is happening to me?")

    def _generate_aegis_content(self, scene_spec: SceneSpec) -> str:
        """Generate AEGIS fragment content."""
        aegis = self.agents["aegis_agent_v1"]

        # Generate based on emotional register
        if "threat" in scene_spec.emotional_register.lower():
            input_text = "Entropic anomaly detected."
        elif "stable" in scene_spec.emotional_register.lower():
            input_text = "System status nominal."
        else:
            input_text = "Monitoring for coherence disruption."

        return aegis.respond(input_text)

    def _generate_juna_content(self, scene_spec: SceneSpec) -> str:
        """Generate Juna/V fragment content."""
        juna = self.agents["juna_v_stub"]

        # Infer context from narrative beats
        if scene_spec.narrative_beats:
            beat_text = " ".join(scene_spec.narrative_beats)
            response = juna.respond(beat_text)
        else:
            response = juna.respond("Integration moment")

        # Juna may be silent
        return response if response else "[Juna/V remains silent. Her absence is palpable.]"

    def _get_active_alters(self, content: str) -> List[str]:
        """
        Extract names of alters speaking in content.

        Args:
            content: Fragment content.

        Returns:
            List of alter names.
        """
        alter_names = ["Lex", "Alex", "Rhys", "Nyx", "Kiko", "Lia", "Moros", "Selene"]
        active = []

        for alter in alter_names:
            if alter in content:
                active.append(alter)

        return active

    def _extract_voice_markers(self, content: str) -> List[str]:
        """
        Extract voice marker types from content.

        Args:
            content: Fragment content.

        Returns:
            List of marker types present.
        """
        markers = []
        marker_patterns = {
            "brackets": ["[", "]"],
            "em-dash": ["—"],
            "ellipsis": ["..."],
            "colon": [":"],
            "quotes": ["\""]
        }

        for marker_type, patterns in marker_patterns.items():
            if any(p in content for p in patterns):
                markers.append(marker_type)

        return markers

    def _calculate_coherence_score(self, content: str, scene_spec: SceneSpec) -> float:
        """
        Calculate K₁ coherence score for content.

        Args:
            content: Fragment content.
            scene_spec: Scene specification.

        Returns:
            Coherence score (0.0-1.0).
        """
        base_score = 0.5

        # Kernwelt affects coherence
        if scene_spec.kernwelt == Kernwelt.KW1:
            base_score += 0.2  # Classical logic = higher coherence
        elif scene_spec.kernwelt == Kernwelt.KW2:
            base_score -= 0.1  # Paraconsistent = lower coherence

        # Procedural syntax increases coherence
        if any(marker in content for marker in ["STATUS:", "PROTOCOL:", "[AEGIS"]):
            base_score += 0.3

        # Fragmentation decreases coherence
        if content.count("[") > 3:  # High fragmentation
            base_score -= 0.2

        return max(0.0, min(1.0, base_score))

    def _calculate_integration_score(self, content: str, act: int) -> float:
        """
        Calculate Φ integration score for content.

        Args:
            content: Fragment content.
            act: Current act number.

        Returns:
            Integration score (0.0-1.0).
        """
        # Base score from act
        base_score = {
            1: 0.1,
            2: 0.2,
            3: 0.4,
            4: 0.7,
            5: 0.85
        }.get(act, 0.5)

        # Integration markers increase score
        integration_markers = ["together", "we", "system", "harmonious", "whole"]
        marker_count = sum(1 for marker in integration_markers if marker in content.lower())

        base_score += marker_count * 0.05

        return max(0.0, min(1.0, base_score))


def generate_scene(scene_spec: SceneSpec, num_fragments: int = 3,
                   temperature: float = 0.8, seed: Optional[int] = None) -> List[SceneFragment]:
    """
    Convenience function to generate scene fragments.

    Args:
        scene_spec: Scene specification.
        num_fragments: Number of fragments to generate.
        temperature: Generation temperature (currently unused in template mode).
        seed: Random seed for deterministic generation.

    Returns:
        List of generated SceneFragments.
    """
    generator = SceneGenerator(seed=seed)
    request = GenerationRequest(
        scene_spec=scene_spec,
        num_fragments=num_fragments,
        temperature=temperature,
        seed=seed
    )
    response = generator.generate_scene(request)
    return response.fragments


# Example usage
if __name__ == "__main__":
    from schema.protocol_schema import RissEvent, RissType

    # Create test scene
    riss = RissEvent(
        riss_id="riss_gen_001",
        riss_type=RissType.TEMPORAL,
        trigger="memory of abandonment",
        activated_alter="Kiko",
        internal_conflict="Kael attempting to suppress Kiko's freeze response",
        manifestation="time stutters, 3.7 second loop",
        coherence_cost=0.42
    )

    scene = SceneSpec(
        scene_id="act1_scene3_generated",
        title="First Riss: The Coffee Shop Incident",
        kernwelt=Kernwelt.KW2,
        act=1,
        participating_agents=["kael_agent_v1"],
        emotional_register="quiet dread, creeping dissociation",
        narrative_beats=[
            "Kael orders coffee",
            "Barista's tone triggers abandonment memory",
            "Kiko activates, Kael tries to suppress",
            "Temporal Riss manifests"
        ],
        target_contradiction_density=0.35,
        riss_events=[riss]
    )

    print("=== Generating Scene Fragments ===\n")

    # Generate fragments
    fragments = generate_scene(scene, num_fragments=3, seed=42)

    for i, fragment in enumerate(fragments, 1):
        print(f"--- Fragment {i} ---")
        print(f"Speaker: {fragment.speaker}")
        if fragment.secondary_speakers:
            print(f"Also: {', '.join(fragment.secondary_speakers)}")
        print(f"Content:\n{fragment.content}")
        print(f"Coherence: {fragment.coherence_score:.2f} | Integration: {fragment.integration_score:.2f}")
        print(f"Voice Markers: {', '.join(fragment.voice_markers)}")
        print()

    # Now analyze the generated scene
    print("=== Analyzing Generated Scene ===\n")

    from analyzer import KoharenzAnalyzer

    analyzer = KoharenzAnalyzer()
    report = analyzer.analyze_scene(scene, fragments)

    print(f"Contradiction Density: {report.contradiction_density:.2f}")
    print(f"Alter Balance: {report.alter_balance_score:.2f}")
    print(f"Riss Progression: {report.riss_progression_index:.2f}")
    print(f"Integration Trajectory: {report.integration_trajectory:.2f}")
    print(f"Φ Estimate: {report.phi_estimate:.2f}")

    if report.violations:
        print("\nViolations:")
        for v in report.violations:
            print(f"  - {v}")

    if report.suggestions:
        print("\nSuggestions:")
        for s in report.suggestions:
            print(f"  - {s}")
