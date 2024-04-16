import unittest
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.frontend_agent import FrontendAgent
from src.config import *


class FrontendAgentTest(unittest.TestCase):
    def __init__(self):
        self.agent = FrontendAgent()
    
    def test_respond(self, user_input: str):
        response = self.agent.respond(user_input)
        print(response)
        assert type(response) == type("str")
        assert response is not None
        assert response != ""
        
    def test_print_past_message(self):
        print("\nThe following is the chat history:")
        for message in self.agent.chat_history:
            print(message, '\n')
        
    def test_generate_system_message(self):
        system_message = self.agent._generate_system_message()
        print(system_message)
        assert type(system_message) == type("str")
        assert system_message is not None
        assert system_message != ""
        
    def test_process_input(self, user_input: str):
        res = self.agent._process_input(user_input)
        print(res)
        assert type(res) == type({})
        
    def test_parse_dictionary_output_in_string():
        pass
    
    def test_frontend_pipeline_complete(self):
        self.agent.clear_history()
        user_input = "I am interested in working at Google for a software engineering position. Can you help me?"
        print("User input:", user_input)
        while not self.agent.check_key_info_completeness(user_input):
            response = self.agent.respond_frontend(user_input)
            print("Agent:", response['frontend response'])
            user_input = input("User input: ")
        
        query = self.agent.query_backend(user_input)
        print("Query:", query, '\n')
        
    def test_frontend_pipeline_incomplete(self):
        self.agent.clear_history()
        user_input = "I am interested in working at Google. Can you help me?"
        print("User input:", user_input)
        while not self.agent.check_key_info_completeness(user_input):
            response = self.agent.respond_frontend(user_input)
            print("Agent:", response['frontend response'])
            user_input = input("User input: ")
        
        query = self.agent.query_backend(user_input)
        print("Query:", query, '\n')


if __name__ == "__main__":
    agent = FrontendAgentTest()
    
    agent.test_frontend_pipeline_complete()
    agent.test_frontend_pipeline_incomplete()
    
    # agent.test_respond("Hello, how are you?")
    # agent.test_respond("I want to know about Machine Learning and AI Companies. Can you give me some examples?")
    # agent.test_print_past_message()