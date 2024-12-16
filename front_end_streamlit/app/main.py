import logging
from openai import AzureOpenAI
from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu
import requests

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

def client_openai(messages, contexto):
    client = AzureOpenAI()
    # Add context to the messages
    messages.append({"role": "system", "content": f"Contexto do brasas movement: {contexto}"})
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return_response = chat_completion.choices[0].message.content
    return return_response

def get_contexto_brasas(fala_usuario):
    body = {"text": f"{fala_usuario}"}
    request = requests.post("http://localhost:8000/ms_embedding/search_similarity", json=body)
    contexto = request.json()
    return contexto

if __name__ == "__main__":

    st.title("Chat.IA do Brasas Movement")

    menu = option_menu(None, 
        ["Chat Brasas", "Adicionar novos dados (VISÃO ADMIN)"], 
        icons=["chat", "data"], 
        menu_icon="cast", 
        default_index=0, 
        orientation="horizontal")

    logging.debug(f"Menu selected: {menu}")

    if menu == "Chat Brasas":

        # Initialize chat history with system message
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "Você está conversando com um assistente do Brasas Movement\
                 que é capaz de responder perguntas sobre o Brasas com dados proprietarios do movimento\
                 Responda as perguntas do usuario com os dados de contexto e historico que você tem\
                 nem sempre o que vir no contexto voce precisa falar, porque as vezes sera um bom dia\
                 uma apresentacao, utilize o contexto apenas para responder perguntas especificas do brasas"
                }
            ]
            logging.debug("Initialized session state messages")

        # Display chat messages from history on app rerun, excluding system messages
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Escreva sua mensagem"):
            logging.debug(f"User input: {prompt}")
            
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": f"Falas dos usúario do brasas: \n{prompt}"})

            # Obter resposta do assistente com contexto
            contexto_brasas = get_contexto_brasas(prompt)
            logging.debug(f"Contexto brasas: {contexto_brasas}")
            llm_response = client_openai(st.session_state.messages, contexto_brasas)
            logging.debug(f"LLM response: {llm_response}")
            with st.chat_message("assistant"):
                st.markdown(llm_response)

            # Adicionar resposta do assistente ao histórico
            st.session_state.messages.append({"role": "assistant", "content": llm_response})