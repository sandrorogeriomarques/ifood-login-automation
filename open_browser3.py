from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.config import BASE_URL
from src.pages.login_page import LoginPage
import os
from dotenv import load_dotenv
import time

def main():
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Obtém email do arquivo .env
    email = os.getenv('IFOOD_EMAIL')
    
    if not email:
        print("\nATENÇÃO: Email não encontrado no arquivo .env!")
        email = input("Digite seu email: ")
    
    try:
        print("Configurando o Chrome...")
        options = Options()
        options.add_argument('--start-maximized')
        
        # Criando driver do Chrome
        print("Iniciando o Chrome...")
        driver = webdriver.Chrome(options=options)
        
        # Navegando para a página
        print("Abrindo a página do iFood...")
        driver.get(BASE_URL)
        
        # Preenchendo email e clicando em continuar
        print("\nPreenchendo o formulário de login...")
        login_page = LoginPage(driver)
        login_page.submit_email(email)
        
        # Aguarda um momento para a página carregar
        print("\nAguardando carregamento da página...")
        time.sleep(3)  # Aumentado para 3 segundos
        
        # Verifica se apareceu a tela de verificação em duas etapas
        if login_page.is_otp_step_present():
            print("\n=== VERIFICAÇÃO EM DUAS ETAPAS ===")
            print("Por favor, verifique seu email para o código de verificação.")
            print("Aguardando entrada do código...")
            otp_code = input("\nDigite o código de 6 dígitos: ")
            
            # Verifica se o código tem 6 dígitos
            while not (otp_code.isdigit() and len(otp_code) == 6):
                print("\nO código deve conter exatamente 6 dígitos!")
                otp_code = input("Digite o código de 6 dígitos: ")
            
            # Submete o código
            print("\nProcessando código de verificação...")
            login_page.submit_otp(otp_code)
            print("\nCódigo de verificação submetido!")
        else:
            print("\nNenhuma verificação em duas etapas necessária.")
        
        print("\nProcesso de login concluído!")
        input("\nPressione Enter para fechar o navegador...")
        
    except Exception as e:
        print(f"\nOcorreu um erro:")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        input("\nPressione Enter para sair...")
        
    finally:
        if 'driver' in locals():
            print("\nFechando o navegador...")
            driver.quit()

if __name__ == "__main__":
    main()
