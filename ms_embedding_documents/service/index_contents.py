import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from service.extract_contents import extract_pdf, extract_txt
import random
from dotenv import load_dotenv
from langchain_core.vectorstores import InMemoryVectorStore
from repositories.connection_openai import connection_openai_Embeddings
from repositories.connection_ai_search import connection_ia_search

load_dotenv()

def embedd_documents(conteudo):
    embeddings = connection_openai_Embeddings()
    vectors = embeddings.embed_documents([conteudo])
    return vectors


def indexar_arquivos(arquivo):
    search_client = connection_ia_search()
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

    conteudo_embedding = embedd_documents(conteudo)

    documentos.append({
        "id": str(id),
        "titulo_do_arquivo": titulo,
        "conteudo": conteudo_embedding,
        "data": datetime.utcnow().isoformat() + "Z",
    })

    #print(conteudo_embedding)

    # Indexar os documentos
    if documentos:
        resultado = search_client.upload_documents(documents=documentos)
        print("Documentos indexados:", resultado)
    else:
        print("Nenhum documento para indexar.")

# teste
# arquivo = "C:/Users/leona/brasas-movement-chat-ia/ms_embedding_documents/arquivos_teste/brasas_college.pdf"
# indexar_arquivos(arquivo)