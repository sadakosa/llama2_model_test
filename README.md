# llama2_model_test
To test the llama model


## 

Using
- https://blog.shadabmohammad.com/run-llama3-on-your-m1-pro-macbook-08388b4b98e1
- https://huggingface.co/mlx-community/Meta-Llama-3-70B-Instruct-4bit
- https://github.com/GusLovesMath/Llama3_MacSilicon/blob/main/Llama3_MacSilicom_Example.ipynb
- https://guslovesmath.medium.com/efficiently-running-meta-llama-3-on-mac-silicon-m1-m2-m3-61585c9bc741

llama3-8b-instruct models
- https://ollama.com/koesn/llama3-8b-instruct
- https://ollama.com/lyfuci/meta-llama-3-8b-instruct





## How to do this
- Because I am lacking time, I need to create a filter to only clean the data that needs to be cleaned. 
- https://stackoverflow.com/questions/13928155/spell-checker-for-python << using this
- then put the data through groq or local llama3 -> to figure out how to do that on ec2

- word list https://www.mit.edu/~ecprice/wordlist.10000


### Google as a spell checker
https://stackoverflow.com/questions/40260655/does-google-allow-businesses-to-use-did-you-mean-feature-as-an-api-i-would-l
- less than 2048 characters
- 
'''
<script async src="https://cse.google.com/cse.js?cx=871059d55d47741ac">
</script>
<div class="gcse-search"></div>
'''

https://github.com/LuanRT/google-this << THE BEST REPO >>

## Miscellaneous
// I can't run the code in the link below as I don't have a GPU
https://medium.com/@manuelescobar-dev/implementing-and-running-llama-3-with-hugging-faces-transformers-library-40e9754d8c80


## Postgres on Mac
"""
pg_ctl -D /usr/local/var/postgres start >> The installer usually initializes and starts the PostgreSQL server automatically. If not, you can manually start the server using the following command in Terminal:


ALTER TABLE papers
ADD COLUMN clean_title TEXT,
ADD COLUMN clean_abstract TEXT;

ALTER TABLE papers
ADD CONSTRAINT clean_columns_not_null_if_cleaned
CHECK (
    (is_cleaned IS NOT TRUE) OR
    (clean_title IS NOT NULL AND clean_abstract IS NOT NULL)
);


"""
