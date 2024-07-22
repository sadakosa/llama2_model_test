from mlx_lm import load, generate
from model import Model

def main():
    # model_path = "meta-llama/Meta-Llama-3-8B-Instruct"
    # llama3_client = Llama3(model_path)

    # llama3_client.chatbot("you are a child, curious and always looking to ask questions.")


    # Define your model to import
    model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
    model = Model(model_name)


    # Example prompt
    system_input = """
    I will provide you with a text. Follow the instructions below carefully.

    If it is not in english, respond with "(not in english)", followed by translated english text.
    If it has spelling mistakes, respond with "(spelling mistakes)", followed by corrected text.
    If it has no issues, respond with "(no issues)", followed by the text.

    After checking for all the above scenarios, when returning the text, make sure that all text returned is in lowercase. 

    Examples are provided below.
    Input (spelling mistakes): 
    [title] InformationRetrieval [abstract] Forthousandsofyearspeoplehaverealizedtheimportanceofarchivingandfindinginformation. Withtheadventofcomputers, itbecamepossibletostorelargeamountsofinformation; andfindingusefulinformationfromsuchcollectionsbecameanecessity.
    Output (spelling mistakes): 
    (spelling mistakes) 
    [title] information retrieval [abstract] for thousands of years, people have realized the importance of archiving and finding information. with the advent of computers, it became possible to store large amounts of information; and finding useful information from such collections became a necessity. 

    Input (not in english): 
    [title] ÉTICA Y GÉNERO EN LA IA: IDENTIFICAR SESGOS DE GÉNERO EN IA MEDIANTE PENSAMIENTO COMPLEJO [abstract] No abstract available
    Output (not in english): 
    (not in english) 
    [title] ethics and gender in ai: identifying gender biases in ai through complex thinking [abstract] no abstract available

    Input (no issues):
    [title] Artificial intelligence in healthcare: past, present and future [abstract] No abstract available
    Output (no issues):
    (no issues)
    [title] artificial intelligence in healthcare: past, present and future [abstract] no abstract available
    """

    user_input = """
    [title] InformationRetrieval [abstract] Forthousandsofyearspeoplehaverealizedtheimportanceofarchivingandfindinginformation. Withtheadventofcomputers, itbecamepossibletostorelargeamountsofinformation; andfindingusefulinformationfromsuchcollectionsbecameanecessity. ThefieldofInformationRetrieval(IR) wasborninthe1950soutofthisnecessity. Overthelastfortyyears, thefieldhasmaturedconsiderably. SeveralIRsystemsareusedonaneverydaybasisbyawidevarietyofusers. ThisarticleisabriefoverviewofthekeyadvancesinthefieldofInformationRetrieval, andadescriptionofwherethestate-of-the-artisatinthefield
    """

    messages = [
        {"role": "system", "content": system_input}, 
        {"role": "user", "content": user_input}
    ]

    response = model.response(messages)

    # Output the response
    print(response)


    return



if __name__ == "__main__":
    main()