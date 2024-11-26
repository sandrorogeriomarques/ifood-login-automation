from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.locators.login_locators import LoginLocators
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.short_wait = WebDriverWait(driver, 3)  # Espera curta para verificações rápidas
    
    def is_logged_in(self):
        """Verifica se o usuário está logado"""
        try:
            # Tenta encontrar elementos que só aparecem quando logado
            self.short_wait.until(
                EC.presence_of_element_located(LoginLocators.MAIN_CONTENT)
            )
            return True
        except TimeoutException:
            return False
    
    def needs_login(self):
        """Verifica se é necessário fazer login"""
        try:
            # Tenta encontrar o formulário de login
            self.short_wait.until(
                EC.presence_of_element_located(LoginLocators.LOGIN_FORM)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_login_state(self):
        """Aguarda e verifica o estado do login"""
        print("Verificando estado do login...")
        
        # Primeiro verifica se já está logado
        if self.is_logged_in():
            print("Usuário já está logado!")
            return "logged_in"
        
        # Se não está logado, verifica se precisa fazer login
        if self.needs_login():
            print("Formulário de login detectado.")
            return "needs_login"
        
        # Se não está logado e não tem form de login, pode ser OTP
        if self.is_otp_step_present():
            print("Verificação em duas etapas detectada.")
            return "needs_otp"
        
        print("Estado de login indefinido.")
        return "unknown"
    
    def enter_email(self, email):
        """Insere o email no campo de login"""
        print(f"Preenchendo o email: {email}")
        email_field = self.wait.until(
            EC.presence_of_element_located(LoginLocators.EMAIL_INPUT)
        )
        email_field.clear()
        email_field.send_keys(email)
    
    def click_continue(self):
        """Clica no botão continuar"""
        print("Clicando no botão Continuar...")
        continue_button = self.wait.until(
            EC.element_to_be_clickable(LoginLocators.CONTINUE_BUTTON)
        )
        continue_button.click()
    
    def submit_email(self, email):
        """Preenche o email e clica em continuar"""
        self.enter_email(email)
        self.click_continue()
    
    def is_otp_step_present(self):
        """Verifica se está na etapa de verificação OTP"""
        try:
            self.short_wait.until(
                EC.presence_of_element_located(LoginLocators.OTP_STEP_DIV)
            )
            return True
        except TimeoutException:
            return False
    
    def enter_otp_code(self, code):
        """Preenche o código OTP nos campos"""
        print(f"Preenchendo código de verificação...")
        
        # Encontra todos os campos de input
        otp_inputs = self.wait.until(
            EC.presence_of_all_elements_located(LoginLocators.OTP_INPUTS)
        )
        
        print(f"Encontrados {len(otp_inputs)} campos para preenchimento")
        
        # Verifica se temos 6 campos e 6 dígitos
        if len(otp_inputs) != 6 or len(code) != 6:
            raise ValueError(f"O código deve ter 6 dígitos (encontrados {len(otp_inputs)} campos)")
        
        # Preenche cada dígito
        for i, (input_field, digit) in enumerate(zip(otp_inputs, code)):
            print(f"Preenchendo dígito {i+1}: {digit}")
            input_field.send_keys(digit)
            time.sleep(0.1)  # Pequena pausa para simular digitação humana
    
    def click_otp_continue(self):
        """Clica no botão continuar após inserir o código"""
        print("Clicando em continuar após código de verificação...")
        continue_button = self.wait.until(
            EC.element_to_be_clickable(LoginLocators.OTP_CONTINUE_BUTTON)
        )
        continue_button.click()
    
    def submit_otp(self, code):
        """Preenche o código OTP e continua"""
        self.enter_otp_code(code)
        self.click_otp_continue()
