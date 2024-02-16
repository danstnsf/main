from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import csv

def limpar_pasta(dir):
    try:
        files=os.listdir(dir)
        for item in files:
            caminho=os.path.join(dir,item)
            os.remove(caminho)
    except OSError as e:
        print(f"Error: {e}")

def esperar_download(directory, timeout=60):
    start_time = time.time()

    while time.time() - start_time < timeout:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        if files:
            return os.path.join(directory, files[0])

        time.sleep(1)

    raise TimeoutError("Timeout waiting for file creation")

def ls_sort_csv(dir):
    arquivos = os.listdir(dir)
    arquivos_csv = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]
    arquivos_csv.sort(key=lambda x: int(x[-7:-4].strip("()")) if x[-6].isdigit() else 0)
    return arquivos_csv

def renomear(dir,antigo,novo):
    dir_ant=os.path.join(dir,antigo)
    dir_novo=os.path.join(dir,novo)
    os.rename(dir_ant,dir_novo)
    

class Extrair_dengue:
    def __init__(self):
        self.url_formulario = 'https://info.dengue.mat.br/services/api'
        self.dict_cidade={}
        self.pasta_dados=os.path.join(os.getcwd(),"data")

    def inic_driver(self):
        options=webdriver.ChromeOptions()
        prefs={"download.default_directory":self.pasta_dados}
        options.add_experimental_option("detach",True)
        options.add_experimental_option("prefs",prefs)
        options.add_argument('--start-minimized')
        servico= Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=options,service=servico)
        self.driver.minimize_window()
    def definir_locais(self):
        with open(os.path.join(os.getcwd(),"bases\\cods_ride.csv"),'r',newline='') as csvfile:
            next(csvfile)
            csv_reader=csv.reader(csvfile,delimiter=';')
            for linha in csv_reader:
                cod=linha[0]
                mun=linha[1]
                self.dict_cidade[cod]=mun

    def puxarinfo(self):
        self.definir_locais()

        limpar_pasta(self.pasta_dados)

        dt_inic=input("Insira a data inicial (DDMMAAAA): ")
        dt_final=input("Insira a data final (DDMMAAAA): ")
        print("Download iniciado, aguarde...\n")
        self.driver.get(self.url_formulario)

        campo_idlocal = self.driver.find_element(By.ID,'geocode-search')            
        campo_inic = self.driver.find_element(By.ID,'epidate_start')
        campo_fim = self.driver.find_element(By.ID,'epidate_end')
        download_but=self.driver.find_element(By.XPATH,'//*[@id="wrap"]/div[2]/form/div/div/div[9]/input')
        
        campo_inic.send_keys(dt_inic)
        campo_fim.send_keys(dt_final)
        
        lista_cods=list(self.dict_cidade.keys())
        for cod in lista_cods:
            campo_idlocal.clear()
            campo_idlocal.send_keys(cod)
            download_but.send_keys(Keys.RETURN)
            esperar_download(self.pasta_dados)
        self.driver.quit()
        print("Download concluido\n")
    def criar_base(self):
        csv_files = [file for file in os.listdir(self.pasta_dados) if file.endswith('.csv')]
        pasta_bases=os.path.join(os.getcwd(),"bases\\infodengue_ride.csv")
        headers_written = False
        with open(pasta_bases, 'w', newline='') as output_file:

            csv_writer = csv.writer(output_file)

            for csv_file in csv_files:
                file_path = os.path.join(self.pasta_dados, csv_file)

                with open(file_path, 'r') as input_file:
                
                    csv_reader = csv.reader(input_file)

                    if headers_written:
                        next(csv_reader)

                    csv_writer.writerows(csv_reader)

                    headers_written = True
class Extrair_inmet:
    def __init__(self):
        self.url_formulario = 'https://tempo.inmet.gov.br/TabelaEstacoes/A001'
        self.dict_cidade={}
        self.pasta_dados=os.path.join(os.getcwd(),"data_inmet")

    def inic_driver(self):
        options=webdriver.ChromeOptions()
        prefs={"download.default_directory":self.pasta_dados}
        options.add_experimental_option("detach",True)
        options.add_experimental_option("prefs",prefs)
        options.add_argument('--start-minimized')
        servico= Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=options,service=servico)
        #self.driver.minimize_window()
        self.driver.get(self.url_formulario)
        
    def definir_locais(self):
            with open(os.path.join(os.getcwd(),"bases\\cods_ride.csv"),'r',newline='') as csvfile:
                next(csvfile)
                csv_reader=csv.reader(csvfile,delimiter=';')
                for linha in csv_reader:
                    cod_cid=linha[0]
                    cod_est=linha[4]
                    self.dict_cidade[cod_cid]=cod_est
    
    def get_csv(self,dti,dtf,cod_est):
        side_but=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div[1]/div[1]/i')))
        side_but.click()
        estacao=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div[2]/div[1]/div[2]/div[3]/input')))
        data_inic=self.driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input')
        data_fim=self.driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input')
        gerar_but=self.driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[1]/div[2]/button')
        estacao.send_keys(cod_est)
        data_inic.send_keys(dti)
        data_fim.send_keys(dtf)
        gerar_but.click()
        download_but=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div[2]/div[2]/div/div/div/span/a')))
        download_but.click()
    
    def atualizar_base(self,dti,dtf):
        self.definir_locais()
        limpar_pasta(self.pasta_dados)
        lista_estacs=set(self.dict_cidade.values())
        ordem=[]
        for cod in lista_estacs:
            self.get_csv(dti,dtf,cod)
            ordem.append(cod)
        time.sleep(5)
        self.driver.quit()
        ordem=[cod+'.csv' for cod in ordem]
        files_name=ls_sort_csv(self.pasta_dados)
        for i in range(len(ordem)):
            renomear(self.pasta_dados,files_name[i],ordem[i])

Teste=Extrair_inmet()
Teste.inic_driver()
Teste.atualizar_base('01092023','16022024')
#Teste.criar_base()

