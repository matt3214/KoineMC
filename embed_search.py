from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone

from dotenv import load_dotenv

load_dotenv()

embedding=OpenAIEmbeddings()

import pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    environment="eastus-azure"  # find next to API key in console
)
print("initialized pinecone")

if 'term-lib' in pinecone.list_indexes():
    # connect to index
    vectordb = Pinecone.from_existing_index(embedding=embedding,index_name='term-lib')
    print("connected to existing index")
    
    print(vectordb.similarity_search('advancements.nether.brew_potion.description": "Brew a Potion',k=3))
   