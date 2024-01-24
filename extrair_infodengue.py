from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

dt_inic=input("Insira a data inicial (DDMMAAAA): ")
dt_final=input("Insira a data final (DDMMAAAA): ")

options=webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
# Caminho para o seu driver. Substitua pelo caminho correto.
servico= Service(ChromeDriverManager().install())

# Inicializa o driver do Chrome
driver = webdriver.Chrome(options=options,service=servico)

# URL do formulário
url_formulario = 'https://info.dengue.mat.br/services/api'

# Navega até o formulário
driver.get(url_formulario)

# Encontrar elementos do formulário pelo nome, ID, XPath, etc.
campo_UF = driver.find_element(By.ID,'geocode-search')
campo_inic = driver.find_element(By.ID,'epidate_start')
campo_fim = driver.find_element(By.ID,'epidate_end')

# Preencher o formulário
campo_UF.send_keys('DF')
campo_inic.send_keys(dt_inic)
campo_fim.send_keys(dt_final)

# Submeter o formulário (opcional, dependendo do seu caso)
#campo_mensagem.send_keys(Keys.RETURN)

# Fechar o navegador
#driver.quit()
