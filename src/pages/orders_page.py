"""Page object for the orders page."""
import time
from typing import List, Dict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from ..locators.orders_locators import OrdersLocators

class OrdersPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.locators = OrdersLocators
        self.known_orders = set()  # Armazena números de pedidos já vistos
    
    def wait_for_orders_container(self):
        """Aguarda o container de pedidos estar visível."""
        return self.wait.until(
            EC.presence_of_element_located(self.locators.ORDERS_CONTAINER)
        )
    
    def get_order_details(self, order_card) -> Dict:
        """Extrai detalhes de um card de pedido."""
        try:
            order_number = order_card.find_element(*self.locators.ORDER_NUMBER).text
            customer_name = order_card.find_element(*self.locators.CUSTOMER_NAME).text
            delivery_time = order_card.find_element(*self.locators.DELIVERY_TIME).text
            
            # Verifica se é um pedido teste
            try:
                tooltip = order_card.find_element(*self.locators.ORDER_TOOLTIP)
                is_test = "Pedido teste" in tooltip.text
            except NoSuchElementException:
                is_test = False
            
            return {
                "number": order_number,
                "customer": customer_name,
                "delivery_time": delivery_time,
                "is_test": is_test
            }
        except NoSuchElementException as e:
            print(f"Erro ao extrair detalhes do pedido: {str(e)}")
            return None
    
    def get_new_orders(self) -> List[Dict]:
        """Verifica e retorna novos pedidos."""
        try:
            # Aguarda container de pedidos
            self.wait_for_orders_container()
            
            # Encontra todos os cards de pedidos
            order_cards = self.driver.find_elements(*self.locators.ORDER_CARD)
            
            new_orders = []
            for card in order_cards:
                details = self.get_order_details(card)
                if details and details["number"] not in self.known_orders:
                    new_orders.append(details)
                    self.known_orders.add(details["number"])
            
            return new_orders
            
        except TimeoutException:
            print("Timeout aguardando container de pedidos")
            return []
        except Exception as e:
            print(f"Erro ao verificar novos pedidos: {str(e)}")
            return []
    
    def watch_for_new_orders(self, callback, interval=5):
        """Monitora continuamente por novos pedidos.
        
        Args:
            callback: Função a ser chamada quando houver novos pedidos
            interval: Intervalo em segundos entre verificações
        """
        try:
            while True:
                new_orders = self.get_new_orders()
                if new_orders:
                    callback(new_orders)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoramento de pedidos interrompido")
        except Exception as e:
            print(f"Erro no monitoramento de pedidos: {str(e)}")
