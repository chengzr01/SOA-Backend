from zhipuai import ZhipuAI
from src.config import ZHIPU_API_KEY


class FrontEndAgent:
    """
    Agent used to interact with users in the front end.
    
    Usage:
    agent = FrontEndAgent()
    response = agent.respond("Hello, how are you?")
    print(response)
    """
    def __init__(self, api_key=ZHIPU_API_KEY, streaming_on=False):
        self.client = ZhipuAI(api_key=api_key)
        self.chat_history = []
        self.streaming_on = streaming_on
        
    def respond(self, latest_user_input: str):
        """
        Respond to user's input.
        """
        
        self.append_user_input(latest_user_input)
        if self.streaming_on:
            raise NotImplementedError("Streaming output is not yet supported.")
        else:
            response = self.client.chat.completions.create(
                model = "glm-4",
                messages = self.chat_history,
                # TODO: Streaming output
            )
            self.append_agent_output(response.choices[0].message.content)
            return response.choices[0].message.content
        
    def append_user_input(self, user_input: str):
        self.chat_history.append({"role": "user", "content": user_input})
        
    def append_agent_output(self, agent_output: str):
        self.chat_history.append({"role": "assistant", "content": agent_output})

    def clear_history(self) -> bool:
        self.chat_history = []
        return True


class BackEndAgent():
    pass