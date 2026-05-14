"""
Interactive CLI สำหรับคุยกับ Claudy
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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