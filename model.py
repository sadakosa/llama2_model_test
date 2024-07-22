from mlx_lm import load, generate

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model, self.tokenizer = load(model_name)
    
    def response(self, messages):
        input_ids = self.tokenizer.apply_chat_template(messages,  add_generation_prompt=True)
        prompt = self.tokenizer.decode(input_ids)
        response = generate(self.model, self.tokenizer, max_tokens=1024, prompt=prompt)

        return response



