from zhipuai import ZhipuAI
from typing import List, Dict, Optional
from src.config import *


class FrontEndAgent:
    """
    Agent used to interact with users in the front end.
    
    Usage:
    agent = FrontEndAgent()
    response = agent.respond("Hello, how are you?")
    print(response)
    """
    def __init__(
        self, 
        api_key : str = ZHIPU_API_KEY,
        keywords : Optinal[List[str]] = DEFAULT_KEYWORDS, 
        opening : str = DEFAULT_OPENING,
        streaming_on : bool = False,
        user_profile : Optional[Dict[str, str]] = None,
    ):
        # ZhipuAI client object
        self.client = ZhipuAI(api_key=api_key)
        
        # chat history of the user and the agent
        self.chat_history = []
        self.append_agent_output(opening)
        
        # streaming output
        self.streaming_on = streaming_on
        
        # key information that the users need to provide
        self.key_information = {key : None for key in keywords}
        for key, value in user_profile.items():
            if key in self.key_information:
                self.key_information[key] = value
        
        # store user profile
        self.user_profile = user_profile        
                
    
    def check_key_info_completeness(self, user_input: str) -> bool:
        """
        Process user input to extract key information.
        @param user_input: the user input.
        @return: True if the key information is complete; False otherwise.
        """
        # append process input to extract key information
        self.append_user_input(user_input)
        self.process_input(user_input)
        
        # check if key information is complete
        for key, value in self.key_information.items():
            if value is None:
                return False
        return True
    
    
    def process_input(self, user_input: str):
        system_message = self.generate_system_message()
       	response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages= [
                {"role": "system", "content": system_message}
            ] + self.chat_history,
        )
        # parse the response to extract key information
        response_text = response.choices[0].message.content
        parse_dictionary_output_in_string(response_text)
        
        
    def generate_system_message(self) -> str:
        system_message = "You are an agent that helps people find jobs of their interest. You should seek for the following information provided by user:"
        for key, value in self.key_information.items():
            if value is None:
                system_message += f" {INFORMATION_NAMES[key]},"
        system_message = system_message[:-1] + "."
        
        system_message += "\nThe results should be displayed in the following format:\n"
        system_message += "{"
        for key, value in self.key_information.items():
            system_message += f"{INFORMATION_NAMES[key]}: xxx, "
        system_message = system_message[:-2] + "}"
        
        system_message += "\nDo not repeat the question. Only return the output dictionary."
        
        return system_message
    
    
    def parse_dictionary_output_in_string(self, output: str)
        # TODO: Implement this method
        pass

    
    def respond_frontend(self, latest_user_input: str) -> str:
        """
        Respond to user's input.
        @param latest_user_input: the latest user input.
        @return: the response to the user's input.
        """
        if self.streaming_on:
            raise NotImplementedError("Streaming output is not yet supported.")
        else:
            response = self.client.chat.completions.create(
                model = "glm-4",
                messages = self.chat_history,
                # TODO: Streaming output
            )
            response_text = response.choices[0].message.content
            self.append_agent_output(response_text)
            return response_text
    
    
    def query_backend(self, latest_user_input: str) -> Dict[str, str]:
        return self.key_information     

        
    def append_user_input(self, user_input: str):
        self.chat_history.append({"role": "user", "content": user_input})
        
        
    def append_agent_output(self, agent_output: str):
        self.chat_history.append({"role": "assistant", "content": agent_output})


    def clear_history(self, size=0) -> bool:
        self.chat_history = self.chat_history[:size]
        return True


class BackEndAgent():
    pass