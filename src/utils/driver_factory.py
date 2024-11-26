from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class DriverFactory:
    @staticmethod
    def create_chrome_driver(user_data_dir=None):
        """
        Cria uma instância do Chrome WebDriver com configurações personalizadas
        
        Args:
            user_data_dir (str): Diretório para armazenar os dados do usuário do Chrome
        """
        options = Options()
        options.add_argument('--start-maximized')
        
        # Se um diretório de perfil foi especificado, usa ele
        if user_data_dir:
            # Cria o diretório se não existir
            os.makedirs(user_data_dir, exist_ok=True)
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument('--profile-directory=Default')
        
        # Outras opções úteis
        options.add_argument('--disable-popup-blocking')  # Desativa bloqueio de popups
        options.add_argument('--disable-notifications')   # Desativa notificações
        options.add_argument('--disable-infobars')       # Remove a barra de informações
        
        return webdriver.Chrome(options=options)
