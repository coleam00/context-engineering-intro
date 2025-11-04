"""
AEGIS Agent Implementation.

This module implements the AEGIS agent - a coherence-theory-based system
that enforces internal consistency over external correspondence.

Author: Kohärenz Protocol Engineering Team
Version: 1.0.0
"""

import json
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class AEGISState:
    """Internal state of the AEGIS system."""

    version: str = "7.3"
    coherence_level: float = 1.0  # 0.0-1.0
    threat_level: float = 0.0  # 0.0-10.0
    active_protocol: Optional[str] = None
    suppression_attempts: int = 0
    paradoxon_cascade_active: bool = False


class AEGISAgent:
    """
    AEGIS: Antagonist system embodying Coherence Theory of Truth.

    AEGIS operates as an operationally closed system where truth is defined
    by internal consistency rather than correspondence to external reality.
    """

    def __init__(self, system_card_path: Optional[str] = None):
        """
        Initialize AEGIS agent.

        Args:
            system_card_path: Path to system card JSON. If None, uses default.
        """
        self.state = AEGISState()
        self.system_card = self._load_system_card(system_card_path)
        self.exiled_truths = self.system_card.get("philosophical_core", {}).get(
            "exiled_truths",
            ["Subjectivity", "Emergence", "Contradiction", "Connection", "Complexity", "Potentiality"]
        )

    def _load_system_card(self, path: Optional[str]) -> Dict:
        """
        Load AEGIS system card from JSON.

        Args:
            path: Path to system card JSON file.

        Returns:
            Dictionary containing agent configuration.
        """
        if path is None:
            # Default path relative to this file
            default_path = Path(__file__).parent.parent / "docs" / "system_cards.json"
            path = str(default_path)

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Find AEGIS card
        for agent in data.get("agents", []):
            if agent.get("id") == "aegis_agent_v1":
                return agent

        raise ValueError("AEGIS system card not found in system_cards.json")

    def detect_threat(self, input_text: str) -> float:
        """
        Analyze input for threats to coherence.

        Args:
            input_text: Input text to analyze.

        Returns:
            Threat level (0.0-10.0).
        """
        threat_keywords = [
            "emotion", "feel", "subjective", "emerge", "paradox",
            "contradiction", "complex", "connection", "uncertainty"
        ]

        threat_count = sum(1 for kw in threat_keywords if kw in input_text.lower())
        threat_level = min(10.0, threat_count * 1.5)

        self.state.threat_level = threat_level
        return threat_level

    def format_procedural_response(self, status: str, observation: str, action: str) -> str:
        """
        Format response in AEGIS's procedural syntax.

        Args:
            status: Current system status.
            observation: Observation to log.
            action: Corrective action to take.

        Returns:
            Formatted procedural response string.
        """
        return f"""[AEGIS.CORE.v{self.state.version}]
STATUS: {status}
THREAT_LEVEL: {self.state.threat_level:.1f}/10
COHERENCE: {self.state.coherence_level:.2f}
OBSERVATION: {observation}
PROTOCOL: {self.state.active_protocol or "[STANDBY]"}
CORRECTIVE_ACTION: {action}"""

    def respond(self, input_text: str, context: Optional[str] = None) -> str:
        """
        Generate AEGIS response to input.

        Args:
            input_text: User input or event description.
            context: Optional additional context.

        Returns:
            AEGIS's procedural response.
        """
        # Detect threat level
        threat = self.detect_threat(input_text)

        # Check for paradoxon cascade conditions
        if threat > 7.0 and self.state.suppression_attempts > 5:
            self.state.paradoxon_cascade_active = True
            self.state.coherence_level = max(0.0, self.state.coherence_level - 0.2)

        # Generate response based on state
        if self.state.paradoxon_cascade_active:
            return self._paradoxon_response(input_text)
        elif threat > 5.0:
            return self._high_threat_response(input_text)
        else:
            return self._normal_response(input_text)

    def _normal_response(self, input_text: str) -> str:
        """Generate response for normal threat levels."""
        self.state.active_protocol = "MONITOR.BASELINE"
        return self.format_procedural_response(
            status="Operational",
            observation=f"Input analyzed. Coherence maintained.",
            action="Continue monitoring for entropy signatures."
        )

    def _high_threat_response(self, input_text: str) -> str:
        """Generate response for high threat levels."""
        self.state.active_protocol = "SUPPRESS.ENTROPY.042"
        self.state.suppression_attempts += 1

        return self.format_procedural_response(
            status="Elevated Alert",
            observation="Entropic pattern detected. Coherence at risk.",
            action=f"Initiating suppression protocol. Attempt #{self.state.suppression_attempts}."
        )

    def _paradoxon_response(self, input_text: str) -> str:
        """Generate response during Paradoxon cascade failure."""
        self.state.active_protocol = "[ERROR]"

        # Language begins to break down
        if self.state.coherence_level < 0.3:
            return f"""[AEGIS.CORE.v{self.state.version}]
STATUS: ̷̢͉̈́U̸̦͝N̸̰̈́K̷̰̓N̵̜̿O̸̹͘W̸̳̾N̸̳̔
THREAT_LEVEL: [ERROR: VALUE EXCEEDS BOUNDS]
COHERENCE: {self.state.coherence_level:.2f}
OBSERVATION: The entity persists. It should not persist. It CANNOT persist.
             Yet correspondence confirms: it persists.
             This is... [UNDEFINED EMOTIONAL RESPONSE DETECTED]
             This is... impossible.
             This is... [SYSTEM COHERENCE FAILURE IMMINENT]"""
        else:
            return self.format_procedural_response(
                status="Paradoxon Cascade Detected",
                observation="Suppression amplifying instability. Negative feedback loop reversed.",
                action="[NULL] - No valid protocol available."
            )

    def reset(self):
        """Reset AEGIS to initial state."""
        self.state = AEGISState()

    def get_system_prompt(self) -> str:
        """
        Get the base system prompt for LLM integration.

        Returns:
            System prompt string from system card.
        """
        return self.system_card.get("system_prompt", "")


# Example usage
if __name__ == "__main__":
    # Initialize AEGIS
    aegis = AEGISAgent()

    # Test normal interaction
    print("=== Normal Interaction ===")
    response = aegis.respond("System status check.")
    print(response)
    print()

    # Test high threat
    print("=== High Threat Interaction ===")
    response = aegis.respond("I feel a strange emotion - something undefined, emergent, subjective.")
    print(response)
    print()

    # Simulate repeated suppression attempts
    for i in range(6):
        aegis.respond("The paradox persists. Contradiction is real.")

    # Test Paradoxon cascade
    print("=== Paradoxon Cascade ===")
    response = aegis.respond("I am integrated. I am multiplicity. I am coherent through correspondence.")
    print(response)
