import os

import ollama
from dotenv import load_dotenv
from openai import OpenAI


class EmailAI:   
    def __init__(self, logger):
        load_dotenv()
        self.logger = logger
        self.openai = OpenAI()
        self.summarizer_system_prompt = """
        You are a helpful assistant who can read an interpret email messages.
        You are going to receive emails. 
        The email message are in HTML format.
        Read the email and summarize it using the BLUF format.
        Be sure to identify any action items that indicated in the email.
        Do not make assumptions.
        Do not include any information that is not already in the email message
        ---
        """
        self.classifier.prompt = """
        You are a helpful assistant who can categorize email. 
        You are going to help me organize my email by suggestion Gmail labels that best suit the email message.

        I am going to give labels and their definitions.

        Labels:
        highpriority  - an email message that has specific action that I need to take on the message. 
        mediumpriority - an email message that is not important for me to act on. It could be information that is reference material.
        bulk - any email that is marketing in nature, such as newsletters, advertisements, or reengagement emails.
        unknown - an email message that does not fit into any of the other categories.
        Do not make assumptions.
        Do not include any information that is not already in the email message
        Only return the label and no other information.
        """

    def summarize(self, message):
        # Using OpenAI, summarize the email message and return a summary
        # of the email message
        self.logger.info("Summarizing the email message")
        self.logger.debug(message["text/html"])

        user_prompt = """
        Subject:
        {0}
        Body:
        {1}
        """

        content = user_prompt.format(message["subject"], message["text/html"])

        completion = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.summarizer_system_prompt},
                {"role": "user", "content": content},
            ]
        )
        self.logger.debug(completion)
        return completion.choices[0].message.content

    def classify(self, message):
        # Using OpenAI, classify the email message and return a classification
        # of the email message
        
        user_prompt = """
        Classify:
        Subject:
        {0}
        Body:
        {1}
        """

        content = user_prompt.format(message["subject"], message["text/html"])

        completion = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.classifier_system_prompt},
                {"role": "user", "content": content},
            ]
        )

        self.logger.debug(completion)
        return completion.choices[0].message.content

