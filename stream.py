# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:53:17 2024

@author: golde
"""

import streamlit as st
import pandas as pd

###

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import pandas as pd
import datetime as dt
from os import path, remove, listdir
import schedule
from inputimeout import inputimeout, TimeoutOccurred
import telepot
import numpy as np
import os
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager




# Carregar a planilha Excel
# pasta_downloads = 'C:/Users/golde/Documents/'
# df = pd.read_excel(pasta_downloads + "usuarios.xlsx")
# diretorio_atual = os.path.dirname(__file__)
caminho_arquivo = os.path.join("usuarios.xlsx")
df = pd.read_excel(caminho_arquivo)
##########
def HUB_login(login):
    # Opções de configuração do Firefox
    firefox_options = Options()
    firefox_options.add_argument("--disable-infobars")
    firefox_options.add_argument("--start-maximized")
    firefox_options.add_argument("--disable-extensions")

    # Crie o serviço para o GeckoDriver
    firefox_service = FirefoxService(GeckoDriverManager().install())
    
    # Crie o driver do Firefox
    web = webdriver.Firefox(service=firefox_service, options=firefox_options)
    
    c = "n"
    while c == 'n':
        web.get("https://hub.xpi.com.br/dashboard/#/performance")
        time.sleep(3)
        web.find_element(By.XPATH, '/html/body/auth0-login-page/arsenal-loader/div/div/div[2]/div/div/div/div/div/div/form/div[1]/div/input').send_keys(login)
        web.find_element(By.XPATH, '/html/body/auth0-login-page/arsenal-loader/div/div/div[2]/div/div/div/div/div/div/form/div[2]/div/input').send_keys(login)
        #web.find_element(By.XPATH, '/html/body/auth0-login-page/arsenal-loader/div/div/div[2]/div/div/div/div/div/div/form/div[5]/button').click()
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
