


# ======================== INSERTION OPERATIONS ========================

def insert_cleaned_paper(db_client, ss_id, title, abstract, url, search_term=None, num_hops=None):
    if ss_id is None or title is None:
        # print("Invalid paper data")
        # print(ss_id, title, abstract, url)
        return
    
    if abstract is None:
        abstract = "No abstract available"
    
    # print(f"Inserting paper: {ss_id}")
    
    insert_query = """
    INSERT INTO papers (ss_id, title, abstract, url, search_term, num_hops)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (ss_id) DO NOTHING;
    """
    db_client.execute(insert_query, (ss_id, title, abstract, url, search_term, num_hops))
    db_client.commit()

def insert_reference(db_client, ss_id, reference_id):
    # print(f"Inserting reference: {ss_id} -> {reference_id}")
    insert_query = """
    INSERT INTO "references" (ss_id, reference_id)
        VALUES (%s, %s)
        ON CONFLICT (ss_id, reference_id) DO NOTHING;
    """
    db_client.execute(insert_query, (ss_id, reference_id))
    db_client.commit()

def update_is_cleaned(db_client, ss_id):
    update_query = """
    UPDATE papers
    SET is_cleaned = TRUE
    WHERE ss_id = %s;
    """
    db_client.execute(update_query, (ss_id,))
    db_client.commit()

def update_cleaned_papers(db_client, papers):
    from psycopg2.extras import execute_values
    
    # Construct the update query
    update_query = """
    UPDATE papers AS p
    SET clean_title = v.clean_title,
        clean_abstract = v.clean_abstract,
        is_cleaned = v.is_cleaned
    FROM (VALUES %s) AS v(ss_id, clean_title, clean_abstract, is_cleaned)
    WHERE p.ss_id = v.ss_id;
    """
    
    # Execute the batch update
    execute_values(db_client.cur, update_query, papers)
    db_client.commit()


# papers = [
#     ('ss_id_1', 'Cleaned Title 1', 'Cleaned Abstract 1', True),
#     ('ss_id_2', 'Cleaned Title 2', 'Cleaned Abstract 2', True),
#     ('ss_id_3', 'Cleaned Title 3', 'Cleaned Abstract 3', True),
#     # More records
# ]

# ======================== SELECTION OPERATIONS ========================

def get_all_paper_ids(db_client):
    select_query = """
    SELECT id, ss_id, is_processed FROM papers
    ORDER BY id;
    """
    cursor = db_client.execute(select_query)
    return cursor.fetchall()

def get_all_paper_ids_with_params(db_client, search_term, num_hops):
    select_query = """
    SELECT id, ss_id, is_processed 
    FROM papers
    WHERE search_term = %s AND num_hops = %s
    ORDER BY id;
    """
    cursor = db_client.execute(select_query, (search_term, num_hops))
    return cursor.fetchall()

def get_papers_to_clean(db_client, search_term, batch_size):
    select_query = """
    SELECT ss_id, title, abstract, is_cleaned
    FROM papers
    WHERE is_cleaned = FALSE AND search_term = %s
    LIMIT %s;
    """
    cursor = db_client.execute(select_query, (search_term, batch_size))
    return cursor.fetchall()




