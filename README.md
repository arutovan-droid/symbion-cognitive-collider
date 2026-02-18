# Cognitive Collider (Symbion Space)

**Language as an Ontological Basis Switch — not a Translation Layer**

[![Medium](https://img.shields.io/badge/Medium-Read%20Article-black?logo=medium)](https://medium.com/p/de7b33b4d520)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/arutovan-droid/symbion-cognitive-collider)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green?logo=python)](https://www.python.org/)

---

## 📖 Read the full article on Medium

[**Cognitive Collider: Why AI Must Think Differently in Different Languages**](https://medium.com/p/de7b33b4d520)

*An introduction to the philosophy and architecture behind the Cognitive Collider, with test results and cultural analysis.*

---

Cognitive Collider is a core module of Symbion Space that treats language as an active operator of thought, not merely a medium of output.

An AI does not think the same way in different languages.
Language reshapes ontology, causality, abstraction, and depth.

Cognitive Collider formalizes this effect and makes it reproducible.

---

## 📋 TL;DR

- `prompt_language`: detected language of the user prompt
- `think_language`: chosen cognitive basis for reasoning (**ontology switch**)
- `output_language`: always the user language
- Optional **collision mode**: two cognitive poles + synthesis arbiter
- Integrates **before PSL** (verification/constraints layer) and before downstream generation

---

## 🧪 Tested Cognitive Profiles

The system successfully distinguishes between:

| Language | Cognitive Role | Recognized In |
|----------|----------------|---------------|
| `hy` (Armenian) | Existential continuity | Narekatsi indictment |
| `zh` (Chinese) | Strategy | Crisis decision-making |
| `sa` (Sanskrit) | Pure logic | Nyaya/Samkhya ontology |
| `arc` (Aramaic) | Sacral substrate | Light without shadow |
| `el` (Greek) | Dialectics | Unprovable truth |
| `ru` (Russian) | Psycho-realism | Narekatsi + conscience |

---

## 🔬 Validation Tests

All epistemological tests pass:

```python
# Test 1: Sacral Light → arc + hy
# Test 2: Unprovable Truth → sa + el (arc, hy in top3)
# Test 3: Crisis → zh (collision not required)
# Test 4: Narekatsi → hy + ru (not arc!)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m symbion_cognitive_collider route "Что такое истина?" --energy 0.95
symbion-cognitive-collider/
├── src/
│   └── symbion_cognitive_collider/
│       ├── collider.py          # Main router
│       ├── lop.py                # Language Ontology Profiler
│       ├── apostles.py           # 12 cognitive profiles
│       └── schemas.py             # Pydantic models
├── tools/
│   ├── demo_examples.py          # Live demos
│   ├── web_fastapi.py             # Web UI
│   └── smoke_router.py            # Smoke tests
├── tests/
│   ├── test_arc.py
│   ├── test_truth.py
│   └── test_epistemological_nuance_fixed4.py
├── README.md
└── pyproject.toml
Resonance Matrix
🔹 Light Without Shadow (Sacral)

Pole A: arc (sacral substrate)

Pole B: hy (survival/testimony)

Philosophy: Light as grace + light as memory

🔹 Unprovable Truth (Epistemology)

Pole A: sa (logic/limits)

Pole B: el (dialectics/aporia)

Also in top 3: arc, hy

Philosophy: Structure of knowledge + limits of rationality

🔹 Crisis (Strategy)

Pole A: zh (危机 = danger+opportunity)

Pole B: — (collision not required)

Philosophy: Pure strategy, internal dialectics

🔹 Narekatsi (Existential Conflict)

Pole A: hy (aybuben/indictment)

Pole B: ru (psycho-realism/conscience)

Philosophy: Armenian tragedy + Russian depth of soul

🧠 Core Thesis
Intelligence is not only about models and parameters.
It is about which cognitive substrate is activated for a given problem.

Cognitive Collider turns human linguistic history into an operational component of artificial intelligence.

This is not translation. This is thinking.

📚 Further Reading
Medium Article: Cognitive Collider

Symbion Space (coming soon)

📄 License
MIT License — see LICENSE file.

🔗 GitHub Repository:
github.com/arutovan-droid/symbion-cognitive-collider

Code, tests, and documentation are available for anyone who wants to hear the sound between the notes.
