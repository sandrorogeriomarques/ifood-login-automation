from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.config import BASE_URL
from src.pages.login_page import LoginPage
from src.utils.driver_factory import DriverFactory
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
        
        # Define o diretório para o perfil do Chrome
        user_data_dir = os.path.join(os.path.expanduser("~"), "chrome-automation-profile")
        print(f"Usando perfil do Chrome em: {user_data_dir}")
        
        # Criando driver do Chrome com perfil personalizado
        driver = DriverFactory.create_chrome_driver(user_data_dir)
        
        # Navegando para a página
        print("Abrindo a página do iFood...")
        driver.get(BASE_URL)
        
        # Inicializa a página de login
        login_page = LoginPage(driver)
        
        # Aguarda e verifica o estado do login
        print("\nVerificando estado da página...")
        time.sleep(2)  # Pequena pausa para carregar
        
        login_state = login_page.wait_for_login_state()
        
        if login_state == "logged_in":
            print("\nVocê já está logado! Não é necessário fazer login novamente.")
        
        elif login_state == "needs_login":
            print("\nRealizando login...")
            login_page.submit_email(email)
            
            # Aguarda e verifica se precisa de verificação em duas etapas
            time.sleep(2)
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
        
        elif login_state == "needs_otp":
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
            print("\nEstado de login indefinido. Por favor, verifique manualmente.")
        
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
