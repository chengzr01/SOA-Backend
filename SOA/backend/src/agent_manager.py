from typing import Optional, Dict

from django.contrib.auth.models import User

from backend.src.frontend_agent import FrontendAgent
from backend.src.backend_agent import BackendAgent


class AgentManager:
    def __init__(self):
        self.frontend_agents : Dict[str, FrontendAgent] = {}
        self.backend_agents : Dict[str, BackendAgent] = {}

    def add_frontend_agent(self, username: str, user: User) -> bool:
        agent = FrontendAgent()
        agent.switch_user(user)
        if username not in self.frontend_agents:
            self.frontend_agents[username] = agent
            return True
        return False
    
    def add_backend_agent(self, username: str, user: User) -> bool:
        agent = BackendAgent()
        agent.switch_user(user)
        if username not in self.backend_agents:
            self.backend_agents[username] = agent
            return True
        return False

    def remove_frontend_agent(self, username: str) -> bool:
        if username in self.frontend_agents:
            del self.frontend_agents[username]
            return True
        return False
    
    def remove_backend_agent(self, username: str) -> bool:
        if username in self.backend_agents:
            # self.backend_agents[username].save_user_profile()
            del self.backend_agents[username]
            return True
        return False

    def get_frontend_agent(self, username: str) -> Optional[FrontendAgent]:
        if username not in self.frontend_agents:
            return None
        return self.frontend_agents[username]
    
    def get_backend_agent(self, username: str) -> Optional[BackendAgent]:
        if username not in self.backend_agents:
            return None
        return self.backend_agents[username]
    