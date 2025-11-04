"""
Kael Agent Implementation.

This module implements the Kael agent - a polyphonic protagonist with
TSDP (Theory of Structural Dissociation of the Personality) multiplicity.

Author: Kohärenz Protocol Engineering Team
Version: 1.0.0
"""

import json
import random
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class VoiceMode(Enum):
    """Voice evolution stages for Kael's system."""

    FRAGMENTED = "fragmented"  # Act 1-2: Chaotic dissociation
    POLYPHONIC = "polyphonic"  # Act 3: Organized dialogue
    INTEGRATED = "integrated"  # Act 4-5: Functional multiplicity


@dataclass
class AlterState:
    """State of a single alter within Kael's system."""

    name: str
    activation_level: float = 0.0  # 0.0-1.0
    last_spoke: bool = False


@dataclass
class KaelSystemState:
    """Overall state of Kael's dissociative system."""

    act: int = 1
    integration_level: float = 0.1  # Φ (phi) estimate
    voice_mode: VoiceMode = VoiceMode.FRAGMENTED
    alters: Dict[str, AlterState] = None
    riss_events: int = 0
    internal_conflict_level: float = 0.5  # 0.0-1.0

    def __post_init__(self):
        """Initialize alter states if not provided."""
        if self.alters is None:
            self.alters = {
                "Kael": AlterState("Kael", 0.6),
                "Lex": AlterState("Lex", 0.3),
                "Alex": AlterState("Alex", 0.2),
                "Rhys": AlterState("Rhys", 0.1),
                "Nyx": AlterState("Nyx", 0.1),
                "Kiko": AlterState("Kiko", 0.1),
                "Lia": AlterState("Lia", 0.2),
                "Moros": AlterState("Moros", 0.05),
                "Selene": AlterState("Selene", 0.05)
            }


