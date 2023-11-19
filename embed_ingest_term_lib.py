from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores.pinecone import Pinecone

from dotenv import load_dotenv

load_dotenv()

import pandas as pd
import openai

"""
Read a CSV file with a column of text, split the text into tokens, get text embeddings using OpenAI,
and write the embeddings to a Pandas DataFrame.

Args:
    csv_file (str): Path to the CSV file.
    column_name (str): Name of the column containing the text.
    max_length (int, optional): Maximum length of each text. Defaults to 512.

Returns:
    pandas.DataFrame: DataFrame with the text embeddings.
"""
# Read the CSV file into a DataFrame
df = pd.read_csv('res/term_library/term_library_unique.csv')
lines=df.to_csv(index=False).split('\n')

from langchain.docstore.document import Document
import datetime
generation_date=datetime.datetime.now().strftime("%Y-%m-%d")

docs=[Document(page_content=line,metadata={'source':'term_library_unique.csv','generated':generation_date}) for line in lines]

# import re
# def valid_content(content):
#     c = re.compile('^\d+$')
#     found=c.findall(content)
#     not_number=len(found)==0
    
#     c = re.compile('^[^\s]*$')
#     found=c.findall(content)
#     has_spaces=len(found)==0
    
#     return not_number and has_spaces

#new=[doc for doc in docs if valid_content(doc.page_content)]

#print([doc.page_content for doc in docs][0:50])

# alpha_index=[i for i in range(0,100) if "1ἄλφα" in new[i].page_content.strip()]
# if len(alpha_index)>0:
#     alpha_index=alpha_index[0]

# new=new[alpha_index:]

embedding=OpenAIEmbeddings()

import pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    environment="eastus-azure"  # find next to API key in console
)
print("initialized pinecone")

if 'term-lib' not in pinecone.list_indexes():
    print("creating new index")
    pinecone.create_index('term-lib', dimension=1536)
    vectordb = Pinecone.from_documents(docs, embedding, index_name='term-lib')
    print("created vectordb")
