from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import pandas as pd
import csv


# Configuração inicial
options = Options()
options.headless = False  # Executar de forma visível ou oculta
navegador = webdriver.Firefox(options=options)

# URL inicial
link = "https://slinghub.io/"
navegador.get(url=link)
print("Página carregada")

# Realizando login
inputLogin = navegador.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/main/div/div/div/div[1]/div[1]/div/div[3]/div")
inputLogin.click()
print("Clique no login realizado")

inputUser = navegador.find_element(By.XPATH, "//label[text()='EMAIL']//following-sibling::input")
inputUser.send_keys("henrycouto@google.com")
print("Email inserido")
sleep(3)

inputPass = navegador.find_element(By.XPATH, "//label[text()='PASSWORD']//following-sibling::input")
inputPass.send_keys("semdoritos")
print("Senha inserida")
sleep(3)

login_button_element = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.font-17:nth-child(1) > span:nth-child(1)"))
)
login_button_element.click()
print("Botão de login clicado")
sleep(10)

# Aguarda até 30 segundos para a página carregar após o login
wait = WebDriverWait(navegador, 30)
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div[1]/main/div/div/div[1]/div/div[2]/div/div[1]/div/div/div")))
    print("Página carregada com sucesso após o login")
except Exception as e:
    print(f"Erro ao carregar página após login: {e}")

# Clicando no botão de filtros
sleep(7)
filter_button = navegador.find_element(By.CSS_SELECTOR, "#app > div.v-application--wrap > main > div > div > div.transition.d-flex.flex-column.shrank-content > div > div.app-bar.top > div > div.flex-1.d-flex.align-center.pr-4 > div > div.full-width > div > div.flex-1 > div > div.pointer.ml-2.d-flex.align-center > span")
filter_button.click()
print("Botão 'Filter' clicado")
sleep(5)

# Selecionando o mercado (Market)
market_button = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div[3]/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div[7]/span")))
market_button.click()
print("Filtro 'Market' selecionado")
sleep(7)

# Selecionando o filtro 'Foodtech'
navegador.execute_script("window.scrollBy(0, 500);")
sleep(5)

foodtech_button = navegador.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div[17]/div[1]")
navegador.execute_script("arguments[0].scrollIntoView();", foodtech_button)
foodtech_button.click()
print("Elemento 'Foodtech' clicado com sucesso!")
sleep(5)

# Aplicando os filtros
apply_filters_button = navegador.find_element(By.XPATH, "//*[@id='app']/div[3]/div/div/div/div[3]/button[1]")
apply_filters_button.click()
print("Filtros aplicados")
sleep(5)

# Função para carregar todas as startups na página
def carregar_todas_startups(navegador, total_esperado):
    total_startups = len(navegador.find_elements(By.XPATH, "//div[@class='startup border-bottom d-flex relative']"))
    print(f"Startups inicialmente carregadas: {total_startups}")
    
    while total_startups < total_esperado:
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        novos_startups = len(navegador.find_elements(By.XPATH, "//div[@class='startup border-bottom d-flex relative']"))
        if novos_startups == total_startups:
            print("Nenhum novo bloco foi carregado. Scrolling finalizado.")
            break
        total_startups = novos_startups
        print(f"Startups carregadas até agora: {total_startups}")
    print(f"Carregamento completo! Total de startups carregadas: {total_startups}")

# Função para processar os dados de cada startup
def processar_startups(navegador):
    startups_data = []
    startup_rows = navegador.find_elements(By.XPATH, "//div[@class='startup border-bottom d-flex relative']")
    total_startups = len(startup_rows)
    print(f"Total de startups na página: {total_startups}")
    
    for index in range(total_startups):
        try:
            startup_rows = navegador.find_elements(By.XPATH, "//div[@class='startup border-bottom d-flex relative']")
            startup = startup_rows[index]
            navegador.execute_script("arguments[0].scrollIntoView(true);", startup)
            sleep(1)
            startup.click()
            sleep(6)

            # Extraindo os dados
            logo = navegador.find_element(By.XPATH, "//img[@class='image border-radius']").get_attribute("src")
            stage = navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[2]/div/div[7]/div[2]/div[1]/div[2]").text
            company = navegador.find_element(By.XPATH, "//*[@id='profile-page']/div/div[1]/div[2]/div[2]/div[1]/div[1]").text
            totalraised = navegador.find_element(By.XPATH, "//*[@id='profile-page']/div/div[2]/div[1]/div[1]/div[3]/div[2]/div/div").text
            vc = navegador.find_element(By.XPATH, "//*[@id='19836']/div/div/div[3]/span/span/a").get_attribute("href")
            sector = navegador.find_element(By.XPATH, "//*[@id='profile-page']/div/div[1]/div[2]/div[2]/div[2]").text
            description = navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[1]/div[2]").text
            subsector = navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[1]/div[3]/div[2]/div[2]/div[1]").text
            country = navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[2]/div/div[6]/div[2]/div").text
            website = navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[2]/div/div[14]/div[2]/a").get_attribute("href")
            
            startup_data = {
                "Logo": logo,
                "Stage": stage,
                "Company": company,
                "Total Raised": totalraised,
                "VC": vc,
                "Sector": sector,
                "Description": description,
                "Sub-sector": subsector,
                "Country": country,
                "Website": website
            }
            startups_data.append(startup_data)
            print(f"Startup '{company}' processada com sucesso!")

            navegador.back()
            sleep(3)

        except Exception as e:
            print(f"Erro ao processar startup {index + 1}: {e}")
            navegador.back()
            sleep(3)
            continue

    df = pd.DataFrame(startups_data)
    df.to_csv("startups_data.csv", index=False)
    print("Dados salvos em startups_data.csv")

# Executar as funções
carregar_todas_startups(navegador, 1334)
processar_startups(navegador)

# Finalizar o navegador
navegador.quit()