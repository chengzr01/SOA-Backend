from src.api import FrontEndAgent, BackEndAgent


def respond_to_user_input(
    user_input: str, 
    FrontEndAgent: frontend_agent, 
    BackEndAgent: backend_agent
):
    """
    Respond to user's input.
    @return: the response to the user's input.
    """
    # TODO: return type undefined
    
    complete = agent.check_key_info_completeness(user_input)
    if complete:
        query = agent.query_backend(user_input)
        # TODO: send query to backend
        # data = backend_agent.process_input(query)
        # return data
    else:
        response = agent.respond_frontend(user_input)
        return response

