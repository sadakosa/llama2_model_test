import os
from together import Together


class TogetheraiClient:
    def __init__(self, api_key_input, logger):
        try:
            self.client = Together(api_key=api_key_input)
            self.logger = logger
        except Exception as e:
            print(f"Error initializing Together AI client: {e}")
            raise

    def query(self):
        print("Running query")
        stream = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
            messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
            stream=True,
        )
        print("Ran query")

        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="", flush=True)