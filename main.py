# from mlx_lm import load, generate
# from mlx_model import MlxModel
from groq_client import GroqClient
from togetherai_client import TogetheraiClient
# from mistake_checker import MistakeChecker
# from call_google import google_correction

import json
import time
from global_methods import get_text_from_file, load_yaml_config, get_search_terms
from global_methods import save_checkpoint, load_checkpoint

from logger.logger import Logger
from db.db_client import DBClient
from db import db_operations


# =============================================================================
# LLM MODELS
# =============================================================================

# MLX MODEL
def start_mlx_model(logger):
    # Define your model to import
    model_name = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
    mlx_model = MlxModel(model_name, logger)

    return mlx_model

def query_mlx_model(mlx_model, system_input, user_input):
    messages = [
        {"role": "system", "content": system_input}, 
        {"role": "user", "content": user_input}
    ]

    response = mlx_model.query(messages)
    print(response)
    
    return json.loads(response)

# TOGETHERAI MODEL
def start_togetherai_model(logger):
    config = load_yaml_config('config/config.yaml')
    togetherai_api_key = config['TOGETHERAI_API_KEY']
    togetherai_client = TogetheraiClient(togetherai_api_key, logger)

    return togetheraiClient

def query_togetherai_model(togetherai_client):
    response = togetherai_client.run_query()

    return response


# GROQ MODEL
def start_groq_model(logger):
    config = load_yaml_config('config/config.yaml')
    groq_api_key = config['GROQ_API_KEY']
    groq_client = GroqClient(groq_api_key, logger)

    return groq_client

def query_groq_model(groq_client, system_input, user_input):
    # system_input = get_text_from_file("./resources/system_input.txt")
    # user_input = get_text_from_file("./resources/test_prompt_4.txt")

    # print("system_input: ", system_input)
    # print("user_input: ", user_input)
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
    
    if "error" in dict_response:
        print(f"Error in response: {dict_response['error']}")
        return None
    
    cleaned_paper = (ss_id, dict_response['title'], dict_response['abstract'], True)
    concept_edges = (dict_response['key_concepts'], dict_response['concept_weights'])

    response = {
        'cleaned_paper': cleaned_paper, # (ss_id, 'Cleaned Title 1', 'Cleaned Abstract 1', is_cleaned=True)
        'concept_edges': concept_edges # (key_concepts=['concept1','concept2'], "concept_weights"=[10,5])
    }

    print("concept_edges: ", concept_edges)
    # dict_keys(['outcome', 'title', 'abstract', 'key concepts', 'weights'])
    # (ss_id, 'Cleaned Title 1', 'Cleaned Abstract 1', is_cleaned=True)
    # (key_concepts=['concept1','concept2'], "concept_weights"=[10,5])
    return response

# def clean_data(logger, model_obj, dbclient, search_term, batch_size):
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




