from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do recurso
ENDPOINT = "https://<SEU_ENDPOINT>.search.windows.net"
API_KEY = os.getenv("AZURE_AI_SEARCH_KEY")
INDEX_NAME = "brasas-documents"

def indexar_arquivos(diretorio):
    search_client = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
    documentos = []
    
    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)
        if arquivo.endswith(".txt"):
            conteudo = extrair_txt(caminho)
        elif arquivo.endswith(".pdf"):
            conteudo = extrair_pdf(caminho)
        else:
            print(f"Formato não suportado: {arquivo}")
            continue

        documentos.append({
            "id": str(len(documentos) + 1),
            "titulo": arquivo,
            "conteudo": conteudo,
            "data": datetime.utcnow().isoformat() + "Z",
        })

    # Indexar os documentos
    if documentos:
        resultado = search_client.upload_documents(documents=documentos)
        print("Documentos indexados:", resultado)
    else:
        print("Nenhum documento para indexar.")