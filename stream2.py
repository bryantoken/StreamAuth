import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import numpy as np
import os
import schedule
from inputimeout import inputimeout, TimeoutOccurred
import telepot

# Carregar a planilha Excel
caminho_arquivo = os.path.join("usuarios.xlsx")
df = pd.read_excel(caminho_arquivo)

def HUB_login(login):
    # Escolha o navegador: Firefox ou Chrome
    use_firefox = True  # Defina como True para usar o Firefox, False para usar o Chrome

    if use_firefox:
        # Opções de configuração do Firefox
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")  # Executar em modo headless
        firefox_options.add_argument("--disable-infobars")
        firefox_options.add_argument("--start-maximized")
        firefox_options.add_argument("--disable-extensions")

        # Crie o serviço para o GeckoDriver
        firefox_service = FirefoxService(GeckoDriverManager().install())
        
        # Crie o driver do Firefox
        web = webdriver.Firefox(service=firefox_service, options=firefox_options)
    else:
        # Opções de configuração do Chrome
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")  # Executar em modo headless
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")

        # Crie o serviço para o ChromeDriver
        chrome_service = ChromeService(ChromeDriverManager().install())
        
        # Crie o driver do Chrome
        web = webdriver.Chrome(service=chrome_service, options=chrome_options)

    c = "n"
    while c == 'n':
        web.get("https://hub.xpi.com.br/dashboard/#/performance")
        time.sleep(3)
        web.find_element(By.XPATH, '/html/body/auth0-login-page/arsenal-loader/div/div/div[2]/div/div/div/div/div/div/form/div[1]/div/input').send_keys(login)
        web.find_element(By.XPATH, '/html/body/auth0-login-page/arsenal-loader/div/div/div[2]/div/div/div/div/div/div/form/div[2]/div/input').send_keys(login)
        # web.find_element(By.XPATH, '/html/body/auth0-login-page/arsenal-loader/div/div/div[2]/div/div/div/div/div/div/form/div[5]/button').click()
        c = input("Posso continuar? s -> Pode. n -> Roda de novo:  ")
        
    return web

# Dicionário para armazenar estados de autenticação
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['current_user'] = None

# Função para verificar login
def check_login(login, senha):
    user_row = df[(df['login'] == login) & (df['senha'] == senha)]
    if not user_row.empty:
        st.session_state['authenticated'] = True
        st.session_state['current_user'] = user_row.iloc[0]['nome']
        return True
    else:
        return False

# Interface de Login
if not st.session_state['authenticated']:
    st.title("Login")
    login_input = st.text_input("Login")
    senha_input = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if check_login(login_input, senha_input):
            st.success(f"Bem-vindo, {st.session_state['current_user']}!")
        else:
            st.error("Login ou senha incorretos.")
else:
    # Interface após login
    st.title(f"Bem-vindo, {st.session_state['current_user']}!")
    
    def funcao_especifica(usuario):
        HUB_login(usuario)
       # st.write(f"Executando função específica para {usuario}!")

    if st.button("Executar Função"):
        funcao_especifica(st.session_state['current_user'])

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['current_user'] = None
        st.experimental_rerun()
