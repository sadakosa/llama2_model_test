from mlx_lm import load, generate

class MlxModel:
    def __init__(self, model_name, logger):
        self.model_name = model_name
        self.model, self.tokenizer = load(model_name)
        self.logger = logger
    
    def query(self, messages):
        try:
            input_ids = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True)
            prompt = self.tokenizer.decode(input_ids)

            # self.logger.info(f"Generated prompt: {prompt}")

            response = generate(self.model, self.tokenizer, max_tokens=1024, prompt=prompt)

            # self.logger.info(f"Generated response: {response}")

            return response

        except Exception as e:
            # Log the error
            self.logger.error(f"Error in response generation: {e}")
            # Optionally, you can also return an error message or handle the error appropriately
            return {"error": "An error occurred while generating the response."}



