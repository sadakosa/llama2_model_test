from mlx_lm import load, generate
from mlx_model import MlxModel
from global_methods import get_text_from_file, load_yaml_config

from groq_client import GroqClient
from mistake_checker import MistakeChecker
from call_google import google_correction
import json
import time

def mlx_model(system_input, user_input):
    # Define your model to import
    model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
    model = MlxModel(model_name)

    messages = [
        {"role": "system", "content": system_input}, 
        {"role": "user", "content": user_input}
    ]

    response = model.response(messages)

    # Output the response
    print(response)


    return json.loads(response)


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


    return response

def corrector(system_input, user_input, case, retries=3):
    for attempt in range(retries):
        try:
            if case == 1 or case == 2:
                # first or second mistake, will check google
                google_corrected = google_correction(user_input)
                return google_corrected
            elif case == 3:
                print("groq")
                # third mistake, will check groq
                llm_corrected = groq_model(system_input, user_input)
                corrected_string = f"[title] {llm_corrected['title']} [abstract] {llm_corrected['abstract']}"
                return corrected_string
            else:
                print("mlx")
                # last mistake, will check mlx
                mlx_corrected_json = mlx_model(system_input, user_input)
                print("mlx_corrected_json")
                print(mlx_corrected_json)
                mlx_corrected = json.loads(mlx_corrected_json)
                print(mlx_corrected)
                corrected_string = f"[title] {mlx_corrected['title']} [abstract] {mlx_corrected['abstract']}"
                return corrected_string
        except Exception as e:
            print(f"Attempt {attempt+1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("Max retries reached. Moving to next step.")
    return user_input  # Return the original input if all retries fail



def main():

    system_input = get_text_from_file("./resources/system_input.txt")
    user_input = get_text_from_file("./resources/test_prompt_5.txt")

    checker = MistakeChecker()
    is_mistake = checker.check_if_mistake(user_input)
    
    counter = 1
    max_count = 5
    while counter < max_count and is_mistake:
        is_mistake = checker.check_if_mistake(user_input)
        user_input = corrector(system_input, user_input, counter)
        counter += 1

    # mlx_model()
    # groq_model()


if __name__ == "__main__":
    main()