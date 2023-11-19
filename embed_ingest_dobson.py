from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores.pinecone import Pinecone

from dotenv import load_dotenv
import os

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 90,
    chunk_overlap = 0,
    length_function = len,
    keep_separator = False,
    add_start_index = False,
    strip_whitespace = True,
    separators=['\d+','\n']
)

loader=PyPDFLoader('res/misc/dodson.pdf')

docs=loader.load_and_split(text_splitter=text_splitter)
import re
def valid_content(content):
    c = re.compile('^\d+$')
    found=c.findall(content)
    not_number=len(found)==0
    
    c = re.compile('^[^\s]*$')
    found=c.findall(content)
    has_spaces=len(found)==0
    
    return not_number and has_spaces

new=[doc for doc in docs if valid_content(doc.page_content)]

#print([doc.page_content for doc in docs][0:50])

alpha_index=[i for i in range(0,100) if "1ἄλφα" in new[i].page_content.strip()]
if len(alpha_index)>0:
    alpha_index=alpha_index[0]

new=new[alpha_index:]

embedding=OpenAIEmbeddings()

import pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    environment="eastus-azure"  # find next to API key in console
)
print("initialized pinecone")

if 'dodson' not in pinecone.list_indexes():
    print("creating new index")
    pinecone.create_index('dodson', dimension=1536)
    vectordb = Pinecone.from_documents(new, embedding, index_name='dodson')
    print("created vectordb")
