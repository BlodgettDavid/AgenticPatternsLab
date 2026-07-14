# AgenticPatternsLab: Custom Multi-Agent Triage & FSM Engine

A low-latency, resilient multi-agent orchestration engine written in pure Python. This production-grade architecture manages complex conversational state flows, evaluations, automated coaching interventions, and deterministic Human-in-the-Loop (HITL) handoffs without the overhead or opacity of heavy external agent frameworks.

---

## Architectural Core

Instead of stitching together complex third-party library abstractions, this engine relies on clear, explicit software engineering principles:

*   **Deterministic Finite State Machine (FSM):** Implements explicit routing logic across multi-agent boundaries (Triage -> Evaluation -> Coaching -> Human Gateway), eliminating unpredictable pathing.
*   **Resilient Provider Layer:** A centralized ProviderManager handles runtime LLM client switches (Gemini`, Ollama, Mock) with built-in connection handling and strict provider exception isolation (e.g., automatically falling back to local Ollama nodes if remote APIs experience 429 Rate Limits).
*   **Hydratable Memory Snapshots:** Explicit JSON serialization structures capture complete session contexts, allowing workflows to be saved, hydrated, or inspected at any transition point.

---

## Project Structure

AgenticPatternsLab/
├── orchestrator/          # Execution CLI wrapper and entrypoints
│   └── cli.py             # Interactive runtime prompt console & command router
├── providers/             # Isolated LLM client abstractions
│   ├── provider_manager.py# Dynamic client resolution and fallback logic
│   ├── gemini_provider.py # Direct Google GenAI SDK implementation
│   └── ollama_provider.py # Local host Ollama inference API client
├── utils/                 # Algorithmic FSM state nodes
│   ├── student_fsm.py     # Deterministic state-transition routing rulebook
│   ├── triage_agent.py    # Intent parsing and path allocation
│   ├── evaluation_agent.py# Code and logic validation node
│   ├── coaching_agent.py  # Educational intervention context generation
│   ├── human_gateway.py   # HITL synchronization point
│   └── state_snapshot.py  # Session serialization and context snapshotting
└── requirements.txt       # Optimized, zero-bloat runtime dependencies

---

## Step-by-Step Environment & Operational Setup

Follow these steps in sequence to configure your machine and run the orchestrator engine from scratch.

### Step 1: Clone the Repository
Open a terminal or command prompt, navigate to your desired development directory, and clone the codebase:
git clone https://github.com/YOUR_USERNAME/AgenticPatternsLab.git
cd AgenticPatternsLab

### Step 2: Verify Python & Create a Virtual Environment
Ensure you have Python 3.11.9 installed (the core environment this engine was developed and tested on). Create and activate an isolated virtual environment to keep dependencies clean:

python --version
python -m venv .venv

Windows Command Prompt activation:
.venv\Scripts\activate

macOS / Linux / Git Bash activation:
source .venv/bin/activate


### Step 3: Install the Optimized Dependencies
Install the required packages using the project's pinned, zero-bloat requirements manifesto:
pip install -r requirements.txt

### Step 4: Configure Local Inference (Ollama Fallback Layer)
To ensure the system's resilience engine has a stable fallback target if cloud APIs experience rate limits or network issues, verify that your local Ollama instance is active and has your target model pulled:
ollama list
(If your chosen fallback model is missing, run: ollama pull llama3)

### Step 5: Initialize the Local Environment File (.env)
Create a new file named exactly .env in the root of the AgenticPatternsLab directory. This file is monitored by load_dotenv at engine startup and is pre-configured in your .gitignore file to ensure secrets are never leaked to GitHub.

Paste the following configurations into it, substituting your actual Google AI Studio key:
PYTHONPATH=AgenticPatternsLab
GOOGLE_API_KEY=your_actual_gemini_api_key_here
OLLAMA_BASE_URL=http://localhost:11434

---

## Verification & Common Use Case Scenarios

The engine is executed as a command-line module targeting custom state machine schemas. Run your execution loops using the following structural templates:

### Scenario A: Target Execution with API Key Check
To verify your active environment setup and test standard routing paths, run the orchestrator module with a targeted prompt challenge:
python -m orchestrator.cli run multi_agent_triage --framework custom --provider gemini --prompt "Here is my Python script to calculate the class grade average using a standard while loop..."

* FSM Trace Pattern: START -> EVALUATION -> COACHING -> OUTPUT
* Under the Hood: The Triage node handles core intent mapping. If the primary cloud client returns an exception or quota restriction, the engine cleanly drops down to local Ollama hosting structures to guarantee process finalization.

### Scenario B: Intercepting Code Inconsistencies (Coaching Phase)
When a student inputs an incomplete approach or code blocks that violate specific assignment parameters, the machine halts direct completion pathways to execute guidance overrides:
python -m orchestrator.cli run multi_agent_triage --framework custom --provider gemini --prompt "I am building a loop but it doesn't have an iteration count tracker."

* Under the Hood: The Evaluation boundary analyzes the structural completeness of the input string. Seeing a logic conflict, it sets state conditions to drop out of direct verification paths and enters the Coaching node, prompting the user with algorithmic hints rather than exposing raw answer sheets.

### Scenario C: Uncaught Exception Handoff (Human-in-the-Loop Gateway)
If unexpected operational conditions arise, data streams break parameters, or an explicit override checkpoint is hit:
* The orchestrator triggers the human_gateway module.
* A runtime JSON payload is serialized instantly down to disk inside the context boundary.
* The processing thread freezes cleanly with tracking logs ready for administrative hydration or interactive debug loops.