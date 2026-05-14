# 🤖 Claudy AI Team (Agent Orchestration System)

> A robust, interactive Python-based AI orchestration framework powered by Claude 3.5 Sonnet.

Claudy AI Team is a multi-agent system designed to streamline the software development lifecycle. At its core is **Claudy**, the intelligent Orchestrator Agent, who delegates tasks to a specialized team of AI sub-agents (Frontend, Backend, DevOps, QA, Security, etc.) based on user requests.

---

## 🌟 Key Features
- **Centralized Orchestration:** "Claudy" acts as your personal AI project manager, delegating tasks to the appropriate specialized agents.
- **Role-Based AI Sub-Agents:** 9 pre-configured specialized agents, including Frontend, Backend, Database, QA, Security, Code Review, Docs Writer, Research, and DevOps.
- **Interactive CLI Interface:** A beautiful, responsive command-line interface powered by `Rich` for seamless communication.
- **Prompt Engineering Driven:** All agents are driven by isolated, easily modifiable markdown prompt templates.
- **Cost Tracking & Logging:** Built-in token usage logging system (JSONL format) to monitor Anthropic API costs.

---

## 🏗️ Architecture

```text
claudy-ai-team/
├── src/
│   ├── claudy.py       # Orchestrator Logic (Main Entry Point)
│   ├── agent.py        # Base Agent Class (Anthropic API Integration)
│   ├── cli.py          # Interactive Terminal Interface
│   └── test_setup.py   # System Health Check
├── prompts/            # System Prompts for Agents
│   ├── claudy_system_prompt.md
│   ├── agent_communication_protocol.md
│   └── agents/         # Specialized Sub-Agent Prompts
│       ├── 01_frontend_agent_system_prompt.md
│       ├── 02_backend_agent_system_prompt.md
│       ├── 03_database_agent_system_prompt.md
│       ├── 04_devops_agent_system_prompt.md
│       ├── 05_qa_testing_agent_system_prompt.md
│       ├── 06_security_agent_system_prompt.md
│       ├── 07_code_review_agent_system_prompt.md
│       ├── 08_docs_writer_agent_system_prompt.md
│       └── 09_research_agent_system_prompt.md
├── logs/               # Token usage & Request logs
├── .env                # Environment Variables (Ignored in Git)
├── requirements.txt    # Python Dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Anthropic API Key (with available prepaid credits)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/chopchobs/Claudy-ai-team.git
   cd claudy-ai-team
   ```

2. **Set up the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup:**
   Create a `.env` file in the root directory and add your Anthropic API Key:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-...
   CLAUDE_MODEL=claude-3-5-sonnet-20241022
   ```

---

## 💻 Usage

### 1. Test the Setup
To verify that your API key is working and the orchestration system is configured correctly:
```bash
python src/test_setup.py
```

### 2. Start the Interactive CLI
Launch the AI Team environment:
```bash
python src/cli.py
```

**Available CLI Commands:**
- `/delegate <agent> <task>`: Directly delegate a specific task to an agent (e.g., `/delegate frontend Build a React Login Form`)
- `/agents`: List all available specialized agents.
- `/reset`: Clear the current conversation history and start fresh.
- `/quit`: Exit the system.

---

## 💰 Cost Optimization (API Pricing Estimate)

This project uses the Anthropic API (Pay-As-You-Go).
Average estimated cost per run/task using `claude-3-5-sonnet-20241022`:
- **Simple chat**: ~$0.02
- **Feature planning**: ~$0.05
- **Code generation**: ~$0.15
- **Deep research**: ~$0.30

*Note: Running terminal commands, activating `venv`, or viewing logs does NOT consume any API credits. Credits are only deducted when you send a prompt via the CLI interface.*

---

## 🛠️ Tech Stack
- **Language:** Python 3.9+
- **LLM Provider:** [Anthropic SDK](https://docs.anthropic.com/) (Claude 3.5 Sonnet)
- **UI:** [Rich](https://rich.readthedocs.io/) (for terminal aesthetics)
- **Config Management:** `python-dotenv`

---

## 🔒 Security & Best Practices
- **API Keys are not tracked:** The `.env` file is strictly ignored via `.gitignore` to prevent secret leaks.
- **Virtual Environment Excluded:** The `venv/` directory is ignored to keep the repository lightweight.
- **Local Logging:** All token usage logs are saved locally in the `logs/` directory and are not pushed to the repository.
