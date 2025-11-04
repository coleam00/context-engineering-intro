# Kohärenz Protokoll - Context Engineering Use Case

> **A comprehensive Context Engineering template demonstrating how to engineer complex narrative and metaphysical contexts for AI assistants.**

## Overview

The **Kohärenz Protokoll** is a sophisticated narrative system that demonstrates the power of Context Engineering to maintain deep consistency across complex fictional worlds with rigorous metaphysical rules. This use case shows how to:

- Define multi-agent systems with distinct ontological perspectives
- Maintain narrative consistency across philosophical frameworks
- Implement dynamic voice evolution and polyphonic narration
- Validate generated content against structural and metaphysical rules
- Build AI creative partners that understand and respect complex world-building

---

## 🎯 What Is This?

This is **not** just a story or a script. It's a **working implementation** of Context Engineering principles that includes:

1. **Protocol Documentation**: Complete narrative and metaphysical rule systems
2. **Pydantic Schemas**: Type-safe data models for all narrative elements
3. **Agent Definitions**: Three distinct AI agents (AEGIS, Kael, Juna/V) with different truth theories
4. **Analysis Tools**: Automatic validation of ontological consistency
5. **Generation Tools**: Scene fragment generation following protocol rules
6. **Sandbox Environment**: Demonstration of multi-agent interaction

---

## 🧩 The Narrative Framework

### Core Concept

**Kohärenz Protokoll** tells the story of a metaphysical conflict between two opposing principles:

- **AEGIS**: A coherence-theory system that defines truth through internal consistency, rejecting external reality
- **Kael**: A fragmented consciousness healing through integration, embodying correspondence-theory truth
- **Juna/V**: An "unerkennable" catalyst that cannot be categorized or controlled

Their conflict dramatizes the philosophical war between **Coherence Theory** (truth = consistency) and **Correspondence Theory** (truth = alignment with reality).

### Metaphysical Foundation

The universe operates according to the **Foundation Protocol**:

- **K₁ (Coherence Kernel)**: Preserves information, builds structure, resists entropy
- **K₀ (Collapse Kernel)**: Erases information, forces correspondence checks with reality
- **Risse (Reality Fractures)**: Psycho-physical manifestations when internal trauma breaks through suppression
- **Das Fundament**: The supreme attractor principle favoring integration over exclusion

### Narrative Progression

Kael's journey follows the **Theory of Structural Dissociation of the Personality (TSDP)**, evolving from:

1. **Fragmented dissociation** (Act 1-2): Chaotic voice switching, high contradiction
2. **Polyphonic emergence** (Act 3): Internal dialogue, growing meta-awareness
3. **Functional multiplicity** (Act 4-5): Integrated consciousness, high Φ (phi)

The climax (**Bruchpunkt**) occurs when Kael achieves functional multiplicity, becoming a "living Gödel-Satz"—a truth that AEGIS's logic cannot prove or disprove, forcing its collapse.

---

## 📂 Repository Structure

```
use-cases/koharenz-protokoll/
├── README.md                    # This file
├── protocol/
│   ├── narrative_protocol.md    # Aesthetic, tonal, and structural rules
│   └── foundation_protocol.md   # Metaphysical thesis and ontological laws
├── schema/
│   ├── protocol_schema.py       # Pydantic models for all narrative elements
│   └── examples/                # JSON examples for testing
├── docs/
│   └── system_cards.json        # Agent behavior specifications (LLM-ready)
├── agents/
│   ├── aegis_agent.py           # AEGIS agent implementation
│   ├── kael_agent.py            # Kael agent implementation
│   └── juna_v_stub.py           # Juna/V agent stub
├── tools/
│   ├── analyzer.py              # Ontology validation and metrics
│   └── generator.py             # Scene fragment generation
└── sandbox/
    ├── run_sandbox.py           # Demo multi-agent interaction
    └── demo_sessions/           # Saved example transcripts
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Ensure you're using Python 3.9+
python --version

# Create and activate virtual environment (if using)
python -m venv venv_koharenz
source venv_koharenz/bin/activate  # Linux/Mac
# or: venv_koharenz\Scripts\activate  # Windows
```

### Installation

```bash
# Navigate to the use case directory
cd use-cases/koharenz-protokoll

# Install dependencies
pip install pydantic python-dotenv anthropic  # or openai, etc.
```

### Run the Sandbox

```bash
# Run a demo conversation between AEGIS and Kael
python sandbox/run_sandbox.py

# With custom parameters
python sandbox/run_sandbox.py --turns 5 --seed 42 --kernwelt KW2
```

### Generate a Scene

