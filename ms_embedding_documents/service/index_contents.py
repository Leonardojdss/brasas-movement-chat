import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from service.extract_contents import extract_pdf, extract_txt
import random
from dotenv import load_dotenv
from repositories.connection_openai import connection_openai_Embeddings
from repositories.connection_ai_search import connection_ia_search
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

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

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False)

    texts = text_splitter.create_documents([conteudo])

    for text in texts:
        
        conteudo_embedding = embedd_documents(text.page_content)

        documentos.append({
            "id": str(random.randint(0, 1000000)),  # Gera um ID aleatório entre 0 e 1.000.000)
            "titulo_do_arquivo": titulo,
            "conteudo": json.dumps(conteudo_embedding),
            "data": datetime.now().isoformat() + "Z",
        })

    # enviar os documentos para ia search
    search_client.upload_documents(documents=documentos)
    print("Documentos indexados com sucesso.")

# teste
arquivo = "C:/Users/leona/brasas-movement-chat-ia/ms_embedding_documents/arquivos_teste/brasas_nossa_missao.pdf"
indexar_arquivos(arquivo)