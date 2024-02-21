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
        You are a helpful assistant who can read an interpret email messages.
        You are going to receive emails. 
        The email message are in HTML format.
        Read the email and summarize it using the BLUF format.
        Be sure to identify any action items that indicated in the email.
        Do not make assumptions.
        Do not include any information that is not already in the email message
        ---
        """

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
                {"role": "system", "content": prompt},
                {"role": "user", "content": content},
            ]
        )
        self.logger.debug(completion)
        return completion.choices[0].message.content

    def classify(self, message):
        # Using OpenAI, classify the email message and return a classification
        # of the email message
        prompt = """
        You are my AI assistant. You are responsible for categorizing my email messages
        so that I can quickly retrieve them.
        I will provide you with a taxonomy and description of the taxonomy.
        Label           | Description
        ai-followup     | This is a message that requires a follow-up response from you, or is a request for something other than an email response.
        ai-newsletter   | These are email messages that are marketing style emails, or newsletters. They are typically
        used to sells something or to encourage someone to re-engage with a product or service.
        ai-information  | This is important information to be aware of. It is not an email newsletter.
        You will only provide the label for the message in your response. Do not include
        any additional information. If you can't classify the message, return nothing.
        """

        completion = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Classify:\n" + message["text/html"]},
            ]
        )

        self.logger.debug(completion)
        return completion.choices[0].message.content

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
    