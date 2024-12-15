import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from service.extract_contents import extract_pdf, extract_txt
import random
from dotenv import load_dotenv
from repositories.connection_openai import connection_openai_Embeddings
from repositories.connection_postgreSQL import connection_postgreSQL
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

load_dotenv()

def embedd_documents(conteudo):
    embeddings = connection_openai_Embeddings()
    vectors = embeddings.embed_documents([conteudo])
    return vectors[0]


def indexar_arquivos(arquivo):

    USER_POSTGRESQL = os.getenv("USER_POSTGRESQL")
    PASSWORD_POSTGRESQL = os.getenv("PASSWORD_POSTGRESQL")
    ENDPOINT_POSTGRESQL = os.getenv("ENDPOINT_POSTGRESQL")

    conn, cur = connection_postgreSQL(USER_POSTGRESQL, PASSWORD_POSTGRESQL, ENDPOINT_POSTGRESQL)
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
            "id": datetime.now().strftime("%d%m%Y%H%M%S"),  # Gera um ID com o formato dia, mês, ano, hora, minuto, segundo
            "titulo_do_arquivo": titulo,
            "conteudo": json.dumps(conteudo_embedding)
            })

    # # enviar os documentos para ia search
    # search_client.upload_documents(documents=documentos)
    # print("Documentos indexados com sucesso.")

    # inserir os documentos no banco de dados postgresql com vector extension   
    for documento in documentos:
        try:
            cur.execute(
                f"INSERT INTO brasas_vector_db (id, titulo, conteudo) VALUES ('{documento['id']}', '{documento['titulo_do_arquivo']}', '{documento['conteudo']}')"
            )
            conn.commit()
        except Exception as e:
            print("Documentos indexados não foram salvos no banco, erro: ", e)
    print("Documentos indexados com sucesso.")

# teste
arquivo = "C:/Users/leona/brasas-movement-chat-ia/ms_embedding_documents/arquivos_teste/brasas_nossa_missao.pdf"
indexar_arquivos(arquivo)