#pip3 install selenium
#pip3 install beautifulsoup4
#pip3 install lxml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from time import sleep

options = Options()
options.headless = False  # executar de forma visível ou oculta

# Usando o Google Chrome para iniciar o script
navegador = webdriver.Firefox(options=options)

link = "https://slinghub.io/"

navegador.get(url=link)
print("Página carregada")

# Usando a classe da Div pois não possui ID para ser usado - clicando no login
inputLogin = navegador.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[1]/main/div/div/div/div[1]/div[1]/div/div[3]/div")
inputLogin.click()
print("Clique no login realizado")

# Inserindo o email para login
inputUser = navegador.find_element(By.XPATH, "//label[text()='EMAIL']//following-sibling::input")
inputUser.send_keys("user@google.com")
print("Email inserido")
sleep(3)

# Inserindo a senha para login
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
wait = WebDriverWait(navegador, 30)  # Aguarda por até 30 segundos
try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    print("Página carregada com sucesso após o login")
except Exception as e:
    print(f"Erro: {e}")

