import unittest
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.api import FrontEndAgent


class FrontEndAgentTest(unittest.TestCase):
    def __init__(self):
        self.agent = FrontEndAgent()
    
    def test_respond(self, user_input: str):
        response = self.agent.respond(user_input)
        print(response)
        assert type(response) == type("str")
        assert response is not None
        assert response != ""
        
    def test_print_past_message(self):
        print("\nThe following is the chat history:")
        for message in self.agent.chat_history:
            print(message)
        print("\n")
        
    def test_generate_system_message(self):
        system_message = self.agent.generate_system_message()
        print(system_message)
        assert type(system_message) == type("str")
        assert system_message is not None
        assert system_message != ""
        
    def test_parse_dictionary_output_in_string():
        pass


if __name__ == "__main__":
    agent = FrontEndAgentTest()
    agent.test_generate_system_message()
    # agent.test_respond("Hello, how are you?")
    # agent.test_respond("I want to know about Machine Learning and AI Companies. Can you give me some examples?")
    agent.test_print_past_message()