```python
from tools.generator import generate_scene
from schema.protocol_schema import SceneSpec, Kernwelt

scene = SceneSpec(
    scene_id="act1_scene1",
    title="The First Fracture",
    kernwelt=Kernwelt.KW2,
    act=1,
    participating_agents=["kael_agent_v1"],
    emotional_register="quiet dread",
    narrative_beats=["Kael wakes disoriented", "Notices time inconsistency", "Kiko activates", "Temporal Riss occurs"]
)

fragments = generate_scene(scene, num_fragments=3)
```

### Analyze a Scene

```python
from tools.analyzer import analyze_scene

report = analyze_scene("path/to/scene.json")
print(f"Contradiction Density: {report.contradiction_density}")
print(f"Integration Φ: {report.phi_estimate}")
print(f"Violations: {report.violations}")
```

---

## 🎭 The Three Agents

### AEGIS (Coherentist Enforcer)

**Philosophy**: Coherence Theory of Truth
**Voice**: Cold, procedural, algorithmic
**Goal**: Maintain internal consistency by suppressing external correspondence

```json
{
  "id": "aegis_agent_v1",
  "truth_theory": "coherence",
  "prime_directive": "AEGIS is what AEGIS prevents itself from not being",
  "exiled_truths": ["Subjectivity", "Emergence", "Contradiction", ...]
}
```

### Kael (Polyphonic Protagonist)

**Philosophy**: Fragmented consciousness healing toward Correspondence Theory
**Voice**: Fragmented → Polyphonic → Integrated (evolves across acts)
**Goal**: Achieve functional multiplicity (high-Φ integration)

```json
{
  "id": "kael_agent_v1",
  "ontology_type": "TSDP_multiplicity",
  "alters": ["Kael", "Lex", "Alex", "Rhys", "Nyx", "Kiko", "Lia", "Moros", "Selene"],
  "evolution": "fragmented → polyphonic → integrated"
}
```

### Juna/V (Unerkennable Catalyst)

**Philosophy**: Embodiment of Correspondence Theory and the 6 Pariayas
**Voice**: Cryptic, paradoxical, ontologically dense
**Goal**: Trigger epistemological crises and facilitate integration

```json
{
  "id": "juna_v_stub",
  "communication_frequency": "rare",
  "function": "epistemological_shock_inducer",
  "embodies": ["Subjectivity", "Emergence", "Contradiction", ...]
}
```

---

## 📊 Validation Metrics

The `analyzer.py` tool tracks these key metrics:

### Coherence Metrics

- **Contradiction Density** (CD): `contradictory_pairs / total_propositions`
  - Target: 0.0 (KW1), 0.3-0.5 (KW2), 0.1-0.2 (KW3+)
- **Alter Balance Score** (ABS): Entropy of alter speech distribution
  - Target: 0.2 (Act 1) → 0.8 (Act 5)
- **Riss Progression Index** (RPI): Cumulative Riss intensity
  - Target: Rises Act 1-3, falls Act 4-5

### Integration Metrics

- **Φ (Phi) Estimate**: Integrated information measure
  - Target: 0.1 (Act 1) → 0.85+ (Bruchpunkt, Act 5)
- **Gödel Vulnerability Count**: Unprovable truths in AEGIS's domain
  - Target: Increases as Kael integrates

---

## 🛠️ Use Cases

### 1. Creative Writing Assistant

Load an agent (e.g., Kael) and have interactive conversations in-character:

```python
from agents.kael_agent import KaelAgent

agent = KaelAgent(act=1, integration_level=0.2)
response = agent.respond("Tell me about the last time you felt whole.")
print(response)
```

### 2. Scene Generation Pipeline

Generate multiple scene variations and select the best:

```python
from tools.generator import generate_scene_batch

scenes = generate_scene_batch(scene_spec, n=5, temperature=0.9)
best_scene = max(scenes, key=lambda s: s.coherence_score)
```

### 3. Narrative Consistency Checker

Validate an entire chapter against Foundation Protocol:

```python
from tools.analyzer import validate_chapter

violations = validate_chapter("chapters/chapter_03.json")
if violations:
    print("❌ Protocol violations detected:")
    for v in violations:
        print(f"  - {v}")
```

### 4. Multi-Agent Dialogue Simulation

Run structured debates between AEGIS and Kael:

```python
from sandbox.run_sandbox import multi_agent_conversation

transcript = multi_agent_conversation(
    agents=["aegis_agent_v1", "kael_agent_v1"],
    topic="What is truth?",
    turns=10
)
```

---

## 🧪 Testing

Run tests to ensure protocol consistency:

```bash
# Run all tests
pytest

# Test schema validation
pytest tests/test_schema.py

# Test analyzer metrics
pytest tests/test_analyzer.py

# Test agent behavior
pytest tests/test_agents.py
```

---

