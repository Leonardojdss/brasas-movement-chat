from repositories.connection_ai_search import connection_ia_search
from datetime import datetime
#import os
#import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.extract_contents import extract_pdf, extract_txt
import random
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

def embedd_documents(conteudo):


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

    documentos.append({
        "id": str(id),
        "titulo_do_arquivo": titulo,
        "conteudo": conteudo,
        "data": datetime.utcnow().isoformat() + "Z",
    })

    print(documentos)

    # Indexar os documentos
    if documentos:
        resultado = search_client.upload_documents(documents=documentos)
        print("Documentos indexados:", resultado)
    else:
        print("Nenhum documento para indexar.")