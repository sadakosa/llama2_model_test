import os
from groq import Groq
import json


class GroqClient:
    def __init__(self, api_key_input, logger):
        try:
            self.client = Groq(api_key=api_key_input)
            self.logger = logger
            print("Groq client initialized")
        except Exception as e:
            print(f"Error initializing Groq client: {e}")
            raise

    # def query(self, user_input, temperature=0.34):
    #     try:
    #         chat_completion = self.client.chat.completions.create(
    #             messages=user_input,
    #             model="llama3-8b-8192",
    #             temperature=temperature,
    #             max_tokens=1024,
    #             stream=False,
    #             response_format={"type": "json_object"},
    #         )
    #         response = chat_completion.choices[0].message.content
    #         response_json = json.loads(response)
    #         # print(response_json)
    #         return response_json
    #     except Exception as e:
    #         print(f"Error during query: {e}")
    #         self.logger.log_message("Error during query: {e}")
    #         return "An error occurred during the query. Please try again later."


    def query(self, user_input, temperature=0.34):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=user_input,
                model="llama3-8b-8192",
                temperature=temperature,
                max_tokens=1024,
                stream=False,
                response_format={"type": "json_object"},
            )
            response = chat_completion.choices[0].message.content
            
            try:
                response_json = json.loads(response)
                return response_json
            except json.JSONDecodeError as json_err:
                print(f"JSON decode error: {json_err}")
                self.logger.log_message(f"JSON decode error: {json_err}")
                return {"error": "Invalid JSON response"}
        except Exception as e:
            print(f"Error during query: {e}")
            self.logger.log_message(f"Error during query: {e}")
            return {"error": "An error occurred during the query. Please try again later."}


    # def chatbot(self, system_instructions=""):
    #     conversation = [{"role": "system", "content": system_instructions}]
    #     while True:
    #         user_input = input("User: ")
    #         if user_input.lower() in ["exit", "quit"]:
    #             print("Exiting the chatbot. Goodbye!")
    #             break
    #         response, conversation = self.get_response(user_input, conversation)
    #         print(f"Assistant: {response}")










# import torch
# import transformers

# class Llama3:
#     def __init__(self, model_path):
#         self.model_id = model_path
#         self.pipeline = transformers.pipeline(
#             "text-generation",
#             model=self.model_id,
#             model_kwargs={
#                 "torch_dtype": torch.float16,
#                 "quantization_config": {"load_in_4bit": True},
#                 "low_cpu_mem_usage": True,
#             },
#         )
#         self.terminators = [
#             self.pipeline.tokenizer.eos_token_id,
#             self.pipeline.tokenizer.convert_tokens_to_ids(""),
#         ]
  
#     def get_response(
#           self, query, message_history=[], max_tokens=4096, temperature=0.6, top_p=0.9
#       ):
#         user_prompt = message_history + [{"role": "user", "content": query}]
#         prompt = self.pipeline.tokenizer.apply_chat_template(
#             user_prompt, tokenize=False, add_generation_prompt=True
#         )
#         outputs = self.pipeline(
#             prompt,
#             max_new_tokens=max_tokens,
#             eos_token_id=self.terminators,
#             do_sample=True,
#             temperature=temperature,
#             top_p=top_p,
#         )
#         response = outputs[0]["generated_text"][len(prompt):]
#         return response, user_prompt + [{"role": "assistant", "content": response}]
    

  
# if __name__ == "__main__":
#     bot = Llama3("meta-llama/Meta-Llama-3-8B-Instruct")
#     bot.chatbot("you are a child, curious and always looking to ask questions.")