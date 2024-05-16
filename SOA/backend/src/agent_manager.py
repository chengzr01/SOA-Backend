from typing import Optional

from backend.src.frontend_agent import FrontendAgent


class AgentManager:
    def __init__(self):
        self.agents = {}

    def add_agent(self, username: str, agent: FrontendAgent) -> bool:
        if username not in self.agents:
            self.agents[username] = agent
            return True
        return False

    def remove_agent(self, username: str) -> bool:
        if username in self.agents:
            del self.agents[username]
            return True
        return False

    def get_agent(self, username: str) -> Optional[FrontendAgent]:
        if username not in self.agents:
            return None
        return self.agents[username]