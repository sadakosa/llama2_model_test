from mlx_lm import load, generate
from mlx_model import MlxModel
from global_methods import get_text_from_file, load_yaml_config, get_search_terms

from groq_client import GroqClient
from mistake_checker import MistakeChecker
from call_google import google_correction
import json
import time

from logger.logger import Logger
from db.db_client import DBClient
from db import db_operations


# =============================================================================
# LLM MODELS
# =============================================================================

def start_mlx_model(logger):
    # Define your model to import
    model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
    mlx_model = MlxModel(model_name, logger)

    return mlx_model

def query_mlx_model(model, system_input, user_input):
    messages = [
        {"role": "system", "content": system_input}, 
        {"role": "user", "content": user_input}
    ]

    response = model.query(messages)
    print(response)
    
    return json.loads(response)



def start_groq_model(logger):
    config = load_yaml_config('config/config.yaml')
    groq_api_key = config['GROQ_API_KEY']
    groq_client = GroqClient(groq_api_key, logger)

    return groq_client

def query_groq_model(groq_client, system_input, user_input):
    messages = [
        {"role": "system", "content": system_input}, 
        {"role": "user", "content": user_input}
    ]

    response =  groq_client.query(messages)
    print(response)

    return response



# =============================================================================
# MAIN
# =============================================================================

def clean_paper(logger, model_obj, paper):
    # =============== get paper details ===============
    ss_id = paper[0]
    title = paper[1]
    abstract = paper[2]

    system_input = get_text_from_file("./resources/system_input.txt")
    # user_input = get_text_from_file("./resources/test_prompt_4.txt")
    user_input_dict = {
        "title": title,
        "abstract": abstract
    }
    user_input_json = json.dumps(user_input_dict)


    # ================== clean paper ==================
    if model_obj[1] == "mlx":
        dict_response = query_mlx_model(model_obj[0], system_input, user_input_json)
    else:
        dict_response = query_groq_model(model_obj[0], system_input, user_input_json)

    response = (ss_id, dict_response['title'], dict_response['abstract'], True)
    return response

def clean_data(logger, model_obj, dbclient, search_term, batch_size):
    while True:
        # get papers from db (ss_id, title_cleaned, abstract_cleaned, is_cleaned)
        papers = db_operations.get_papers_to_clean(dbclient, search_term, batch_size)

        if not papers:
            break  # No more papers to clean

        # clean papers
        cleaned_papers = []
        for paper in papers:
            logger.log_message(f"Cleaning paper: {paper}")
            cleaned_paper = clean_paper(logger, model_obj, paper)
            cleaned_papers.append(cleaned_paper) # cleaned paper is a tuple ('ss_id_1', 'Cleaned Title 1', 'Cleaned Abstract 1', True)

        # save papers as a batch
        db_operations.update_cleaned_papers(dbclient, cleaned_papers)

        # Check if the number of papers fetched is less than the batch size
        if len(papers) < batch_size:
            break  # No more papers to clean in this search term


def main():
    logger = Logger() # To log last try

    # =============================================
    # POSTGRESQL DATABASE CONNECTION
    # =============================================

    config = load_yaml_config('config/config.yaml')
    rds_db = config['RDS_DB']
    
    # PostgreSQL database connection details
    psql_user = config['PSQL_USER'] if rds_db else config['LOCAL_PSQL_USER']
    psql_password = config['PSQL_PASSWORD'] if rds_db else config['LOCAL_PSQL_PASSWORD']
    psql_host = config['PSQL_HOST'] if rds_db else config['LOCAL_PSQL_HOST']
    psql_port = config['PSQL_PORT'] if rds_db else config['LOCAL_PSQL_PORT']
    psql_read_host = config['PSQL_READ_HOST'] if rds_db else config['LOCAL_PSQL_HOST']

    db_client = DBClient("postgres", psql_user, psql_password, psql_host, psql_port)
    db_read_client = DBClient("postgres", psql_user, psql_password, psql_read_host, psql_port)

    # =============================================
    # SEARCH TERMS SETTINGS
    # =============================================

    search_terms = get_search_terms() # there are 460 search terms in total
    start_term = 0
    end_term = 6
    num_hops = 0

    # =============================================
    # LLM MODELS
    # =============================================
    llm_type = "mlx"
    
    if llm_type == "mlx":
        llm = start_mlx_model(logger)
    else: 
        llm = start_groq_model(logger)

    model_obj = [llm, llm_type]

    # =============================================
    # CLEAN PAPERS
    # =============================================

    for search_term in search_terms[start_term:end_term]:
        logger.log_message(f"Cleaning papers for search term: {search_term[0]}")
        print(f"Cleaning papers for search term: {search_term[0]}")
        clean_data(logger, model_obj, db_client, search_term[0], 10) 

if __name__ == "__main__":
    main()