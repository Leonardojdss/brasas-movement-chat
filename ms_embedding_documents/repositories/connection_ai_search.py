from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from dotenv import load_dotenv
from datetime import datetime
import os
import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


load_dotenv()

# Configurações do recurso
ENDPOINT = os.getenv("ENDPOINT_AI_SEARCH")
API_KEY = os.getenv("AZURE_AI_SEARCH_KEY")
INDEX_NAME = "brasas-documents"

<<<<<<< HEAD
def indexar_arquivos(arquivo):
    search_client = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
    documentos = []
    
    #extrair titulo do arquivo
    titulo = arquivo.split("/")[-1]

    if arquivo.endswith(".txt"):
        conteudo = extract_txt(arquivo)
    elif arquivo.endswith(".pdf"):
        conteudo = extract_pdf(arquivo)
    else:
        print(f"Formato não suportado: {arquivo}")

    id = random.randint(0, 1000000)  # Gera um ID aleatório entre 0 e 1.000.000

    documentos.append({
        "id": str(id),
        "titulo_do_arquivo": titulo,
        "conteudo": conteudo,
        "data": datetime.utcnow().isoformat() + "Z",
    })

    print(documentos)

=======
# Configurações do recurso
ENDPOINT = os.getenv("ENDPOINT_AI_SEARCH")
API_KEY = os.getenv("AZURE_AI_SEARCH_KEY")
INDEX_NAME = "brasas-documents"

def indexar_arquivos(arquivo):
    search_client = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
    documentos = []

    #extrair titulo do arquivo
    titulo = arquivo.split("/")[-1]
    
    
    if arquivo.endswith(".txt"):
        conteudo = extrair_txt(arquivo)
    elif arquivo.endswith(".pdf"):
        conteudo = extrair_pdf(arquivo)
    else:
        print(f"Formato não suportado: {arquivo}")

    documentos.append({
        "id": str(len(documentos) + 1),
        "titulo": arquivo,
        "conteudo": conteudo,
        "data": datetime.utcnow().isoformat() + "Z",
    })

>>>>>>> refs/remotes/origin/main
    # Indexar os documentos
    if documentos:
        resultado = search_client.upload_documents(documents=documentos)
        print("Documentos indexados:", resultado)
    else:
        print("Nenhum documento para indexar.")

<<<<<<< HEAD
def pesquisar_conteudo_indexado(pergunta):
    search_client = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
    resultado = search_client.search(search_text=pergunta, top=5)
    print("Documentos encontrados:", resultado)

pergunta = "nossa missão"

pesquisar_conteudo_indexado(pergunta)
=======
def pesquisar_conteudo_indexado():
    search_client = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
    resultado = search_client.search(search_text="brasas", top=5)
    print("Documentos encontrados:", resultado)
>>>>>>> refs/remotes/origin/main
