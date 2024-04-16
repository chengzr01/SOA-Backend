from typing import List, Dict, Optional
from src.frontend_agent import FrontendAgent


def respond_to_user_input(
    user_input: str, 
    FrontendAgent: frontend_agent
) -> Dict[str, str]:
    """
    Respond to user's input.
    @return: the response to the user's input in a dictionary format.
    """
    
    complete = agent.check_key_info_completeness(user_input)
    if complete:
        query = agent.query_backend(user_input)
        # TODO: send query to backend
        
        return {"front end response": None, "back end response": None}
    else:
        response = agent.respond_frontend(user_input)
        return response

