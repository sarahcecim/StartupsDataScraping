from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from time import sleep
import pandas as pd

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
    wait.until(EC.presence_of_element_located(((By.CSS_SELECTOR, "body"))))
    print("Página carregada com sucesso após o login")
except Exception as e:
    print(f"Erro: {e}")

# Clicando no botão de filtros
filter_button = navegador.find_element(By.XPATH, "//*[@id='app']/div[1]/main/div/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div[2]/span/div/div/i")
filter_button.click()
print("Botão 'Filter' clicado")
sleep(2)

# Selecionando o mercado (Market)
market_button = navegador.find_element(By.XPATH, "//*[@id='app']/div[7]/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div[7]/span/div")
market_button.click()
print("Botão 'Market' clicado")
sleep(2)

# Selecionando o filtro 'Foodtech'
foodtech_button = navegador.find_element(By.XPATH, "//*[@id='app']/div[7]/div/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div[17]/div[1]/div/i")
foodtech_button.click()
print("Filtro 'Foodtech' selecionado")
sleep(2)

# Aplicando os filtros
apply_filters_button = navegador.find_element(By.XPATH, "//*[@id='app']/div[7]/div/div/div/div[3]/button[1]")
apply_filters_button.click()
print("Filtros aplicados")
sleep(5)

# Lista para armazenar os dados
startups_data = []

# Loop principal para raspar os dados de cada startup
while True:
    # Encontra as startups visíveis na página
    rows = navegador.find_elements(By.XPATH, "//div[@class='startup border-bottom d-flex relative']")  # Ajuste o XPath conforme necessário

    for i, row in enumerate(rows):
        try:
            # Clica na startup para abrir os detalhes
            row.click()
            sleep(3)

            # Extração dos dados de cada startup
            logo = logo = navegador.find_element(By.XPATH, "//img[@class='image border-radius']").get_attribute("src")
            stage = "Stage"  # Substitua com o código correto
            totalraised = navegador.find_element(By.XPATH, "//*[@id='profile-page']/div/div[2]/div[1]/div[1]/div[3]/div[2]/div/div").text
            company = navegador.find_element(By.XPATH, "//*[@id='profile-page']/div/div[1]/div[2]/div[2]/div[1]/div[1]").text
            vc = "VC Name"  # Substitua com o código correto
            sector = "Sector"  # Substitua com o código correto
            description = "Description"  # Substitua com o código correto
            subsector = "Sub-sector"  # Substitua com o código correto
            country = "Country"  # Substitua com o código correto
            notes = "Notes"  # Substitua com o código correto
            

            # Armazenar os dados na lista
            startups_data.append({
                "Logo": logo,
                "Stage": stage,
                "Total Raised": totalraised,
                "Company": company,
                "VC": vc,
                "Sector": sector,
                "Description": description,
                "Sub-sector": subsector,
                "Country": country,
                "Notes": notes
            })
            print(f"Startup {company} processada.")

            # Voltar à página principal
            navegador.back()
            sleep(3)
        except Exception as e:
            print(f"Erro ao processar startup na linha {i + 1}: {e}")
            navegador.back()
            sleep(3)

    # Verificar se há mais páginas
    try:
        next_button = navegador.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        next_button.click()
        sleep(5)
    except:
        print("Fim da lista de startups.")
        break

# Salvar os dados em um CSV
df = pd.DataFrame(startups_data)
df.to_csv("startups_data.csv", index=False)
print("Dados salvos em startups_data.csv")

# Finalizar o navegador
navegador.quit()