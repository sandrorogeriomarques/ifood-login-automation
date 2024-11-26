from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """
    Cria e retorna uma instância do WebDriver do Chrome.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Descomente para executar em modo headless
    options.add_argument('--start-maximized')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver
