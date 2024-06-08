from typing import List, Dict, Optional
import re
from backend.models import ChatMessage
from django.contrib.auth.models import User
from django.db import models

from zhipuai import ZhipuAI

from backend.src.config import *


class FrontendAgent:
    """
    Agent used to interact with users in the front end.

    Usage:
    agent = FrontEndAgent()
    response = agent.respond("Hello, how are you?")
    print(response)
    """

    def __init__(
        self,
        api_key: str = ZHIPU_API_KEY,
        keywords: Optional[List[str]] = DEFAULT_KEYWORDS,
        optinal_keywords: Optional[List[str]] = OPTIONAL_KEYWORDS,
        streaming_on: bool = False,
        user_profile: Optional[Dict[str, str]] = None,
    ):
        self.user = None
        # ZhipuAI client object
        self.client = ZhipuAI(api_key=api_key)

        # chat history of the user and the agent
        self.chat_history = []
        # we temporarily comment out this
        # because we initialize before the user logs in
        # so at this point we are unable to determine the receiver of the opening message
        # we will restore the opening message manually
        # everytime the user log in

        # self.append_agent_output(opening)

        # streaming output
        self.streaming_on = streaming_on

        # store user profile
        self.user_profile = user_profile

        # key information that the users need to provide
        print("@" * 10)
        print("[__INIT__ (FRONTEND AGENT)] keywords", keywords)
        print("[__INIT__ (FRONTEND AGENT)] optional_keywords", optinal_keywords)
        self.keywords = keywords
        self.optional_keywords = optinal_keywords
        self._initialize_key_information()

        self.summary = ""  # a summary of the chatting history

    def switch_user(self, user: User):
        self.user = user
        print('Switching user to:', user)  # DEBUG
        self._switch_history()

    def _initialize_key_information(self) -> Dict[str, str]:
        # combine the keywords and optional keywords
        self.key_information = {
            key: None for key in self.keywords + self.optional_keywords}

        if self.user_profile is not None:
            for key, value in self.user_profile.items():
                if key in self.key_information:
                    self.key_information[key] = value

    def flush(self) -> bool:
        """
        Clear the chat history and key information for the current user.
        Deleting from the dataset and cache 
        """
        self.__reset_chat_history_for_user()
        self._initialize_key_information()
        return True

    def reset(self) -> bool:
        """
        Clear the chat history and key information for all users.
        Deleting from the dataset and cache
        """
        self.__reset_chat_history()
        return True

    def __reset_chat_history_for_user(self):
        """
        Reset the chat history and key information.
        """
        self.chat_history = []
        self._initialize_key_information()
        # also delete all chat messages about the current user from the database
        ChatMessage.objects.filter(
            models.Q(sender=self.user) | models.Q(receiver=self.user)
        ).delete()

    def __reset_chat_history(self):
        """
        Reset the chat history and key information.
        """
        self.chat_history = []
        self._initialize_key_information()
        # also delete all chat messages from the database
        ChatMessage.objects.all().delete()

    def check_key_info_completeness(self, user_input: str) -> bool:
        """
        Process user input to extract key information.
        @param user_input: the user input.
        @return: True if the key information is complete; False otherwise.
        """
        # append process input to extract key information
        self._append_user_input(user_input)
        self._store_chat_message({"role": "user", "content": user_input})
        self._process_input(user_input)

        # check if key information is complete
        # only key information is require, the optional information is not required
        for key, value in self.key_information.items():
            if key in self.keywords and value is None:
                return False
        return True

    def _process_input(self, user_input: str) -> Dict[str, str]:
        system_message = self._generate_system_message('user input process')
        self._append_user_input(user_input)
        self._store_chat_message({"role": "user", "content": user_input})

        print("%" * 10)
        print("[_PROCESS_INPUT] system_message", system_message)

        response = self.client.chat.completions.create(
            model="glm-3-turbo",
            messages=[
                {"role": "system", "content": system_message}
            ] + self.chat_history,
            # messages = self.chat_history,
        )
        # parse the response to extract key information
        response_text = response.choices[0].message.content

        print("%" * 10)
        print("[_PROCESS_INPUT] response_text", response_text)

        response_dict = self._parse_string_to_dictionary(response_text)

        print("%" * 10)
        print("[_PROCESS_INPUT] response_dict", response_dict)

        # update key information
        for key, value in response_dict.items():
            if (key in self.key_information):
                self.key_information[key] = value

        return response_dict

    def _generate_system_message(self, mode='user input process') -> str:
        assert mode in ['user input process', 'asking for more information']

        if mode == 'user input process':
            system_message = "You are an agent that helps people find jobs of their interest. You should seek for the following information provided by user:"
            for key, value in self.key_information.items():
                if value is None:
                    system_message += f" {key},"
            system_message = system_message[:-1] + "."

            system_message += "\n###\n"
            system_message += "\nThe results should be displayed in the following format:\n"
            system_message += "{"
            for key, value in self.key_information.items():
                system_message += f"{key}: value, "
            system_message = system_message[:-2] + "}"
            system_message += "\n###\n"

            system_message += "\nIf an information is missing, the value should be 'None'."
            system_message += "\nDo not repeat the question. Only return the output dictionary."

            system_message += "\n###\n"
            system_message += "Example:\nInput: Research Scientist at Amazon.\nOutput: {company name: Amazon, job title: Research Scientist, level: None, corporate: None, requirements: None, location: None}"
            system_message += "\n###\n"

            return system_message

        elif mode == 'asking for more information':
            system_message = "Ask the user to provide more information about the following:"
            for key, value in self.key_information.items():
                if value is None:
                    system_message += f" {key},"
            system_message = system_message[:-1] + "."

            return system_message

    def _parse_string_to_dictionary(self, output: str) -> Dict[str, str]:
        # input is like: {company name: Google, job title: Software Engineer}
        # output is like: {"company name": "Google", "job title": "Software Engineer"}
        try:
            res = {}
            pattern = re.compile(r'([\w\s]+): ([\w\s]+)(, |})')
            for match in pattern.finditer(output):
                key = match.group(1)
                value = match.group(2)
                res[key] = value if value != "None" else None
            return res
        except:
            return {}

    def respond_frontend(self, latest_user_input: str) -> Dict[str, str]:
        """
        Respond to user's input.
        @param latest_user_input: the latest user input.
        @return: the response to the user's input.
        """
        if self.streaming_on:
            raise NotImplementedError("Streaming output is not yet supported.")
        else:
            system_message = self._generate_system_message(
                mode='asking for more information')
            response = self.client.chat.completions.create(
                model="glm-3-turbo",
                messages=[
                    {"role": "system", "content": system_message}
                ] + self.chat_history,
                # TODO: Streaming output
            )
            response_text = response.choices[0].message.content
            self.append_agent_output(response_text)
            self._store_chat_message(
                {"role": "assistant", "content": response_text})
            return {"frontend response": response_text, "backend response": None}

    def query_backend(self) -> Dict[str, str]:
        print("-" * 10)
        print("[QUERY BACKEND] key_information", self.key_information)
        return self.key_information

    def _append_user_input(self, user_input: str):
        self.chat_history.append({"role": "user", "content": user_input})

    def append_agent_output(self, agent_output: str):
        self.chat_history.append(
            {"role": "assistant", "content": agent_output})

    def clear_history(self, size=0) -> bool:
        self.chat_history = self.chat_history[:size]
        self._initialize_key_information()
        return True

    def _store_chat_message(self, chat_message):
        """
        Store the chat history in the database.
        """
        sender_role = chat_message["role"]
        content = chat_message["content"]
        is_user_message = True if sender_role == "user" else False
        messsage_object = ChatMessage.objects.create(
            sender=self.user if is_user_message else None,
            receiver=self.user if not is_user_message else None,
            message=content,
            is_user_message=is_user_message
        )
        # save the chat history to the database
        messsage_object.save()

    def _update_summary(self, user_chat_history):
        """
        Update the summary of the chat history.
        """
        if len(user_chat_history) > 0:
            summary = ""
            all_key_words = self.keywords + self.optional_keywords
            all_key_words = ", ".join(all_key_words)
            for message in user_chat_history:
                role = "user" if message.is_user_message else "assistant"
                content = message.message
                summary += f"[{role}]: {content}\n"
            prompt = f"Below is a conversation between a user and an AI assistant. \
    Please read through the entire chat history and provide a concise summary of the key points and main topics \
    discussed by the user. Your summary should focus on the most important details and provide a clear and comprehensive overview of the user's input. if there are informations regarding {all_key_words}, please include them in your summary.\
    Here is the chat history:\n"
            prompt += summary
            prompt += "The summary:"
            print(f'Updating summary:{prompt}')  # DEBUG
            response = self.client.chat.completions.create(
                model="glm-3-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ] + self.chat_history,
                # TODO: Streaming output
            )
            response_text = response.choices[0].message.content
            self.summary = response_text
        else:
            return

    def _switch_history(self):
        """
        Switch chat history based on authentication information.
        """
        print('Switching chat history...')
        # Retrieve chat history for the current user
        user_chat_history = ChatMessage.objects.filter(
            models.Q(sender=self.user) | models.Q(receiver=self.user)
        ).order_by('id')
        # self._update_summary(user_chat_history)
        # Convert chat history to the format used by FrontendAgent
        self.chat_history = []
        # first append the opening sentence
        if self.summary == "":
            self.append_agent_output(DEFAULT_OPENING)
        else:
            self.append_agent_output(self.summary)

        for message in user_chat_history:
            sender_role = "user" if message.is_user_message else "assistant"
            self.chat_history.append({
                "role": sender_role,
                "content": message.message
            })

        # DEBUG
        print(self.chat_history)
