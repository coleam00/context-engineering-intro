#!/usr/bin/env python3
"""
Kohärenz Protocol Sandbox - Multi-Agent Interaction Demo.

This script demonstrates the interaction between AEGIS, Kael, and Juna/V
agents following the Foundation Protocol and Narrative Protocol rules.

Usage:
    python run_sandbox.py --turns 5 --seed 42 --act 3

Author: Kohärenz Protocol Engineering Team
Version: 1.0.0
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.kael_agent import KaelAgent
from agents.aegis_agent import AEGISAgent
from agents.juna_v_stub import JunaVAgent


class SandboxSession:
    """Manages a multi-agent conversation session."""

    def __init__(self, act: int = 1, seed: int = None):
        """
        Initialize sandbox session.

        Args:
            act: Current narrative act (1-5).
            seed: Random seed for deterministic behavior.
        """
        self.act = act
        self.kael = KaelAgent(act=act)
        self.aegis = AEGISAgent()
        self.juna = JunaVAgent()
        self.conversation_log = []

        if seed is not None:
            import random
            random.seed(seed)

    def run_dialogue(self, topic: str, turns: int = 5) -> List[Dict]:
        """
        Run a multi-turn dialogue between agents.

        Args:
            topic: Conversation topic or prompt.
            turns: Number of conversation turns.

        Returns:
            List of conversation turns.
        """
        print(f"\n{'='*70}")
        print(f"  KOHÄRENZ PROTOCOL SANDBOX - Act {self.act}")
        print(f"  Topic: {topic}")
        print(f"  Turns: {turns}")
        print(f"{'='*70}\n")

        # Initial setup
        context = topic

        for turn_num in range(1, turns + 1):
            print(f"\n--- Turn {turn_num}/{turns} ---\n")

            # Kael speaks
            kael_response = self.kael.respond(context)
            self._log_turn(turn_num, "Kael", kael_response)
            print(f"[Kael]")
            print(kael_response)
            print()

            # AEGIS responds to Kael
            aegis_response = self.aegis.respond(kael_response)
            self._log_turn(turn_num, "AEGIS", aegis_response)
            print(f"[AEGIS]")
            print(aegis_response)
            print()

            # Occasionally, Juna/V interjects
            juna_response = self.juna.respond(context=context)
            if juna_response:
                self._log_turn(turn_num, "Juna/V", juna_response)
                print(f"[Juna/V]")
                print(juna_response)
                print()

            # Update context for next turn
            context = self._summarize_turn(kael_response, aegis_response)

        print(f"\n{'='*70}")
        print(f"  SESSION COMPLETE")
        print(f"{'='*70}\n")

        return self.conversation_log

    def _log_turn(self, turn: int, speaker: str, content: str):
        """Log a conversation turn."""
        self.conversation_log.append({
            "turn": turn,
            "speaker": speaker,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def _summarize_turn(self, kael_msg: str, aegis_msg: str) -> str:
        """Summarize turn for context."""
        # Simple heuristic: use last sentence of each
        kael_last = kael_msg.split(".")[-2] if "." in kael_msg else kael_msg[:50]
        aegis_last = aegis_msg.split("\n")[-1] if "\n" in aegis_msg else aegis_msg[:50]

        return f"Kael expressed: {kael_last}. AEGIS responded with: {aegis_last}"

    def save_transcript(self, filename: str):
        """
        Save conversation transcript to file.

        Args:
            filename: Output filename.
        """
        output_path = Path(__file__).parent / "demo_sessions" / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"KOHÄRENZ PROTOCOL SANDBOX TRANSCRIPT\n")
            f.write(f"Act: {self.act}\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"{'='*70}\n\n")

            for entry in self.conversation_log:
                f.write(f"--- Turn {entry['turn']} - {entry['speaker']} ---\n")
                f.write(f"{entry['content']}\n\n")

            f.write(f"{'='*70}\n")
            f.write(f"END TRANSCRIPT\n")

        print(f"✓ Transcript saved to: {output_path}")

    def get_metrics(self) -> Dict:
        """
        Get session metrics.

        Returns:
            Dictionary of session metrics.
        """
        return {
            "act": self.act,
            "total_turns": len(self.conversation_log) // 3,  # Approx
            "kael_integration": self.kael.state.integration_level,
            "aegis_coherence": self.aegis.state.coherence_level,
            "aegis_threat_level": self.aegis.state.threat_level,
            "paradoxon_active": self.aegis.state.paradoxon_cascade_active,
            "juna_appearances": self.juna.state.appearances_this_act
        }


def main():
    """Main entry point for sandbox."""
    parser = argparse.ArgumentParser(
        description="Kohärenz Protocol Sandbox - Multi-Agent Demo"
    )
    parser.add_argument(
        "--act",
        type=int,
        default=3,
        choices=[1, 2, 3, 4, 5],
        help="Narrative act (1-5). Affects Kael's integration level."
    )
    parser.add_argument(
        "--turns",
        type=int,
        default=5,
        help="Number of conversation turns."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for deterministic behavior."
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="What is the nature of truth?",
        help="Conversation topic/prompt."
    )
    parser.add_argument(
        "--save",
        type=str,
        default=None,
        help="Save transcript to file (e.g., 'session_001.txt')."
    )

    args = parser.parse_args()

    # Create session
    session = SandboxSession(act=args.act, seed=args.seed)

    # Run dialogue
    session.run_dialogue(topic=args.topic, turns=args.turns)

    # Print metrics
    print("\n=== Session Metrics ===")
    metrics = session.get_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Save transcript if requested
    if args.save:
        session.save_transcript(args.save)
    else:
        # Auto-save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session.save_transcript(f"sandbox_act{args.act}_{timestamp}.txt")


if __name__ == "__main__":
    main()
