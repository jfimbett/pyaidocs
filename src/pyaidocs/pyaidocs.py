
import logging
logging.basicConfig(level=logging.INFO)
from pyaidocs.options import Options
from pyaidocs.pyaipdfs import pdf_to_text
import pandas as pd
import json

def talk_to_gpt(user, options = Options(), temperature=0.0):
    response = options.client.chat.completions.create(
        model= options.model,
        messages=[{"role": "user", "content": user},
                  {"role": "system", "content": 
    """
   You are a financial assistant specialised in Private Equity. Use \$ instead of $ and \% instead of %.
    """
                   }],
        temperature=temperature,
        seed=42
    )
    return response.choices[0].message.content

def ask_question_pdf(pdf_path, user_question, options=Options(), password=None):
    text_pages, tables, message = pdf_to_text(pdf_path, password=password)
    if not text_pages:
        return message
    text = ' '.join(text_pages)
    user = f"{user_question} {text}"
    response = talk_to_gpt(user, options=options, temperature=0.0)
    return response

def is_last_element(tree):
    # is last element if its a dictionary but no elements are dictionaries
    if isinstance(tree, dict):
        for key, value in tree.items():
            if isinstance(value, dict):
                return False
        return True
    else:
        return True
    
def traverse_tree(tree, key_before ='' , result=None):
    
    if result is None:
        result = []

    if not is_last_element(tree):
        for key, value in tree.items():
            traverse_tree(value, key_before=key_before+' '+key, result=result)  
    else:

        # convert to pandas dataframe if tree is a dictionary
        table_ = tree
        if isinstance(tree, dict):

            # we need to make all the values the same length
            elements = [len(value) for value in tree.values() if type(value) == list]
            if len(elements) > 0:
                max_len = max(elements)
                for key, value in tree.items():
                    if type(value) != list:
                        continue

                    if len(value) < max_len:
                        tree[key] = value + ['']*(max_len-len(value))

            try:
                table_ = pd.DataFrame(tree).T
            except:
                table_ = pd.DataFrame(tree, index=[0])


        result.append({key_before: table_})

    return result

def retrieve_key_variables_text_with_page(pdf_path, key_variables, options=Options(), password=None):
    prompt = f""" 
            Identify the following information, return a json string 
            with the exact keys as below.

            {key_variables}       

            Return only a json string with the first character being '{{ and the last character being '}}'.  

            I need to load the string using python's json.loads() function, so make sure the string is in the correct format.   
            """
    text_pages, tables, message = pdf_to_text(pdf_path, password=password)
    # dictionary to store where the key variables are found, they might be in more than one page 
    key_variables_found = {k : {'values' : [], 'pages' : []} for k in key_variables}
    for page_num, text in enumerate(text_pages):
        # use talk_to_gpt to find the key variables in the text
        user = f"{prompt} {text}"
        response = talk_to_gpt(user, options=options, temperature=0.0)
        # convert to dictionary
        response_dict = response.replace('\n', '').replace('\r', '')
        # load from json 
        response_dict = json.loads(response_dict)

        for key in key_variables: 
            # check if the key is in the response and its value 
            if key in response_dict:
                value = response_dict[key]
                # if value is different from '' or N/A we add the page 
                if value not in ['', 'N/A', 'NA', '-']:
                    dict_ = key_variables_found[key]
                    dict_pages = dict_['pages']
                    dict_values = dict_['values']
                    dict_pages.append(page_num+1) # because we started at zero
                    dict_values.append(value)
                    dict_['pages'] = dict_pages
                    dict_['values'] = dict_values
                    key_variables_found[key] = dict_
        
    return key_variables_found



def retrieve_key_variables_text(pdf_path, key_variables, options=Options(), password=None):
            prompt = f""" 
            Identify the following information, return a json string 
            with the exact keys as below.

            {key_variables}       

            Return only a json string with the first character being '{{ and the last character being '}}'.  

            I need to load the string using python's json.loads() function, so make sure the string is in the correct format.   
            """

            response = ask_question_pdf(pdf_path, prompt, options=options, password=None)
            # to json 
            response_dict = response.replace('\n', '').replace('\r', '')
            # load from json
            response_dict = json.loads(response_dict)
            return response_dict

def talk_to_gpt(user, options = Options(), temperature=0.0):
    response = options.client.chat.completions.create(
        model= options.model,
        messages=[{"role": "user", "content": user},
                  {"role": "system", "content": 
    """
   You are a financial assistant specialised in Private Equity. Use \$ instead of $ and \% instead of %.
    """
                   }],
        temperature=temperature,
        seed=42
    )
    return response.choices[0].message.content