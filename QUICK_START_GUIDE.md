# 🚀 Claudy AI Team — Quick Start Guide
## Deploy Multi-Agent System with Anthropic API + Claude Code

> **Target:** Solo Developer using Anthropic API + Claude Code
> **Time to first run:** ~30 minutes
> **Skill required:** Basic Python/Node.js, terminal familiarity
> **Cost estimate:** ~$5-20/month for personal use

---

## 📋 TABLE OF CONTENTS

1. [What You're Building](#what-youre-building)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Configure Claudy + Agents](#configure-claudy--agents)
5. [Run Your First Task](#run-your-first-task)
6. [Daily Workflow](#daily-workflow)
7. [Real-World Examples](#real-world-examples)
8. [Cost Optimization](#cost-optimization)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## 🎯 WHAT YOU'RE BUILDING

ระบบ Multi-Agent ที่ทำงานเป็นทีมให้คุณ — แทนที่จะคุยกับ Claude ทีละครั้ง คุณจะมี

```
        คุณ (Solo Dev)
              ↓
       ⭐ Claudy (Orchestrator)
              ↓
   ┌──────────┴──────────┐
   ↓                     ↓
🎨 Frontend    ⚙️ Backend    🗄️ Database
🚀 DevOps      🧪 QA         🔐 Security
🔍 Code Review 📝 Docs       🔭 Research
```

**ตัวอย่างการใช้งาน:**
```
คุณ: "ทำหน้า login พร้อม JWT authentication"

→ Claudy วิเคราะห์ → กระจายงานให้ Agents
→ Research Agent: หา best practice JWT 2026
→ Backend Agent: สร้าง API
→ Database Agent: ออกแบบ schema
→ Frontend Agent: สร้าง UI
→ Security Agent: audit
→ QA Agent: test
→ Docs Writer: เขียน API doc

คุณได้รับ: complete feature พร้อม code + tests + docs
```

---

## ✅ PREREQUISITES

### 1. ทักษะที่ต้องมี
- Python 3.10+ หรือ Node.js 20+
- ใช้ terminal/command line ได้
- เข้าใจ environment variables
- รู้จัก Git พื้นฐาน

### 2. Account ที่ต้องเตรียม
- **Anthropic API Key** — สมัครที่ [console.anthropic.com](https://console.anthropic.com)
- **GitHub account** — สำหรับเก็บ project
- บัตรเครดิตสำหรับ API credit ($5-20 จะใช้ได้นาน)

### 3. Tools ที่ต้องติดตั้ง
- Python หรือ Node.js
- Git
- Code editor (VS Code แนะนำ)
- Terminal

### 4. ไฟล์ที่ได้รับมาแล้ว (11 ไฟล์)
```
📁 Your Claudy AI Team files:
├── 📝 claudy_system_prompt.md
├── 📡 agent_communication_protocol.md
├── 🎨 01_frontend_agent_system_prompt.md
├── ⚙️ 02_backend_agent_system_prompt.md
├── 🗄️ 03_database_agent_system_prompt.md
├── 🚀 04_devops_agent_system_prompt.md
├── 🧪 05_qa_testing_agent_system_prompt.md
├── 🔐 06_security_agent_system_prompt.md
├── 🔍 07_code_review_agent_system_prompt.md
├── 📝 08_docs_writer_agent_system_prompt.md
└── 🔭 09_research_agent_system_prompt.md
```

---

## 📦 PROJECT SETUP

### Step 1: สร้าง Project Directory

```bash
# สร้าง folder
mkdir claudy-ai-team
cd claudy-ai-team

# Init git
git init
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
echo "logs/" >> .gitignore
```

### Step 2: เลือก Language (Python หรือ Node.js)

#### Option A: Python (แนะนำสำหรับเริ่มต้น)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install anthropic python-dotenv rich
```

#### Option B: Node.js / TypeScript

```bash
# Init project
npm init -y

# Install dependencies
npm install @anthropic-ai/sdk dotenv chalk
npm install -D typescript @types/node tsx

# Init TypeScript
npx tsc --init
```

### Step 3: Setup Environment Variables

สร้างไฟล์ `.env`:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx

# Model selection (เลือก 1)
CLAUDE_MODEL=claude-sonnet-4-5
# หรือ
# CLAUDE_MODEL=claude-opus-4-1
# CLAUDE_MODEL=claude-haiku-4-5

# Optional: Logging
LOG_LEVEL=info
```

> 💡 **แนะนำ:** ใช้ `claude-sonnet-4-5` สำหรับ daily work (balance ระหว่าง speed + capability)
> ใช้ `claude-opus-4-1` สำหรับ complex tasks (architecture, deep research)

### Step 4: จัดวางไฟล์ System Prompts

```bash
# สร้าง folder structure
mkdir -p prompts/agents
mkdir -p src
mkdir -p logs

# ย้ายไฟล์ system prompts เข้าไป
mv claudy_system_prompt.md prompts/
mv agent_communication_protocol.md prompts/
mv 01_frontend_agent_system_prompt.md prompts/agents/frontend.md
mv 02_backend_agent_system_prompt.md prompts/agents/backend.md
mv 03_database_agent_system_prompt.md prompts/agents/database.md
mv 04_devops_agent_system_prompt.md prompts/agents/devops.md
mv 05_qa_testing_agent_system_prompt.md prompts/agents/qa.md
mv 06_security_agent_system_prompt.md prompts/agents/security.md
mv 07_code_review_agent_system_prompt.md prompts/agents/code_review.md
mv 08_docs_writer_agent_system_prompt.md prompts/agents/docs_writer.md
mv 09_research_agent_system_prompt.md prompts/agents/research.md
```

**โครงสร้างสุดท้าย:**
```
claudy-ai-team/
├── .env
├── .gitignore
├── prompts/
│   ├── claudy_system_prompt.md
│   ├── agent_communication_protocol.md
│   └── agents/
│       ├── frontend.md
│       ├── backend.md
│       ├── database.md
│       ├── devops.md
│       ├── qa.md
│       ├── security.md
│       ├── code_review.md
│       ├── docs_writer.md
│       └── research.md
├── src/
│   └── (main code)
└── logs/
```

---

## ⚙️ CONFIGURE CLAUDY + AGENTS

### Step 5: สร้าง Core Agent Class (Python)

สร้างไฟล์ `src/agent.py`:

```python
"""
Agent base class — Foundation for Claudy and all sub-agents
"""
import os
import json
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class Agent:
    """Base class สำหรับทุก Agent ในระบบ"""
    
    def __init__(self, name: str, prompt_file: str, model: str = None):
        self.name = name
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model or os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
        self.system_prompt = self._load_prompt(prompt_file)
        self.conversation_history = []
        
    def _load_prompt(self, prompt_file: str) -> str:
        """โหลด system prompt จาก markdown file"""
        path = Path("prompts") / prompt_file
        return path.read_text(encoding="utf-8")
    
    def chat(self, message: str, max_tokens: int = 8000) -> str:
        """ส่งข้อความและรับ response"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=self.system_prompt,
            messages=self.conversation_history,
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Log การใช้งาน
        self._log_usage(response)
        
        return assistant_message
    
    def reset(self):
        """ล้าง conversation history"""
        self.conversation_history = []
    
    def _log_usage(self, response):
        """Log token usage สำหรับ tracking cost"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "model": self.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        
        log_path = Path("logs") / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        log_path.parent.mkdir(exist_ok=True)
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
```

### Step 6: สร้าง Claudy Orchestrator

สร้างไฟล์ `src/claudy.py`:

```python
"""
Claudy — The Orchestrator
จัดการการสื่อสารระหว่าง Dev และ Agents ทั้งหมด
"""
from src.agent import Agent
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

class ClaudyOrchestrator:
    """Claudy — เลขาส่วนตัวที่จัดการทีม AI"""
    
    def __init__(self):
        # โหลด Claudy พร้อม system prompt + communication protocol
        claudy_prompt = self._build_claudy_prompt()
        self.claudy = Agent(
            name="claudy",
            prompt_file="claudy_system_prompt.md",
        )
        # Inject ACP เข้าไปใน context
        self.claudy.system_prompt += "\n\n" + self._load_acp()
        
        # Lazy-load agents (สร้างเฉพาะเมื่อจำเป็น)
        self.agents = {}
        self.agent_configs = {
            "frontend": "agents/frontend.md",
            "backend": "agents/backend.md",
            "database": "agents/database.md",
            "devops": "agents/devops.md",
            "qa": "agents/qa.md",
            "security": "agents/security.md",
            "code_review": "agents/code_review.md",
            "docs_writer": "agents/docs_writer.md",
            "research": "agents/research.md",
        }
    
    def _build_claudy_prompt(self) -> str:
        """รวม Claudy prompt"""
        from pathlib import Path
        return (Path("prompts") / "claudy_system_prompt.md").read_text(encoding="utf-8")
    
    def _load_acp(self) -> str:
        """โหลด Agent Communication Protocol"""
        from pathlib import Path
        return (Path("prompts") / "agent_communication_protocol.md").read_text(encoding="utf-8")
    
    def get_agent(self, agent_name: str) -> Agent:
        """Lazy-load agent เมื่อต้องการ"""
        if agent_name not in self.agents:
            if agent_name not in self.agent_configs:
                raise ValueError(f"Unknown agent: {agent_name}")
            
            self.agents[agent_name] = Agent(
                name=agent_name,
                prompt_file=self.agent_configs[agent_name],
            )
        return self.agents[agent_name]
    
    def delegate(self, agent_name: str, task: str) -> str:
        """ให้ Claudy ส่งงานต่อให้ agent อื่น"""
        console.print(Panel(
            f"[yellow]Claudy → {agent_name.upper()}[/yellow]\n\n{task}",
            border_style="yellow",
        ))
        
        agent = self.get_agent(agent_name)
        response = agent.chat(task)
        
        console.print(Panel(
            f"[cyan]{agent_name.upper()} → Claudy[/cyan]",
            border_style="cyan",
        ))
        console.print(Markdown(response))
        console.print()
        
        return response
    
    def chat(self, user_message: str) -> str:
        """Main entry point — Dev คุยกับ Claudy"""
        console.print(Panel(
            f"[green]YOU → Claudy[/green]\n\n{user_message}",
            border_style="green",
        ))
        
        response = self.claudy.chat(user_message)
        
        console.print(Panel(
            "[yellow]Claudy → YOU[/yellow]",
            border_style="yellow",
        ))
        console.print(Markdown(response))
        console.print()
        
        return response
```

### Step 7: สร้าง CLI Interface

สร้างไฟล์ `src/cli.py`:

```python
"""
Interactive CLI สำหรับคุยกับ Claudy
"""
import sys
from src.claudy import ClaudyOrchestrator
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def main():
    console.print("[bold cyan]🌟 Claudy AI Team — Initialized[/bold cyan]")
    console.print("Type your task, or 'quit' to exit\n")
    console.print("Commands:")
    console.print("  • [yellow]/delegate <agent> <task>[/yellow] — ส่งงานตรงให้ agent")
    console.print("  • [yellow]/agents[/yellow] — แสดงรายชื่อ agents")
    console.print("  • [yellow]/reset[/yellow] — ล้าง conversation")
    console.print("  • [yellow]/quit[/yellow] — ออก\n")
    
    claudy = ClaudyOrchestrator()
    
    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
            
            if not user_input.strip():
                continue
            
            # Handle commands
            if user_input.lower() in ["/quit", "quit", "exit"]:
                console.print("[cyan]Bye! 👋[/cyan]")
                break
            
            elif user_input.lower() == "/agents":
                console.print("[cyan]Available agents:[/cyan]")
                for name in claudy.agent_configs.keys():
                    console.print(f"  • {name}")
                continue
            
            elif user_input.lower() == "/reset":
                claudy.claudy.reset()
                console.print("[cyan]Conversation reset[/cyan]")
                continue
            
            elif user_input.startswith("/delegate "):
                parts = user_input[10:].split(" ", 1)
                if len(parts) == 2:
                    claudy.delegate(parts[0], parts[1])
                else:
                    console.print("[red]Usage: /delegate <agent> <task>[/red]")
                continue
            
            # Normal chat with Claudy
            claudy.chat(user_input)
            
        except KeyboardInterrupt:
            console.print("\n[cyan]Bye! 👋[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
```

### Step 8: ทดสอบการติดตั้ง

สร้างไฟล์ `src/test_setup.py`:

```python
"""ทดสอบว่า setup ถูกต้อง"""
from src.claudy import ClaudyOrchestrator

def test_basic_setup():
    print("Testing Claudy setup...")
    claudy = ClaudyOrchestrator()
    
    response = claudy.chat("สวัสดี ทดสอบระบบ — ลูกทีมพร้อมไหม?")
    
    print("\n✅ Setup สำเร็จ!")
    print(f"Response length: {len(response)} chars")

if __name__ == "__main__":
    test_basic_setup()
```

รัน test:

```bash
python -m src.test_setup
```

ถ้าเห็น `✅ Setup สำเร็จ!` — พร้อมใช้งานแล้ว! 🎉

---

## 🎬 RUN YOUR FIRST TASK

### เปิด CLI

```bash
python -m src.cli
```

คุณจะเห็น:
```
🌟 Claudy AI Team — Initialized
Type your task, or 'quit' to exit

Commands:
  • /delegate <agent> <task> — ส่งงานตรงให้ agent
  • /agents — แสดงรายชื่อ agents
  • /reset — ล้าง conversation
  • /quit — ออก

You: 
```

### ลองคุยกับ Claudy

**ตัวอย่าง 1: ขอ research**
```
You: ช่วยหาว่า state management library สำหรับ React โปรเจกต์เล็ก 
     ควรใช้อะไรดี? ทีมแค่คนเดียว
```

Claudy จะวิเคราะห์และส่งให้ Research Agent ทำงาน

**ตัวอย่าง 2: สร้าง feature เต็ม**
```
You: ทำ login form ด้วย React + TypeScript ให้หน่อย
     - มี email + password fields
     - validation
     - loading state
     - error handling
```

Claudy จะกระจายให้ Frontend Agent

**ตัวอย่าง 3: ส่งงานตรง (skip Claudy)**
```
You: /delegate research เปรียบเทียบ PostgreSQL vs MongoDB สำหรับ e-commerce
```

ส่งตรงให้ Research Agent โดยไม่ผ่าน Claudy

---

## 📅 DAILY WORKFLOW

### Morning Routine
```bash
# 1. Activate environment
cd claudy-ai-team
source venv/bin/activate

# 2. Start Claudy
python -m src.cli
```

### Typical Solo Dev Day

```
☀️ เช้า: Planning
You: "วันนี้จะทำ feature checkout. ช่วยวางแผนให้หน่อย"
Claudy: → วิเคราะห์ → แตก task → แนะนำลำดับ

🍕 บ่าย: Implementation
You: "ทำส่วน Backend API ก่อน"
Claudy: → Backend Agent → code + tests
You: "review code นี้ให้หน่อย"
Claudy: → Code Review Agent

🌙 เย็น: Polish
You: "เขียน API docs สำหรับ endpoint ที่ทำวันนี้"
Claudy: → Docs Writer Agent
```

### Tips สำหรับ Solo Dev

1. **เริ่มจาก Claudy เสมอ** — ให้ Claudy แตก task ก่อน
2. **ใช้ `/delegate` เมื่อรู้แล้วว่าใครต้องทำ** — เร็วกว่า ประหยัด token
3. **`/reset` บ่อยๆ** — long conversation = expensive
4. **Save outputs** — copy code ออกมาเก็บใน project จริงทันที

---

## 💡 REAL-WORLD EXAMPLES

### Example 1: สร้าง Feature ใหม่

```
You: ทำ user profile page ที่
     - แสดง avatar + name + email
     - แก้ไขข้อมูลได้
     - upload รูป
     - ใช้ React + TypeScript + Tailwind

Claudy: 📥 รับเรื่อง: User Profile Page

แผนการทำงาน:
1. 🎨 Frontend Agent → UI components
2. ⚙️ Backend Agent → API endpoints (GET/PATCH /api/profile, POST /api/upload)
3. 🗄️ Database Agent → User schema check (อาจไม่ต้องเปลี่ยน)
4. 🔐 Security Agent → file upload security review
5. 🧪 QA Agent → test scenarios
6. 📝 Docs Writer → API documentation

ประเมิน: ~2 ชั่วโมงทำเอง / Agent ทำได้ใน 1 turn ต่อ agent

จะเริ่มจาก Frontend ก่อนดีไหม?
```

**คุณ:**
```
You: เริ่มเลย
```

Claudy จะวิ่งไปคุยกับแต่ละ agent ตามลำดับ

### Example 2: Debug ปัญหา

```
You: API /api/orders ตอบช้ามาก ใช้เวลา 3 วินาที
     ช่วยวิเคราะห์ให้หน่อย

Claudy: 🔍 ขอข้อมูลเพิ่ม:
1. Endpoint ทำอะไรบ้าง?
2. Database query แบบไหน?
3. Traffic เป็นยังไง?

You: เป็น GET ดึง orders ของ user พร้อม items ทั้งหมด
     ใช้ Prisma findMany มี include items
     User มี ~1000 orders

Claudy: เข้าใจแล้ว — น่าจะเป็น N+1 problem
ขอส่งให้ Database Agent วิเคราะห์ลึก

→ Database Agent:
   - แนะนำ composite index
   - Rewrite query ด้วย select เฉพาะ field ที่ต้อง
   - ใช้ cursor pagination
   - Expected improvement: 3000ms → 50ms
```

### Example 3: Architecture Decision

```
You: โปรเจกต์เริ่มโต ควรย้ายเป็น microservices ไหม?

Claudy: เป็น architecture decision สำคัญ
ขอส่งให้ Research Agent ค้นคว้าให้ครบ

→ Research Agent: (research 30 min)
   Recommendation: ยังไม่ควรย้าย เพราะ:
   - ทีม 1 คน — overhead ของ microservices สูงเกินไป
   - Traffic ยังไม่ถึง 10K RPS
   - Modular monolith ดีกว่าใน context นี้
   
   แนะนำ: Modular monolith pattern
   - แยก modules ชัดเจน (อนาคต extract ได้)
   - Tools: NestJS modules / Domain-Driven structure
   - Migration path ถ้าโตขึ้น: 2-3 เดือน
```

### Example 4: Code Review

```
You: /delegate code_review ดูโค้ดนี้ให้หน่อย
[paste โค้ด]

→ Code Review Agent:
   🌟 Praise: TypeScript types ดี, error handling ครบ
   ⚠️ Major: 
     - useEffect dependency ไม่ครบ (line 23)
     - Missing key in list (line 45)
   💡 Minor:
     - Extract magic number
     - Consider useMemo for expensive calc
   ✨ Nitpicks:
     - Import order
```

---

## 💰 COST OPTIMIZATION

### ราคาโดยประมาณ (Claude Sonnet 4.5)

| งาน | Token ใช้ | ราคาประมาณ |
|----|----------|------------|
| Simple chat | 5-10K | $0.02 |
| Feature planning | 15-25K | $0.05 |
| Code generation | 30-50K | $0.15 |
| Full feature flow | 100K+ | $0.50 |
| Deep research | 50-150K | $0.30 |

**สำหรับ Solo Dev ใช้งานปกติ: $5-20/เดือน**

### Tips ลดค่าใช้จ่าย

**1. ใช้ Reset บ่อยๆ**
```bash
# ทุกครั้งที่เริ่มงานใหม่
/reset
```
Long conversation = expensive (เพราะส่ง history ทั้งหมด)

**2. ใช้ /delegate แทน chat ปกติ เมื่อรู้แล้ว**
```bash
# แทนที่
You: ช่วยให้ research agent หา...

# ใช้
/delegate research หา...
```
ประหยัด token ของ Claudy

**3. ใช้ Model ที่เหมาะสม**

```python
# Edit .env
CLAUDE_MODEL=claude-haiku-4-5  # เร็ว ถูก (10x ถูกกว่า)
# ใช้สำหรับ:
# - Simple lookups
# - Docs writing
# - Code review เบื้องต้น

CLAUDE_MODEL=claude-sonnet-4-5  # Balance (default)
# ใช้สำหรับ:
# - งานทั่วไป daily work

CLAUDE_MODEL=claude-opus-4-1  # ดีที่สุด แพง
# ใช้สำหรับ:
# - Architecture decisions
# - Complex algorithms
# - Deep research
```

**4. Track Usage**

ดู logs:
```bash
cat logs/$(date +%Y-%m-%d).jsonl | jq '.input_tokens + .output_tokens' | awk '{sum+=$1} END {print "Total tokens today:", sum}'
```

**5. Set Budget Alert**

ที่ [console.anthropic.com](https://console.anthropic.com) ตั้ง spending limit เช่น $20/เดือน

---

## 🔧 TROUBLESHOOTING

### ปัญหา: API Key error

```
anthropic.AuthenticationError: invalid x-api-key
```

**แก้:**
- ตรวจสอบ `.env` มี API key ถูกต้อง
- ตรวจสอบ `load_dotenv()` ทำงาน
- API key ไม่มี whitespace
- API key ยังไม่หมดอายุ

```bash
# Test
echo $ANTHROPIC_API_KEY  # ควรเห็น sk-ant-...
```

### ปัญหา: Token limit exceeded

```
anthropic.BadRequestError: max_tokens exceeded
```

**แก้:**
- ลด `max_tokens` ใน `agent.chat()`
- `/reset` conversation
- แตกงานเป็นชิ้นเล็กลง

### ปัญหา: Rate limit

```
anthropic.RateLimitError: rate_limit_exceeded
```

**แก้:**
- รอ 60 วินาที
- เพิ่ม credit ใน console
- ใช้ exponential backoff

```python
# เพิ่มใน agent.py
import time
from anthropic import RateLimitError

def chat_with_retry(self, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return self.chat(message)
        except RateLimitError:
            wait = 2 ** attempt
            print(f"Rate limited, waiting {wait}s...")
            time.sleep(wait)
    raise
```

### ปัญหา: Agent ลืม context

**สาเหตุ:** อาจ reset ไป หรือ context window เต็ม

**แก้:**
- เก็บ key decisions ไว้ใน notes
- ส่ง context สำคัญทุกครั้งที่เริ่ม conversation ใหม่
- ใช้ explicit summary ก่อน reset

### ปัญหา: Response ช้า

**แก้:**
- ใช้ Haiku model สำหรับงานเร็ว
- ลด max_tokens
- Streaming response (advanced)

### ปัญหา: Agent ตอบไม่ตรงประเด็น

**แก้:**
- ส่ง context ให้ครบ
- ระบุ format ที่ต้องการ
- ให้ตัวอย่าง output

```
❌ "ทำ login form"
✅ "ทำ login form ด้วย React + TypeScript + Tailwind
    - Email + password fields
    - Show password toggle
    - Loading state
    - Error display
    - Submit handler ที่รับ onSuccess + onError props"
```

---

## 🎓 NEXT STEPS

### Level 1: Master the Basics (สัปดาห์ที่ 1)
- [ ] Setup เสร็จ
- [ ] รัน first task สำเร็จ
- [ ] ลองใช้ทุก agent อย่างน้อย 1 ครั้ง
- [ ] ทำ feature เล็กๆ ที่ end-to-end

### Level 2: Optimize Workflow (สัปดาห์ที่ 2-4)
- [ ] สร้าง alias / shortcuts
- [ ] เก็บ template prompts ที่ใช้บ่อย
- [ ] Track cost
- [ ] ปรับ model ตาม task

### Level 3: Customize (เดือนที่ 2)
- [ ] เพิ่ม project-specific context ใน Claudy prompt
- [ ] สร้าง custom agent สำหรับ stack ของคุณ
- [ ] Build dashboard ดู usage
- [ ] Integrate with VS Code

### Level 4: Advanced (เดือนที่ 3+)
- [ ] Multi-agent parallel execution
- [ ] Memory system (เก็บ project knowledge)
- [ ] Auto-commit + git integration
- [ ] CI/CD with Claudy reviewing PRs

---

## 📚 USEFUL SHORTCUTS

### Bash Aliases

เพิ่มใน `~/.bashrc` หรือ `~/.zshrc`:

```bash
# Claudy shortcuts
alias claudy='cd ~/claudy-ai-team && source venv/bin/activate && python -m src.cli'
alias claudy-cost='cat ~/claudy-ai-team/logs/$(date +%Y-%m-%d).jsonl | jq ".input_tokens + .output_tokens" | awk "{sum+=\$1} END {print \"Tokens today:\", sum}"'
alias claudy-logs='tail -f ~/claudy-ai-team/logs/$(date +%Y-%m-%d).jsonl'
```

ใช้งาน:
```bash
claudy          # เปิด CLI
claudy-cost     # ดู token usage วันนี้
claudy-logs     # ดู logs realtime
```

### VS Code Tasks

สร้าง `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Claudy",
      "type": "shell",
      "command": "python -m src.cli",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

`Ctrl+Shift+B` → Run Claudy

---

## 🎯 PRO TIPS

### 1. Project Context Injection

ทุกครั้งที่เปิด session ใหม่ ส่ง context ของ project:

```
You: Context: ผมทำ e-commerce ด้วย Next.js 14 + Prisma + PostgreSQL
     Deploy บน Vercel + Supabase
     ตอนนี้กำลังทำ checkout feature
     
     ขอเริ่มงานวันนี้: ทำ payment integration
```

### 2. Save Reusable Prompts

สร้าง `templates/` folder:

```
templates/
├── new-feature.md
├── code-review-request.md
├── deploy-checklist.md
└── debug-template.md
```

ใช้:
```bash
cat templates/new-feature.md | xclip  # copy to clipboard
```

### 3. Iterate, Don't Restart

แทนที่จะเริ่มใหม่ทั้งหมด — แก้ทีละจุด:

```
You: โค้ดเมื่อกี้ดี แต่ error message ภาษาไทยหน่อย
You: เพิ่ม dark mode support ในนี้
You: ทำให้ responsive บน mobile ด้วย
```

### 4. Use Agents Specialization

- **Speed:** Haiku สำหรับงาน routine
- **Quality:** Sonnet สำหรับงานหลัก
- **Depth:** Opus สำหรับ architecture / research

### 5. Document Decisions

ใช้ Docs Writer Agent บันทึก ADRs:

```
You: /delegate docs_writer 
     บันทึก ADR ของการตัดสินใจใช้ Zustand แทน Redux Toolkit
     เหตุผล: bundle size + team size
```

---

## 🚨 IMPORTANT REMINDERS

### Security
- ❌ ห้าม commit `.env` ไป git
- ❌ ห้ามแชร์ API key
- ✅ Rotate API key ทุก 3 เดือน
- ✅ ตั้ง spending limit

### Best Practices
- 💾 Save outputs ที่ดีลงใน project ทันที
- 📝 Log decisions สำคัญ
- 🔄 Reset conversation บ่อยๆ
- 🧪 Test code ที่ได้รับเสมอ
- 📊 Monitor costs

### Limitations to Remember
- Agents ไม่รู้ codebase ของคุณ ต้อง paste context
- ไม่มี persistent memory ระหว่าง sessions
- ไม่สามารถรัน code ได้ (แค่ generate)
- ต้อง verify โค้ดเสมอก่อนใช้ production

---

## 📞 GETTING HELP

### เมื่อติดปัญหา:

1. **ตรวจสอบ logs:**
   ```bash
   tail -20 logs/$(date +%Y-%m-%d).jsonl
   ```

2. **ลด complexity:**
   - แตก task ให้เล็กลง
   - ส่ง context ให้ครบ
   - ระบุ format output ที่ต้องการ

3. **Resources:**
   - [Anthropic Docs](https://docs.anthropic.com)
   - [API Reference](https://docs.anthropic.com/en/api/getting-started)
   - [Discord](https://discord.gg/anthropic)

---

## 🎉 YOU'RE READY!

ตอนนี้คุณมี

✅ Claudy + 9 Agents พร้อมใช้
✅ CLI สำหรับ daily work
✅ Cost tracking
✅ Workflow ที่ optimize แล้ว

**สิ่งสุดท้ายที่ต้องจำ:**

> Agents เก่ง แต่คุณคือ Dev
> ให้ Agents ช่วย แต่ตัดสินใจสุดท้ายเป็นของคุณ
> Quality is your responsibility
> 
> **Happy coding with your AI team! 🚀**

---

## 📋 APPENDIX

### A. File Structure ที่ Complete

```
claudy-ai-team/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt          # Python
├── package.json              # หรือ Node.js
├── prompts/
│   ├── claudy_system_prompt.md
│   ├── agent_communication_protocol.md
│   └── agents/
│       ├── frontend.md
│       ├── backend.md
│       ├── database.md
│       ├── devops.md
│       ├── qa.md
│       ├── security.md
│       ├── code_review.md
│       ├── docs_writer.md
│       └── research.md
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── claudy.py
│   ├── cli.py
│   └── test_setup.py
├── logs/
│   └── 2026-05-13.jsonl
└── templates/                # Optional
    ├── new-feature.md
    └── debug-template.md
```

### B. .env.example

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...

# Model selection
CLAUDE_MODEL=claude-sonnet-4-5

# Optional
LOG_LEVEL=info
MAX_TOKENS=8000
```

### C. requirements.txt (Python)

```
anthropic>=0.40.0
python-dotenv>=1.0.0
rich>=13.0.0
```

### D. package.json (Node.js)

```json
{
  "name": "claudy-ai-team",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "tsx src/cli.ts",
    "test": "tsx src/test_setup.ts"
  },
  "dependencies": {
    "@anthropic-ai/sdk": "^0.40.0",
    "dotenv": "^16.0.0",
    "chalk": "^5.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0"
  }
}
```

### E. Sample Workflow Script

`workflows/new_feature.py`:

```python
"""Quick template for new feature development"""
from src.claudy import ClaudyOrchestrator

def new_feature_workflow(feature_description: str):
    claudy = ClaudyOrchestrator()
    
    # 1. Planning
    plan = claudy.chat(f"""
    วางแผนทำ feature นี้:
    {feature_description}
    
    บอก:
    1. แตก task ยังไง
    2. Agent ไหนทำอะไร
    3. ลำดับ
    4. Risk
    """)
    
    # 2. Research first
    claudy.delegate("research", 
        f"หา best practice สำหรับ: {feature_description}")
    
    # 3. Backend first (usually)
    claudy.delegate("backend",
        f"Implement backend สำหรับ: {feature_description}")
    
    # 4. Frontend
    claudy.delegate("frontend",
        f"Implement frontend สำหรับ: {feature_description}")
    
    # 5. Tests
    claudy.delegate("qa",
        f"เขียน tests สำหรับ feature นี้")
    
    # 6. Docs
    claudy.delegate("docs_writer",
        f"เขียน docs สำหรับ feature นี้")

if __name__ == "__main__":
    new_feature_workflow("User profile page with avatar upload")
```

ใช้:
```bash
python -m workflows.new_feature
```

---

*Version 1.0 — Quick Start Guide for Solo Developers*
*Last Updated: 2026-05-13*

🌟 **Happy building with Claudy AI Team!** 🚀
