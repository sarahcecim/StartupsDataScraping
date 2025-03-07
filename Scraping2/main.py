from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
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
inputUser.send_keys("user@google.com")
print("Email inserido")
sleep(3)

inputPass = navegador.find_element(By.XPATH, "//label[text()='PASSWORD']//following-sibling::input")
inputPass.send_keys("userpassword")
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
try:
    market_button = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div[3]/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div[7]/span"))
    )
    market_button.click()
    print("Botão 'Market' clicado com sucesso!")
except TimeoutException:
    print("Não foi possível encontrar o botão 'Market'. A página pode não ter carregado corretamente.")
sleep(5)

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
sleep(7)

# Função para extrair os dados de cada startup
def extract_startup_details(startup):
    try:
        # Clique na startup para acessar os detalhes
        startup.click()
        sleep(7)

        # Extrair os dados
        startup_data = {
            "Logo": navegador.find_element(By.XPATH, "//img[@class='image border-radius']").get_attribute("src"),
            "Stage": navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[2]/div/div[7]/div[2]/div[1]/div[2]").text,
            "Company": navegador.find_element(By.XPATH, "//*[@id='profile-page']/div/div[1]/div[2]/div[2]/div[1]/div[1]").text,
            "Total Raised": navegador.find_element(By.XPATH, "//*[@id='profile-page']/div/div[2]/div[1]/div[1]/div[3]/div[2]/div/div").text,
            "VC": navegador.find_element(By.XPATH, "//*[@id='19836']/div/div/div[3]/span/span/a").get_attribute("href"),
            "Sector": navegador.find_element(By.XPATH, "//*[@id='profile-page']/div/div[1]/div[2]/div[2]/div[2]").text,
            "Description": navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[1]/div[2]").text,
            "Sub-sector": navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[1]/div[3]/div[2]/div[2]/div[1]").text,
            "Country": navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[2]/div/div[6]/div[2]/div").text,
            "Website": navegador.find_element(By.XPATH, "//*[@id='SUMMARY']/div[3]/div[2]/div/div[14]/div[2]/a").get_attribute("href"),
        }
        print(f"Startup '{startup_data['Company']}' extraída com sucesso!")
        return startup_data
    except Exception as e:
        print(f"Erro ao processar startup: {e}")
        return None
    finally:
        # Volte para a lista principal
        navegador.back()
        sleep(7)

# Função para rolar e extrair todas as startups
def scroll_and_extract_details(driver, output_file):
    startups_data = []
    startups_seen = set()  # Evitar duplicados

    # Obtém as startups visíveis na página
    startups = driver.find_elements(By.CSS_SELECTOR, "#app > div.v-application--wrap > main > div > div > div.transition.d-flex.flex-column.shrank-content > div > div.px-3.mb-12 > div:nth-child(2) > div:nth-child(1) > div.disable-text-selection.relative > div.relative > div:nth-child(3) > div.startup.border-bottom.d-flex.relative")  # Seletor genérico para cada startup

    for startup in startups:
        try:
            # Identificar nome ou título único da startup para evitar clicar novamente
            startup_name_element = WebDriverWait(startup, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.disable-text-selection:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")))
            startup_name = startup_name_element.text

            # Verifica se o nome da startup já foi visto
            if startup_name not in startups_seen:
                startups_seen.add(startup_name)  # Marca o nome como visto

                # Clicar na startup
                startup.click()
                sleep(7)  # Aguardar a página carregar, considere substituir por WebDriverWait

                # Extrair os dados da startup
                startup_data = extract_startup_details(startup)

                # Verifica se os dados foram extraídos com sucesso
                if startup_data:
                    startups_data.append(startup_data)

                # Voltar para a lista de startups para continuar o loop
                navegador.back()
                sleep(5)

        except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException) as e:
            print(f"Erro ao clicar ou processar a startup: {e}")
            continue  # Continue para a próxima startup caso ocorra um erro

    # Escrever os dados extraídos em um arquivo CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=startups_data[0].keys())
        writer.writeheader()
        writer.writerows(startups_data)

    print(f"Dados extraídos e salvos em {output_file}")

# Função principal para iniciar o processo
def main():
    output_file = "startups_data.csv"
    
    # Aguardar que a página carregue e garantir que todas as startups estão visíveis
    WebDriverWait(navegador, 30).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#app > div.v-application--wrap > main > div > div > div.transition.d-flex.flex-column.shrank-content > div > div.px-3.mb-12 > div:nth-child(2) > div:nth-child(1) > div.disable-text-selection.relative > div.relative > div:nth-child(4)")  # Ajustado para o seletor correto de cada startup
        )
    )
    print("Startups carregadas na página.")
    
    # Chamar a função para rolar e extrair os detalhes das startups
    scroll_and_extract_details(navegador, output_file)
    print("Processo concluído!")

# Chamar a função principal
if __name__ == "__main__":
    main()
    navegador.quit()
