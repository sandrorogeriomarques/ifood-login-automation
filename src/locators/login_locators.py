from selenium.webdriver.common.by import By

class LoginLocators:
    # Primeira etapa - Email
    EMAIL_INPUT = (By.ID, "username")
    CONTINUE_BUTTON = (By.ID, "login-next-button")
    LOGIN_FORM = (By.CLASS_NAME, "Login__form")
    
    # Verificação OTP
    OTP_STEP_DIV = (By.CLASS_NAME, "OTPStep")
    OTP_SUBTITLE = (By.CLASS_NAME, "OTPStep__subtitle")
    OTP_INPUTS = (By.CSS_SELECTOR, "input[type='tel'][maxlength='1']")
    OTP_CONTINUE_BUTTON = (By.CSS_SELECTOR, "button.Button.Button--primary")
    OTP_RESEND_BUTTON = (By.CSS_SELECTOR, "button.Button.Button--secondary")
    
    # Página Principal (quando logado)
    MAIN_CONTENT = (By.CSS_SELECTOR, "div[class*='MainContent']")  # Elemento que só aparece quando logado
    USER_MENU = (By.CSS_SELECTOR, "div[class*='UserMenu']")  # Menu do usuário quando logado
