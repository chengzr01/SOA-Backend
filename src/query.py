from src.api import FrontEndAgent


def respond_to_user_input(user_input: str, FrontEndAgent: agent) -> str:
    """
    Respond to user's input.
    """
    if agent.streaming_on:
        # TODO: Streaming output
        raise NotImplementedError("Streaming output is not yet supported.")
    else:
        response = agent.respond(user_input)
        return response
    

