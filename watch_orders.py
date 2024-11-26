"""Script para monitorar novos pedidos do iFood."""
import os
import time
from dotenv import load_dotenv
from src.utils.driver_factory import DriverFactory
from src.pages.login_page import LoginPage
from src.pages.orders_page import OrdersPage

def handle_new_orders(orders):
    """Função chamada quando novos pedidos são detectados."""
    for order in orders:
        print("\n🔔 Novo Pedido Detectado!")
        print(f"Número: {order['number']}")
        print(f"Cliente: {order['customer']}")
        print(f"Entrega: {order['delivery_time']}")
        if order['is_test']:
            print("⚠️ Este é um pedido de teste!")
        print("-" * 50)

def main():
    # Carrega variáveis de ambiente
    load_dotenv()
    email = os.getenv("IFOOD_EMAIL")
    
    try:
        # Inicializa o driver
        driver_factory = DriverFactory()
        driver = driver_factory.get_driver()
        
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
        print("\nFechando navegador...")
        driver.quit()

if __name__ == "__main__":
    main()
