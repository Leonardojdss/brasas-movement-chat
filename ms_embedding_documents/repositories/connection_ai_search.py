from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
import os
from dotenv import load_dotenv
from ms_embedding_documents.repositories.connection_ai_search import extract_txt, extract_pdf

load_dotenv()

#teste
pdf_teste = "C:/Users/leona/brasas-movement-chat-ia/ms-embedding-documents/arquivos_teste/brasas_nossa_missao.pdf"
conteudo = extract_pdf(pdf_teste)
print(conteudo)

# # Configurações do recurso
# ENDPOINT = os.getenv("ENDPOINT_AI_SEARCH")
# API_KEY = os.getenv("AZURE_AI_SEARCH_KEY")
# INDEX_NAME = "brasas-documents"

# def indexar_arquivos(arquivo):
#     search_client = SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(API_KEY))
#     documentos = []
    
    
#     if arquivo.endswith(".txt"):
#         conteudo = extrair_txt(arquivo)
#     elif arquivo.endswith(".pdf"):
#         conteudo = extrair_pdf(arquivo)
#     else:
#         print(f"Formato não suportado: {arquivo}")

#     documentos.append({
#         "id": str(len(documentos) + 1),
#         "titulo": arquivo,
#         "conteudo": conteudo,
#         "data": datetime.utcnow().isoformat() + "Z",
#     })

#     # Indexar os documentos
#     if documentos:
#         resultado = search_client.upload_documents(documents=documentos)
#         print("Documentos indexados:", resultado)
#     else:
#         print("Nenhum documento para indexar.")