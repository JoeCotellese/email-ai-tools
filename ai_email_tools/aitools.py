import os

import ollama
from dotenv import load_dotenv
from openai import OpenAI


class EmailAI:   
    def __init__(self, logger):
        load_dotenv()
        self.logger = logger
        self.openai = OpenAI()

    def summarize(self, message):
        # Using OpenAI, summarize the email message and return a summary
        # of the email message
        self.logger.info("Summarizing the email message")
        self.logger.debug(message["text/html"])
        prompt = """
        You are my AI assistant. You are responsible for helping me
        quickly read and process email messages.
        I will provide you with email messages. You will return
        a summary of the message.
        If there are specific requests or actions for me, please include
        them in the summary message.
        Summarize as markdown bullet points.
        """
        completion = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Summarize" + message["text/html"]},
            ]
        )
        self.logger.debug(completion)
        return completion.choices[0].message.content

    def classify(self, message):
        # Using OpenAI, classify the email message and return a classification
        # of the email message
        classification = ""
        return classification


# class EmailAI:
#     def __init__(self, logger):        
#         self.logger = logger
#         pass

#     def summarize(self, message):
#         # Using OpenAI, summarize the email message and return a summary
#         # of the email message
#         self.logger.info("Summarizing the email message")
#         self.logger.info(message["text/html"])
#         prompt = """
#         You are my AI assistant. You are responsible for helping me
#         quickly read and process messages.
#         Read the information below and then return a summary.
#         If there are specific requests or actions for me, please include
#         them in the summary message.
#         MESSAGE:
#         \n
#         """
#         messages = [
#             {
#                 'role': 'user',
#                 'content': prompt + message["text/html"]
#             }
#         ]
#         response = ollama.chat(model='llama2:7b-chat', messages=messages)
#         return response['message']['content']

#     def classify(self, message):
#         # Using OpenAI, classify the email message and return a classification
#         # of the email message
#         classification = ""
#         return classification
    