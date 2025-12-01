import sys
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class AgentLogger:
    """
    Observability module to trace agent execution and hand-offs.
    """
    
    @staticmethod
    def log_phase(agent_name, icon, status):
        """Logs a major phase change in the agent pipeline."""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*60}")
        print(f"{icon}  {Fore.YELLOW}AGENT ACITVATED: {Fore.WHITE}{agent_name}")
        print(f"   {Fore.BLACK}Status: {status}")
        print(f"{Style.BRIGHT}{Fore.CYAN}{'='*60}\n")
        time.sleep(0.5) # Artificial delay for dramatic effect in demo

    @staticmethod
    def log_thought(content):
        """Logs the internal reasoning or raw output of an agent."""
        print(f"{Fore.GREEN}┌── {Style.BRIGHT}Agent Output / Reasoning:")
        for line in content.split('\n'):
            if line.strip():
                print(f"{Fore.GREEN}│ {Fore.WHITE} {line}")
        print(f"{Fore.GREEN}└──────────────────────────────────────────")

    @staticmethod
    def log_handoff(from_agent, to_agent, data_preview):
        """Visually demonstrates the data hand-off between agents."""
        print(f"\n{Fore.MAGENTA}>>> HAND-OFF PROTOCOL INITIATED >>>")
        print(f"{Fore.MAGENTA}    From: {Fore.WHITE}{from_agent}")
        print(f"{Fore.MAGENTA}    To:   {Fore.WHITE}{to_agent}")
        print(f"{Fore.MAGENTA}    Payload: {Fore.WHITE}{data_preview}...")
        print(f"{Fore.MAGENTA}>>> TRANSFER COMPLETE >>>\n")

    @staticmethod
    def log_tool_usage(tool_name, args, result):
        """Logs when a tool is actually called."""
        print(f"\n{Fore.RED}🛠️  TOOL USE DETECTED: {Fore.WHITE}{tool_name}")
        print(f"    {Fore.RED}Args:   {Fore.WHITE}{args}")
        print(f"    {Fore.RED}Result: {Fore.WHITE}{result}\n")