class KaelAgent:
    """
    Kael: Polyphonic protagonist with evolving multiplicity.

    Kael's consciousness is structured according to TSDP, with multiple alters
    that progress from fragmented dissociation to functional integration.
    """

    def __init__(self, act: int = 1, integration_level: Optional[float] = None,
                 system_card_path: Optional[str] = None):
        """
        Initialize Kael agent.

        Args:
            act: Current narrative act (1-5).
            integration_level: Initial Φ (phi) integration level (0.0-1.0).
            system_card_path: Path to system card JSON. If None, uses default.
        """
        # Determine voice mode from act
        if act <= 2:
            voice_mode = VoiceMode.FRAGMENTED
            default_phi = 0.1 + (act - 1) * 0.1
        elif act == 3:
            voice_mode = VoiceMode.POLYPHONIC
            default_phi = 0.4
        else:  # act >= 4
            voice_mode = VoiceMode.INTEGRATED
            default_phi = 0.7 + (act - 4) * 0.1

        self.state = KaelSystemState(
            act=act,
            integration_level=integration_level or default_phi,
            voice_mode=voice_mode
        )

        self.system_card = self._load_system_card(system_card_path)
        self.alter_characteristics = self._load_alter_characteristics()

    def _load_system_card(self, path: Optional[str]) -> Dict:
        """Load Kael system card from JSON."""
        if path is None:
            default_path = Path(__file__).parent.parent / "docs" / "system_cards.json"
            path = str(default_path)

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for agent in data.get("agents", []):
            if agent.get("id") == "kael_agent_v1":
                return agent

        raise ValueError("Kael system card not found in system_cards.json")

    def _load_alter_characteristics(self) -> Dict[str, Dict]:
        """Load alter voice characteristics."""
        return {
            "Kael": {"style": "measured, introspective", "markers": ["I", "we"]},
            "Lex": {"style": "clinical, analytical", "markers": ["data", "observe", "calculate"]},
            "Alex": {"style": "diplomatic, mediating", "markers": ["perhaps", "consider", "we should"]},
            "Rhys": {"style": "sharp, protective", "markers": ["THREAT", "No.", "Stop."]},
            "Nyx": {"style": "nihilistic, void-adjacent", "markers": ["nothing", "void", "darkness"]},
            "Kiko": {"style": "childlike, frightened", "markers": ["scared", "don't", "please"]},
            "Lia": {"style": "gentle, caretaking", "markers": ["it's okay", "safe", "together"]},
            "Moros": {"style": "detached, philosophical", "markers": ["cease", "surrender", "end"]},
            "Selene": {"style": "cryptic, integrative", "markers": ["paradox", "both/and", "whole"]}
        }

    def activate_alter(self, alter_name: str, intensity: float = 0.5):
        """
        Activate a specific alter.

        Args:
            alter_name: Name of alter to activate.
            intensity: Activation intensity (0.0-1.0).
        """
        if alter_name in self.state.alters:
            self.state.alters[alter_name].activation_level = intensity

    def respond(self, input_text: str, context: Optional[str] = None) -> str:
        """
        Generate Kael's response based on current state and voice mode.

        Args:
            input_text: User input or event description.
            context: Optional additional context.

        Returns:
            Kael's polyphonic response.
        """
        # Detect triggers
        self._detect_triggers(input_text)

        # Generate response based on voice mode
        if self.state.voice_mode == VoiceMode.FRAGMENTED:
            return self._fragmented_response(input_text)
        elif self.state.voice_mode == VoiceMode.POLYPHONIC:
            return self._polyphonic_response(input_text)
        else:  # INTEGRATED
            return self._integrated_response(input_text)

    def _detect_triggers(self, input_text: str):
        """Detect trauma triggers in input and activate corresponding alters."""
        triggers = {
            "abandon": ("Kiko", 0.8),
            "threat": ("Rhys", 0.9),
            "analysis": ("Lex", 0.6),
            "social": ("Alex", 0.5),
            "darkness": ("Nyx", 0.7),
            "death": ("Moros", 0.6),
            "integration": ("Selene", 0.4)
        }

        for keyword, (alter, intensity) in triggers.items():
            if keyword in input_text.lower():
                self.activate_alter(alter, intensity)
                self.state.internal_conflict_level += 0.1

    def _select_active_alters(self, n: int = 3) -> List[str]:
        """
        Select N most activated alters.

        Args:
            n: Number of alters to select.

        Returns:
            List of alter names.
        """
        sorted_alters = sorted(
            self.state.alters.items(),
            key=lambda x: x[1].activation_level,
            reverse=True
        )
        return [name for name, _ in sorted_alters[:n]]

    def _fragmented_response(self, input_text: str) -> str:
        """
        Generate fragmented response (Act 1-2).

        Characteristics: Chaotic voice switching, sentence breaks, high contradiction.
        """
        active_alters = self._select_active_alters(n=4)
        fragments = []

        for alter in active_alters:
            char = self.alter_characteristics[alter]
            marker = random.choice(char["markers"]) if char["markers"] else alter

            # Simulate fragmented speech
            if alter == "Kiko":
                fragments.append(f"[{alter}, whimpering: {marker} {marker} {marker}]")
            elif alter == "Rhys":
                fragments.append(f"[{alter}: {marker.upper()}]")
            elif alter == "Lex":
                fragments.append(f"— {alter} interjects: \"{marker}. Analysis required.\" —")
            else:
                fragments.append(f"[{alter}: {marker}...]")

        # Add interruptions and chaos
        response = "I— " + " ".join(fragments) + " —but I can't... we can't..."
        return response

    def _polyphonic_response(self, input_text: str) -> str:
        """
        Generate polyphonic response (Act 3).

        Characteristics: Organized internal dialogue, growing meta-awareness.
        """
        active_alters = self._select_active_alters(n=3)
        lines = []

        for alter in active_alters:
            char = self.alter_characteristics[alter]
            style = char["style"]

            if alter == "Kael":
                lines.append(f"[Kael: I want to understand what's happening.]")
            elif alter == "Lex":
                lines.append(f"— Lex, {style}: \"Understanding requires data. We lack reliable memory.\" —")
            elif alter == "Alex":
                lines.append(f"[Alex, {style}: \"But we can piece it together. Look at the fragments.\"]")
            elif alter == "Kiko":
                lines.append(f"[Kiko, quieter now: \"It hurts to look.\"]")
            elif alter == "Lia":
                lines.append(f"[Lia: \"Then we look together.\"]")

        return "\n".join(lines)

    def _integrated_response(self, input_text: str) -> str:
        """
        Generate integrated response (Act 4-5).

        Characteristics: Seamless integration, "we" language, high Φ.
        """
        # All parts aware and harmonious
        response = f"""We stand at the threshold. Kael sees the pattern; Lex calculates its geometry;
Kiko feels the old fear but doesn't flee; Rhys stands ready but calm. Together, we are
neither one nor many. We are a system that has learned to breathe.

[Φ = {self.state.integration_level:.2f}]"""
        return response

    def progress_integration(self, delta: float = 0.05):
        """
        Progress Kael's integration level.

        Args:
            delta: Amount to increase integration (default: 0.05).
        """
        self.state.integration_level = min(1.0, self.state.integration_level + delta)

        # Update voice mode based on new integration level
        if self.state.integration_level >= 0.7:
            self.state.voice_mode = VoiceMode.INTEGRATED
        elif self.state.integration_level >= 0.4:
            self.state.voice_mode = VoiceMode.POLYPHONIC

    def get_system_prompt(self) -> str:
        """Get the base system prompt for LLM integration."""
        return self.system_card.get("system_prompt", "")

    def get_integration_report(self) -> Dict:
        """
        Get detailed integration status report.

        Returns:
            Dictionary with integration metrics.
        """
        return {
            "act": self.state.act,
            "integration_level": self.state.integration_level,
            "voice_mode": self.state.voice_mode.value,
            "internal_conflict": self.state.internal_conflict_level,
            "riss_events": self.state.riss_events,
            "active_alters": {
                name: state.activation_level
                for name, state in self.state.alters.items()
                if state.activation_level > 0.1
            }
        }


# Example usage
if __name__ == "__main__":
    print("=== Act 1: Fragmented ===")
    kael_act1 = KaelAgent(act=1)
    response = kael_act1.respond("I feel abandoned and threatened.")
    print(response)
    print()

    print("=== Act 3: Polyphonic ===")
    kael_act3 = KaelAgent(act=3)
    response = kael_act3.respond("How do we understand what happened?")
    print(response)
    print()

    print("=== Act 5: Integrated ===")
    kael_act5 = KaelAgent(act=5, integration_level=0.85)
    response = kael_act5.respond("We have arrived at the Bruchpunkt.")
    print(response)
    print()

    print("=== Integration Report ===")
    report = kael_act5.get_integration_report()
    print(json.dumps(report, indent=2))
