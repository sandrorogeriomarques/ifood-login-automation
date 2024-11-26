from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def main():
    try:
        # Configuração do Chrome
        print("Configurando o Chrome...")
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        
        # Instalação do ChromeDriver com configurações específicas
        print("Instalando/Verificando ChromeDriver...")
        chrome_driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver instalado em: {chrome_driver_path}")
        
        # Configuração do serviço
        service = Service(executable_path=chrome_driver_path)
        
        # Inicializa o driver
        print("Iniciando o Chrome...")
        driver = webdriver.Chrome(service=service, options=options)
        
        # Abre a página
        print("Abrindo a página do iFood...")
        driver.get('https://gestordepedidos.ifood.com.br/#/login')
        
        # Mantém o navegador aberto até pressionar Enter
        input("Pressione Enter para fechar o navegador...")
    
    except Exception as e:
        print(f"Erro: {str(e)}")
        print(f"Tipo do erro: {type(e)}")
        input("Pressione Enter para sair...")
    
    finally:
        # Fecha o navegador se estiver aberto
        if 'driver' in locals():
            print("Fechando o navegador...")
            driver.quit()

if __name__ == "__main__":
    main()
