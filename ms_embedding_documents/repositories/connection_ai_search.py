from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from dotenv import load_dotenv
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.extract_contents import extract_pdf, extract_txt

load_dotenv()

# Configurações do recurso
ENDPOINT = os.getenv("ENDPOINT_AI_SEARCH")
API_KEY = os.getenv("AZURE_AI_SEARCH_KEY")
INDEX_NAME = "brasas-documents"

def connection_ia_search():
    search_client = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
    return search_client

