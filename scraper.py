# scraper.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def login_and_scrape(driver, wait, login_url, credentials):
    """Realiza login e extrai informações dos pedidos."""
    driver.get(login_url)
    
    # Login
    login_user = wait.until(EC.presence_of_element_located((By.ID, "email")))
    login_pass = driver.find_element(By.ID, "password")
    login_user.send_keys(credentials["email"])
    login_pass.send_keys(credentials["password"])
    login_pass.send_keys(Keys.RETURN)

    # Aguardar a página principal carregar
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "order-list")))

    # Coleta de pedidos
    pedidos = driver.find_elements(By.CLASS_NAME, "order-card")
    data = []
    for pedido in pedidos:
        cliente = pedido.find_element(By.CLASS_NAME, "customer-name").text
        valor = pedido.find_element(By.CLASS_NAME, "order-value").text
        data.append({"Cliente": cliente, "Valor": valor})

    return data
