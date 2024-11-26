from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main():
    try:
        # Configuração do Chrome
        print("Configurando o Chrome...")
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        
        # Usando o Chrome padrão
        print("Iniciando o Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        
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
        if 'driver' in locals():
            print("Fechando o navegador...")
            driver.quit()

if __name__ == "__main__":
    main()
