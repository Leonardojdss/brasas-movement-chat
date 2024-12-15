import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from repositories.connection_postgreSQL import connection_postgreSQL
from repositories.connection_openai import connection_openai_Embeddings
import os
import json

# Converter a pergunta em um vetor
def embedd_pergunta(pergunta):
    embeddings = connection_openai_Embeddings()
    vectors = embeddings.embed_documents([pergunta])
    return vectors[0]

# Realizar a pesquisa de conteúdo indexado
def pesquisar_conteudo_indexado(pergunta_vetorizada):

    pergunta_vetorizada = json.dumps(pergunta_vetorizada)

    USER_POSTGRESQL = os.getenv("USER_POSTGRESQL")
    PASSWORD_POSTGRESQL = os.getenv("PASSWORD_POSTGRESQL")
    ENDPOINT_POSTGRESQL = os.getenv("ENDPOINT_POSTGRESQL")

    conn, cur = connection_postgreSQL(USER_POSTGRESQL, PASSWORD_POSTGRESQL, ENDPOINT_POSTGRESQL)

    try:
        cur.execute("SELECT conteudo_vetorizada <=> %s AS distance, metadado \
                    FROM brasas_vector_db \
                    ORDER BY distance ASC \
                    LIMIT 10", (pergunta_vetorizada,))
        results = cur.fetchall()
        conn.commit()
        return results
    except Exception as e:
        print(f"Error: {e}")
        return None
        
pergunta = "quais são todas as 5 missões do brasas"
pergunta_ve=embedd_pergunta(pergunta)
print(pesquisar_conteudo_indexado(pergunta_ve))
