from mlx_lm import load, generate
from model import Model
from global_methods import get_text_from_file, load_yaml_config, remove_punctuation

from groq_client import GroqClient
from mistake_checker import MistakeChecker

def mlx_model(system_input, user_input):
    # Define your model to import
    model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
    model = Model(model_name)

    

    messages = [
        {"role": "system", "content": system_input}, 
        {"role": "user", "content": user_input}
    ]

    response = model.response(messages)

    # Output the response
    print(response)


    return


def groq_model(system_input, user_input):
    config = load_yaml_config('config/config.yaml')
    groq_api_key = config['GROQ_API_KEY']
    groq_client = GroqClient(groq_api_key)

    messages = [
        {"role": "system", "content": system_input}, 
        {"role": "user", "content": user_input}
    ]

    response =  groq_client.query(messages)    

    # Output the response
    print(response)


    return




def main():

    system_input = get_text_from_file("./resources/system_input.txt")
    user_input = get_text_from_file("./resources/test_prompt_4.txt")

    checker = MistakeChecker()
    print(checker.check_if_mistake(user_input))

    # mlx_model()
    # groq_model()


if __name__ == "__main__":
    main()