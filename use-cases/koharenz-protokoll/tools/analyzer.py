"""
Ontology Analyzer for Kohärenz Protocol.

This module provides tools for analyzing narrative fragments and scenes
to ensure consistency with the Foundation Protocol and Narrative Protocol.

Author: Kohärenz Protocol Engineering Team
Version: 1.0.0
"""

import re
import math
from typing import List, Dict, Tuple
from datetime import datetime
from collections import Counter

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from schema.protocol_schema import (
    SceneFragment,
    SceneSpec,
    OntologyReport,
    Kernwelt
)


class KoharenzAnalyzer:
    """Analyzer for validating narrative consistency with protocol rules."""

    def __init__(self):
        """Initialize analyzer with protocol rules."""
        self.alter_names = [
            "Kael", "Lex", "Alex", "Rhys", "Nyx",
            "Kiko", "Lia", "Moros", "Selene"
        ]
        self.voice_markers = ["[", "]", "—", "...", ":",  "whimpering", "interjects"]
        self.paradox_indicators = [
            "but", "yet", "however", "although", "contradiction",
            "impossible", "cannot", "must not", "both", "neither"
        ]

    def analyze_scene(self, scene_spec: SceneSpec, fragments: List[SceneFragment]) -> OntologyReport:
        """
        Analyze a complete scene for protocol consistency.

        Args:
            scene_spec: Scene specification.
            fragments: List of generated fragments.

        Returns:
            OntologyReport with metrics and violations.
        """
        # Calculate metrics
        contradiction_density = self.calculate_contradiction_density(fragments)
        alter_balance = self.calculate_alter_balance(fragments)
        riss_progression = self.calculate_riss_progression(scene_spec)
        integration_trajectory = self.estimate_integration_trajectory(fragments, scene_spec.act)
        phi_estimate = self.estimate_phi(fragments, scene_spec.act)

        # Detect violations
        violations = self._detect_violations(scene_spec, fragments)

        # Generate suggestions
        suggestions = self._generate_suggestions(scene_spec, fragments, violations)

        # Gödel analysis
        godel_vulnerabilities = self._detect_godel_patterns(fragments)

        return OntologyReport(
            report_id=f"report_{scene_spec.scene_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            scene_id=scene_spec.scene_id,
            contradiction_density=contradiction_density,
            alter_balance_score=alter_balance,
            riss_progression_index=riss_progression,
            integration_trajectory=integration_trajectory,
            phi_estimate=phi_estimate,
            violations=violations,
            suggestions=suggestions,
            godel_vulnerabilities=godel_vulnerabilities
        )

    def calculate_contradiction_density(self, fragments: List[SceneFragment]) -> float:
        """
        Calculate ratio of contradictory propositions.

        Args:
            fragments: List of scene fragments.

        Returns:
            Contradiction density (0.0-1.0).
        """
        total_sentences = 0
        contradictory_sentences = 0

        for fragment in fragments:
            sentences = re.split(r'[.!?]', fragment.content)
            sentences = [s.strip() for s in sentences if s.strip()]
            total_sentences += len(sentences)

            # Count sentences with paradox indicators
            for sentence in sentences:
                if any(indicator in sentence.lower() for indicator in self.paradox_indicators):
                    contradictory_sentences += 1

        if total_sentences == 0:
            return 0.0

        return min(1.0, contradictory_sentences / total_sentences)

    def calculate_alter_balance(self, fragments: List[SceneFragment]) -> float:
        """
        Calculate distribution entropy across alters (Alter Balance Score).

        Higher score = more balanced distribution of voices.

        Args:
            fragments: List of scene fragments.

        Returns:
            Alter balance score (0.0-1.0).
        """
        speaker_counts = Counter()

        for fragment in fragments:
            speaker_counts[fragment.speaker] += 1
            for secondary in fragment.secondary_speakers:
                speaker_counts[secondary] += 0.5  # Secondary speakers count less

        if not speaker_counts:
            return 0.0

        # Calculate Shannon entropy
        total = sum(speaker_counts.values())
        probabilities = [count / total for count in speaker_counts.values()]
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)

        # Normalize to 0-1 (max entropy is log2(n) where n is number of speakers)
        max_entropy = math.log2(len(speaker_counts)) if len(speaker_counts) > 1 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0

        return min(1.0, normalized_entropy)

    def calculate_riss_progression(self, scene_spec: SceneSpec) -> float:
        """
        Calculate cumulative Riss intensity.

        Args:
            scene_spec: Scene specification with Riss events.

        Returns:
            Riss progression index (0.0-1.0).
        """
        if not scene_spec.riss_events:
            return 0.0

        total_coherence_cost = sum(
            riss.coherence_cost for riss in scene_spec.riss_events
        )

        # Normalize by number of events and max possible cost
        avg_cost = total_coherence_cost / len(scene_spec.riss_events)

        return min(1.0, avg_cost)

    def estimate_integration_trajectory(self, fragments: List[SceneFragment], act: int) -> float:
        """
        Estimate progress toward functional multiplicity.

        Args:
            fragments: List of scene fragments.
            act: Current act number.

        Returns:
            Integration trajectory (0.0-1.0).
        """
        # Base trajectory from act
        base_trajectory = {
            1: 0.1,
            2: 0.2,
            3: 0.5,
            4: 0.7,
            5: 0.9
        }.get(act, 0.5)

        # Adjust based on markers of integration
        integration_markers = [
            "together", "we are", "harmonious", "integrated",
            "cooperative", "unified", "whole", "system"
        ]

        marker_count = 0
        total_words = 0

        for fragment in fragments:
            words = fragment.content.lower().split()
            total_words += len(words)
            marker_count += sum(1 for word in words if any(m in word for m in integration_markers))

        if total_words > 0:
            marker_density = marker_count / total_words
            # Adjust base by marker density
            adjustment = marker_density * 0.3  # Max 0.3 adjustment
            return min(1.0, base_trajectory + adjustment)

        return base_trajectory

    def estimate_phi(self, fragments: List[SceneFragment], act: int) -> float:
        """
        Estimate Φ (integrated information) for Kael's system.

        Args:
            fragments: List of scene fragments.
            act: Current act number.

        Returns:
            Φ estimate (0.0-1.0).
        """
        # Base Φ from act
        base_phi = {
            1: 0.1,
            2: 0.2,
            3: 0.4,
            4: 0.7,
            5: 0.85
        }.get(act, 0.5)

        # Check for polyphonic vs. fragmented markers
        polyphonic_markers = ["[", "]", ":", "—"]
        integration_markers = ["we", "together", "system"]

        poly_count = 0
        int_count = 0

        for fragment in fragments:
            content_lower = fragment.content.lower()
            poly_count += sum(fragment.content.count(m) for m in polyphonic_markers)
            int_count += sum(content_lower.count(m) for m in integration_markers)

        # High polyphonic markers = organized multiplicity (raises Φ)
        # High integration markers = unified multiplicity (raises Φ more)
        if poly_count > 10:  # Organized polyphony
            base_phi += 0.1
        if int_count > 5:  # Integration language
            base_phi += 0.2

        return min(1.0, base_phi)

    def _detect_violations(self, scene_spec: SceneSpec, fragments: List[SceneFragment]) -> List[str]:
        """
        Detect Foundation Protocol violations.

        Args:
            scene_spec: Scene specification.
            fragments: List of fragments.

        Returns:
            List of violation descriptions.
        """
        violations = []

        # Check Kernwelt consistency
        if scene_spec.kernwelt == Kernwelt.KW1:
            # KW1: Classical logic, no contradictions allowed
            cd = self.calculate_contradiction_density(fragments)
            if cd > 0.1:
                violations.append(
                    f"KW1 violation: Contradiction density {cd:.2f} exceeds threshold (0.1). "
                    "Classical logic enforces Law of Non-Contradiction."
                )

        elif scene_spec.kernwelt == Kernwelt.KW2:
            # KW2: Paraconsistent logic, contradictions expected
            cd = self.calculate_contradiction_density(fragments)
            if cd < 0.2:
                violations.append(
                    f"KW2 expectation: Contradiction density {cd:.2f} below expected range (0.3-0.5). "
                    "KW2 should embrace paradox."
                )

        # Check voice evolution consistency
        if scene_spec.act >= 4:
            # Late acts should show integration
            trajectory = self.estimate_integration_trajectory(fragments, scene_spec.act)
            if trajectory < 0.6:
                violations.append(
                    f"Integration violation: Act {scene_spec.act} shows trajectory {trajectory:.2f}, "
                    "expected >= 0.6 for late-act integration."
                )

        # Check AEGIS language if present
        if "aegis_agent_v1" in scene_spec.participating_agents:
            for fragment in fragments:
                if "aegis" in fragment.speaker.lower():
                    # AEGIS should use procedural syntax
                    if not any(marker in fragment.content for marker in ["[AEGIS", "STATUS:", "PROTOCOL:"]):
                        violations.append(
                            f"AEGIS voice violation: Fragment {fragment.fragment_id} lacks procedural syntax."
                        )

        return violations

    def _generate_suggestions(self, scene_spec: SceneSpec, fragments: List[SceneFragment],
                             violations: List[str]) -> List[str]:
        """
        Generate suggestions for improving ontological consistency.

        Args:
            scene_spec: Scene specification.
            fragments: List of fragments.
            violations: Detected violations.

        Returns:
            List of suggestions.
        """
        suggestions = []

        # Suggest based on violations
        if any("KW1 violation" in v for v in violations):
            suggestions.append(
                "Reduce contradiction density by ensuring propositions are logically consistent. "
                "Remove paradoxical language."
            )

        if any("KW2 expectation" in v for v in violations):
            suggestions.append(
                "Increase contradiction density by introducing paraconsistent propositions. "
                "Use 'but', 'yet', 'both/and' constructions."
            )

        if any("Integration violation" in v for v in violations):
            suggestions.append(
                "Increase integration markers: use 'we' language, show cooperative alter dialogue, "
                "reduce fragmentation and chaos."
            )

        if any("AEGIS voice violation" in v for v in violations):
            suggestions.append(
                "Ensure AEGIS uses procedural syntax: [AEGIS.CORE.vX.X], STATUS:, PROTOCOL:, etc. "
                "Avoid emotional or metaphorical language."
            )

        # General suggestions based on metrics
        alter_balance = self.calculate_alter_balance(fragments)
        if alter_balance < 0.3 and scene_spec.act >= 3:
            suggestions.append(
                f"Alter balance score {alter_balance:.2f} is low for Act {scene_spec.act}. "
                "Consider giving voice to more alters to show polyphonic emergence."
            )

        return suggestions

    def _detect_godel_patterns(self, fragments: List[SceneFragment]) -> List[str]:
        """
        Detect Gödel-incompleteness patterns (unprovable truths).

        Args:
            fragments: List of fragments.

        Returns:
            List of detected Gödel vulnerabilities.
        """
        vulnerabilities = []

        godel_indicators = [
            "cannot prove", "unprovable", "irresolvable", "paradox",
            "undefined", "impossible yet true", "exists but cannot"
        ]

        for fragment in fragments:
            content_lower = fragment.content.lower()
            for indicator in godel_indicators:
                if indicator in content_lower:
                    vulnerabilities.append(
                        f"Gödel pattern detected in {fragment.fragment_id}: "
                        f"'{indicator}' suggests unprovable truth within system."
                    )
                    break  # One per fragment max

        return vulnerabilities


