"""Locators for the orders page elements."""
from selenium.webdriver.common.by import By

class OrdersLocators:
    # Container principal de pedidos
    ORDERS_CONTAINER = (By.CLASS_NAME, "ReactVirtualized__Grid__innerScrollContainer")
    
    # Seção de categorias (Em preparo, etc)
    CATEGORY_SECTION = (By.CSS_SELECTOR, '[data-tour-element="CATEGORY_SECTION"]')
    CATEGORY_HEADER = (By.CLASS_NAME, "sc-gdfaqJ")
    CATEGORY_NAME = (By.CLASS_NAME, "sc-cHMHOW")
    CATEGORY_COUNT = (By.CLASS_NAME, "sc-ciQpPG")
    
    # Card de pedido
    ORDER_CARD = (By.CSS_SELECTOR, '[data-test-id="preparing-order-order-card"]')
    ORDER_NUMBER = (By.CSS_SELECTOR, 'span[type="order"]')
    CUSTOMER_NAME = (By.CSS_SELECTOR, 'span[type="name"]')
    DELIVERY_TIME = (By.CSS_SELECTOR, 'span[type="action"]')
    
    # Botão de despachar
    DISPATCH_BUTTON = (By.CSS_SELECTOR, '[data-tour-element="ORDER_DETAILS_DISPATCH_ACTION"]')
    
    # Tooltip de pedido teste
    ORDER_TOOLTIP = (By.CLASS_NAME, "TooltipContent-sc-15tsulq-3")