def clean_data(logger, model_obj, dbclient, dbclient_read, search_term, batch_size, search_term_index, cleaned_papers_checkpoint, concept_edges_checkpoint):
    cleaned_papers_list = cleaned_papers_checkpoint
    concept_edges_list = concept_edges_checkpoint

    while True:
        # get papers from db (ss_id, title_cleaned, abstract_cleaned, is_cleaned)
        papers = db_operations.get_papers_to_clean(dbclient_read, search_term, batch_size)

        if not papers:
            break  # No more papers to clean

        # clean papers
        for paper in papers:
            logger.log_message(f"Cleaning paper: {paper}")
            cleaned_paper_response = clean_paper(logger, model_obj, paper)
            if cleaned_paper_response is None:
                continue

            cleaned_paper = cleaned_paper_response['cleaned_paper']
            cleaned_papers_list.append(cleaned_paper)  # cleaned paper is a tuple ('ss_id_1', 'Cleaned Title 1', 'Cleaned Abstract 1', True)

            concept_edges = cleaned_paper_response['concept_edges']
            concept_edges_list.append(concept_edges)  # concept_edges is a tuple (['concept1','concept2'], [10,5])
    
        # ============== batch insert concepts and concept_edges ==============
        unique_concepts = {concept for edges in concept_edges_list for concept in edges[0]}
        # unique_concepts = {d[1] for d in concept_edges_list} # Extract unique concepts
        concept_id_map = db_operations.batch_insert_concepts(dbclient, unique_concepts) # Batch insert unique concepts and retrieve their IDs (data format returned: {concept: concept_id})
        # concept_edges = [(concept_id_map[d[1]], d[0], d[2], d[3]) for d in concept_edges_list] # Prepare data for paper_concept_edges table (concept_id, ss_id, weight, is_cleaned)
        # Prepare data for paper_concept_edges table
        concept_edges = []
        for paper, edges in zip(cleaned_papers_list, concept_edges_list):
            ss_id = paper[0]
            concepts, weights = edges
            for concept, weight in zip(concepts, weights):
                concept_id = concept_id_map[concept]
                concept_edges.append((concept_id, ss_id, weight))
        # print("Concept Edges:", concept_edges)
        # print("unique_concepts: ", unique_concepts)
        # print("concept_id_map: ", concept_id_map)
        # print("concept_edges: ", concept_edges)
        db_operations.batch_insert_concept_edges(dbclient, concept_edges) # Batch insert into paper_concept_edges table

        # ============== update papers as a batch ==============
        db_operations.batch_update_cleaned_papers(dbclient, cleaned_papers_list)

        # =================== save checkpoint ==================
        save_checkpoint(search_term_index, cleaned_papers_list, concept_edges_list)
        print(f"Checkpoint saved for search term: {search_term_index}")
        cleaned_papers_list = []


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

    dbclient = DBClient("postgres", psql_user, psql_password, psql_host, psql_port)
    dbclient_read = DBClient("postgres", psql_user, psql_password, psql_read_host, psql_port)

    # create tables
    db_operations.create_concepts_table(dbclient)
    db_operations.create_paper_concept_table(dbclient)

    # =============================================
    # SEARCH TERMS SETTINGS
    # =============================================
    search_terms = get_search_terms() # there are 460 search terms in total
    start_term_input = 0
    start_term, cleaned_papers_checkpoint, concept_edges_checkpoint = load_checkpoint(start_term_input)
    end_term = 4
    num_hops = 0
    batch_size = 300

    # =============================================
    # LLM MODELS
    # =============================================
    llm_type = "groq"
    
    if llm_type == "mlx":
        llm = start_mlx_model(logger)
    elif llm_type == "tgtai":
        llm = start_togetherai_model(logger)
    else:
        llm = start_groq_model(logger)

    model_obj = [llm, llm_type]

    # =============================================
    # TEST TOGETHERAI MODEL
    # =============================================
    # response = query_togetherai_model(llm)
    # query_groq_model(llm, "system_input", "user_input")


    # =============================================
    # CLEAN PAPERS
    # =============================================

    # for idx, search_term in enumerate(search_terms[start_term:end_term], start=start_term):
    #     logger.log_message(f"Cleaning papers for search term: {search_term[0]}")
    #     print(f"Cleaning papers for search term: {search_term[0]}")
    #     clean_data(logger, model_obj, db_client, search_term[0], batch_size)
    
    for idx, search_term in enumerate(search_terms[start_term:end_term], start=start_term):
        logger.log_message(f"Cleaning papers for search term: {search_term[0]}")
        print(f"Cleaning papers for search term: {search_term[0]}")
        clean_data(logger, model_obj, dbclient, dbclient_read, search_term[0], batch_size, idx, cleaned_papers_checkpoint, concept_edges_checkpoint)

        # Reset checkpoint for the next search term
        cleaned_papers_checkpoint = []
        concept_edges_checkpoint = []


if __name__ == "__main__":
    main()