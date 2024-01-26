from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

dt_inic=input("Insira a data inicial (DDMMAAAA): ")
dt_final=input("Insira a data final (DDMMAAAA): ")

class Extrair_dengue:
    def __init__(self):
        self.options=webdriver.ChromeOptions()
        self.options.add_experimental_option("detach",True)
        self.servico= Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=self.options,service=self.servico)
        self.url_formulario = 'https://info.dengue.mat.br/services/api'
        self.driver.get(self.url_formulario)
        self.campo_idlocal = self.driver.find_element(By.ID,'geocode-search')
        self.campo_inic = self.driver.find_element(By.ID,'epidate_start')
        self.campo_fim = self.driver.find_element(By.ID,'epidate_end')
        self.download_but=self.driver.find_element(By.XPATH,'//*[@id="wrap"]/div[2]/form/div/div/div[9]/input')
        self.dict_cidade={}

    def definir_locais(self,tabela_locais):
        with open('cods_ride.csv','r',newline='') as csvfile:
            next(csvfile)
            csv_reader=csv.reader(csvfile,delimiter=';')
            for linha in csv_reader:
                cod=linha[0]
                mun=linha[1]
                self.dict_cidade[cod]=mun


    def run(self):
        lista_cods=list(self.dict_cidade.keys())
        self.campo_inic.send_keys(dt_inic)
        self.campo_fim.send_keys(dt_final)
        for cod in lista_cods:
            self.campo_idlocal.send_keys(cod)
            self.download_but.send_keys(Keys.RETURN)

Teste=Extrair_dengue()
Teste.definir_locais('cods_ride.csv')
Teste.run()
    # Fechar o navegador
    #driver.quit()
