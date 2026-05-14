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
        self.model = model or os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        self.system_prompt = self._load_prompt(prompt_file)
        self.conversation_history = []
        
    def _load_prompt(self, prompt_file: str) -> str:
        """โหลด system prompt จาก markdown file"""
        base_dir = Path(__file__).resolve().parent.parent
        path = base_dir / "prompts" / prompt_file
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
        
        base_dir = Path(__file__).resolve().parent.parent
        log_path = base_dir / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        log_path.parent.mkdir(exist_ok=True)
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")