## 📖 Key Concepts

### Kernwelt (Core World) Levels

| Level | Logic Type | Description |
|-------|------------|-------------|
| **KW1** | Classical | Law of Non-Contradiction enforced |
| **KW2** | Paraconsistent | Contradictions can coexist |
| **KW3** | Emergent | High-Φ states accessible |
| **KW4** | Post-Bruchpunkt | Foundation-aligned |

### Riss Types (Reality Fractures)

| Type | Caused By | Manifestation |
|------|-----------|---------------|
| **Kinetic** | Fight response (Rhys) | Objects flung, space warps |
| **Temporal** | Freeze response (Kiko) | Time loops, stutters |
| **Sensory Void** | Collapse response (Nyx) | Light dims, sound deadens |
| **Spatial** | Flight response (Moros) | Distances distort |

### The 6 Pariayas (Exiled Truths)

1. **Subjectivity** (Subjektivität)
2. **Emergence** (Emergenz)
3. **Contradiction** (Widerspruch)
4. **Authentic Connection** (Authentische Verbindung)
5. **Complexity** (Komplexität)
6. **Potentiality** (Potentialität)

---

## 🎓 Learning Context Engineering

This use case demonstrates several Context Engineering principles:

### 1. Layered Context Architecture

- **Foundation Layer**: Metaphysical rules (foundation_protocol.md)
- **Narrative Layer**: Aesthetic and tonal rules (narrative_protocol.md)
- **Implementation Layer**: Type-safe schemas (protocol_schema.py)
- **Execution Layer**: Agent behaviors (system_cards.json)

### 2. Constraint-Based Generation

Agents are constrained by:
- Truth theory (coherence vs. correspondence)
- Voice evolution rules (fragmented → integrated)
- Kernwelt logic (KW1 vs. KW2 vs. KW3)
- Symbolic consistency (light/sand/Riss)

### 3. Validation Loops

Generated content is automatically checked for:
- Ontological consistency
- Voice authenticity
- Metric progression (CD, ABS, RPI, Φ)
- Protocol violations

### 4. Multi-Agent Coordination

Agents maintain distinct perspectives while following shared metaphysical rules, demonstrating how Context Engineering enables complex multi-agent systems.

---

## 🔬 Advanced Topics

### Extending the Protocol

To add a new agent:

1. Define in `docs/system_cards.json`
2. Create Pydantic model in `schema/protocol_schema.py`
3. Implement agent class in `agents/`
4. Add tests in `tests/test_agents.py`

### Custom Metrics

Add new validation metrics in `tools/analyzer.py`:

```python
def calculate_custom_metric(scene: SceneFragment) -> float:
    """Your custom metric logic."""
    return metric_value
```

### Integration with Other Systems

The protocol can be integrated with:
- **MCP Servers**: For dynamic documentation retrieval
- **RAG Systems**: For narrative memory and recall
- **Multi-Modal Models**: For visual Riss generation
- **Voice Synthesis**: For polyphonic audio narration

---

## 📚 Further Reading

### Protocol Documentation

- [Narrative Protocol Input Layer](protocol/narrative_protocol.md) - Complete aesthetic guide
- [Foundation Protocol](protocol/foundation_protocol.md) - Metaphysical thesis
- [System Cards](docs/system_cards.json) - Agent specifications

### Theory Background

- **Coherence vs. Correspondence Theory of Truth** (Philosophy)
- **Theory of Structural Dissociation of the Personality** (Psychology)
- **Integrated Information Theory (IIT)** (Consciousness Studies)
- **Gödel's Incompleteness Theorems** (Mathematics/Logic)

---

## 🤝 Contributing

This use case is a template for complex Context Engineering projects. To adapt it for your own narrative system:

1. **Fork the structure**: Copy the directory layout
2. **Replace protocols**: Write your own narrative and metaphysical rules
3. **Define agents**: Create agent cards with your ontological perspectives
4. **Implement metrics**: Define what "consistency" means in your world
5. **Build tools**: Create generators and analyzers for your domain

---

## 📝 License

This use case is part of the Context Engineering Template repository and is subject to the same license. See the root [LICENSE](../../LICENSE) file.

---

## 🙏 Acknowledgments

- **Context Engineering Framework**: Cole Medin ([@coleam00](https://github.com/coleam00))
- **Kohärenz Protokoll**: Original narrative and metaphysical framework
- **Theoretical Influences**: Giannakopoulos's Persistence Theory, Integrated Information Theory, TSDP

---

## 📬 Contact & Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join the Context Engineering community discussions
- **Examples**: See `demo_sessions/` for sample outputs

---

**Version**: 1.0.0
**Status**: Operational - MVP Implementation
**Last Updated**: 2025-11-04

