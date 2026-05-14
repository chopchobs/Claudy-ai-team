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
            "frontend": "agents/01_frontend_agent_system_prompt.md",
            "backend": "agents/02_backend_agent_system_prompt.md",
            "database": "agents/03_database_agent_system_prompt.md",
            "devops": "agents/04_devops_agent_system_prompt.md",
            "qa": "agents/05_qa_testing_agent_system_prompt.md",
            "security": "agents/06_security_agent_system_prompt.md",
            "code_review": "agents/07_code_review_agent_system_prompt.md",
            "docs_writer": "agents/08_docs_writer_agent_system_prompt.md",
            "research": "agents/09_research_agent_system_prompt.md",
        }
    
    def _build_claudy_prompt(self) -> str:
        """รวม Claudy prompt"""
        from pathlib import Path
        base_dir = Path(__file__).resolve().parent.parent
        return (base_dir / "prompts" / "claudy_system_prompt.md").read_text(encoding="utf-8")
    
    def _load_acp(self) -> str:
        """โหลด Agent Communication Protocol"""
        from pathlib import Path
        base_dir = Path(__file__).resolve().parent.parent
        return (base_dir / "prompts" / "agent_communication_protocol.md").read_text(encoding="utf-8")
    
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