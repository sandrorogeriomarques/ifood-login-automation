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

        # Faz login se necessário
        login_page = LoginPage(driver)
        if not login_page.is_logged_in():
            print("Fazendo login...")
            login_page.login(email)
            print("Login realizado com sucesso!")
        else:
            print("Já está logado!")

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
