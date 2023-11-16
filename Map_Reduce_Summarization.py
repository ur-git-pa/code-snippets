from dotenv import load_dotenv
import os
import pandas as pd
import openai
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate

load_dotenv("Credentials.env")

#openai.api_key = os.getenv('OPEN_AI_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPEN_AI_KEY')


def overall_summary(dataframe,group):
    corpus = '\n'.join(dataframe['Comment'][dataframe['Group']==group].astype(str))

    #####Including overlap
    #llm = OpenAI(temperature=0)

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)

    docs = text_splitter.create_documents([corpus])

    ######### Map Reduce
    map_prompt = '''
******** is a equipment rental company. Your job is to summarize a number of employee comments.
They will be given by region and topic group. Give a general overview of each chunk of comments and the general themes of the corpus.
"{text}"
'''
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

###Summarizing the summary

    combine_prompt = """
Write a 500 word summary of the following employee survey comments delimited by triple backquotes. 
This overview is region specific so avoid talking about location. This is not an overview on how ******** is doing but how this group compares to others within the company.
Give equal commentary to what is working well and what could be improved.
```{text}```
"""
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    summary_chain = load_summarize_chain(llm=OpenAI(temperature=1.1,max_tokens=500),
                                     chain_type='map_reduce',
                                     map_prompt=map_prompt_template,
                                     combine_prompt=combine_prompt_template,
#                                      verbose=True
                                    )

    return summary_chain.run(docs)

def positive_theme(dataframe,group):

    corpus = '\n'.join(dataframe['Comment'][(dataframe['Group']==group)&(dataframe['Score']>=8)].astype(str))

    #####Including overlap
    #llm = OpenAI(temperature=0)

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)

    docs = text_splitter.create_documents([corpus])

    #### First Phase prompt
    map_prompt = '''
Your job is to summarize a number of employee comments. 
They will be given by region and topic group. Note the positive themes of each chunk of comments and take note of how many comments relate to each theme.
The chunk of comments is denoted by the the double quotes.
"{text}"
'''
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

###Summarizing the summary

    combine_prompt = """
Return the top 5 numbered themes sorted by the number of comments associated with the theme of the following text delimited by triple backquotes. 
Each theme should be 2-3 setences long and include the count of the comments that are part of each theme.
```{text}```
Example format:
1. THEME 1 (Number of comments related to THEME 1):
2. THEME 2 (Number of comments related to THEME 2):
3. THEME 3 (Number of comments related to THEME 3):
4. THEME 4 (Number of comments related to THEME 4):
5. THEME 5 (Number of comments related to THEME 5):
"""
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    summary_chain = load_summarize_chain(llm=OpenAI(temperature=1.1,max_tokens=500),
                                     chain_type='map_reduce',
                                     map_prompt=map_prompt_template,
                                     combine_prompt=combine_prompt_template,
#                                      verbose=True
                                    )

    return summary_chain.run(docs)

def negative_theme(dataframe,group):

    corpus = '\n'.join(dataframe['Comment'][(dataframe['Group']==group)&(dataframe['Score']<5)].astype(str))

    #####Including overlap
    #llm = OpenAI(temperature=0)

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)

    docs = text_splitter.create_documents([corpus])

    #### First Phase prompt
    map_prompt = '''
Your job is to summarize a number of employee comments. 
They will be given by region and topic group. Note the negative themes of each chunk of comments and take note of how many comments relate to each theme.
The chunk of comments is denoted by the the double quotes.
"{text}"
'''
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

###Summarizing the summary

    combine_prompt = """
Return the top 5 numbered themes sorted by the number of comments associated with the theme of the following text delimited by triple backquotes. 
Each theme should be 2-3 setences long and include the count of the comments that are part of each theme.
```{text}```
Example format:
1. THEME 1 (THEME 1 Comment Count): 2-3 setence explanation
2. THEME 2 (THEME 2 Comment Count): 2-3 setence explanation
3. THEME 3 (THEME 3 Comment Count): 2-3 setence explanation
4. THEME 4 (THEME 4 Comment Count): 2-3 setence explanation
5. THEME 5 (THEME 5 Comment Count): 2-3 setence explanation
"""
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    summary_chain = load_summarize_chain(llm=OpenAI(temperature=1.1,max_tokens=500),
                                     chain_type='map_reduce',
                                     map_prompt=map_prompt_template,
                                     combine_prompt=combine_prompt_template,
#                                      verbose=True
                                    )
    return summary_chain.run(docs)
