"""Script principal para automação do iFood Gestor de Pedidos."""
import os
import time
from dotenv import load_dotenv
from config.config import BASE_URL
from src.utils.driver_factory import DriverFactory
from src.pages.login_page import LoginPage
from src.pages.orders_page import OrdersPage

def handle_new_orders(orders):
    """Função chamada quando novos pedidos são detectados."""
    for order in orders:
        print("\n Novo Pedido Detectado!")
        print(f"Número: {order['number']}")
        print(f"Cliente: {order['customer']}")
        print(f"Entrega: {order['delivery_time']}")
        if order['is_test']:
            print(" Este é um pedido de teste!")
        print("-" * 50)

def main():
    # Carrega variáveis de ambiente
    load_dotenv()
    email = os.getenv("IFOOD_EMAIL")
    
    if not email:
        print("\nATENÇÃO: Email não encontrado no arquivo .env!")
        email = input("Digite seu email: ")

    driver = None
    try:
        # Define o diretório para o perfil do Chrome
        user_data_dir = os.path.join(os.path.expanduser("~"), "chrome-automation-profile")
        print(f"Usando perfil do Chrome em: {user_data_dir}")
        
        # Inicializa o driver
        driver = DriverFactory.create_chrome_driver(user_data_dir)
        
        # Navega para a página
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

        # Inicializa monitoramento de pedidos
        print("\nIniciando monitoramento de pedidos...")
        print("Pressione Ctrl+C para interromper")
        print("-" * 50)

        orders_page = OrdersPage(driver)
        orders_page.watch_for_new_orders(handle_new_orders)

    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário")
    except Exception as e:
        print(f"\nErro: {str(e)}")
    finally:
        if driver:
            print("\nFechando navegador...")
            driver.quit()

if __name__ == "__main__":
    main()