# Example usage
if __name__ == "__main__":
    from schema.protocol_schema import RissEvent, RissType

    # Create test scene
    riss = RissEvent(
        riss_id="riss_test_001",
        riss_type=RissType.TEMPORAL,
        trigger="memory trigger",
        activated_alter="Kiko",
        internal_conflict="Kael suppressing Kiko",
        manifestation="time stutters",
        coherence_cost=0.4
    )

    scene = SceneSpec(
        scene_id="test_scene_1",
        title="Test Scene",
        kernwelt=Kernwelt.KW2,
        act=3,
        participating_agents=["kael_agent_v1"],
        emotional_register="tense polyphony",
        narrative_beats=["Internal dialogue", "Alter conflict", "Partial resolution"],
        target_contradiction_density=0.4,
        riss_events=[riss]
    )

    # Create test fragments
    fragments = [
        SceneFragment(
            fragment_id="frag_001",
            scene_id="test_scene_1",
            speaker="Kael",
            content="[Kael: I want to understand.] — Lex: 'Analysis required.' — [Kiko: scared...]",
            voice_markers=["[", "]", "—", ":"],
            coherence_score=0.6,
            integration_score=0.4
        ),
        SceneFragment(
            fragment_id="frag_002",
            scene_id="test_scene_1",
            speaker="Lex",
            content="The data is contradictory yet consistent. Both true and false simultaneously.",
            voice_markers=[],
            coherence_score=0.5,
            integration_score=0.4
        )
    ]

    # Analyze
    analyzer = KoharenzAnalyzer()
    report = analyzer.analyze_scene(scene, fragments)

    print("=== Ontology Report ===")
    print(f"Scene: {scene.title}")
    print(f"Contradiction Density: {report.contradiction_density:.2f}")
    print(f"Alter Balance: {report.alter_balance_score:.2f}")
    print(f"Riss Progression: {report.riss_progression_index:.2f}")
    print(f"Integration Trajectory: {report.integration_trajectory:.2f}")
    print(f"Φ Estimate: {report.phi_estimate:.2f}")
    print(f"\nViolations: {len(report.violations)}")
    for v in report.violations:
        print(f"  - {v}")
    print(f"\nSuggestions: {len(report.suggestions)}")
    for s in report.suggestions:
        print(f"  - {s}")
    print(f"\nGödel Vulnerabilities: {len(report.godel_vulnerabilities)}")
    for g in report.godel_vulnerabilities:
        print(f"  - {g}")
