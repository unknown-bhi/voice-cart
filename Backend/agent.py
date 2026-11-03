"""
Entrypoint for LiveKit Agent CLI.
Run: python agent.py console
"""

import os
from dotenv import load_dotenv
from app.modules.agent.worker import entrypoint
from livekit.agents import WorkerOptions, cli

load_dotenv()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))