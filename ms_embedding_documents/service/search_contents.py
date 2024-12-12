from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField

def pesquisar_conteudo_indexado(pergunta):
    search_client = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
    resultado = search_client.search(search_text=pergunta, top=5)
    print("Documentos encontrados:", resultado)

pergunta = "nossa missão"

pesquisar_conteudo_indexado(pergunta)
