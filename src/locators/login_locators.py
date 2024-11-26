from selenium.webdriver.common.by import By

class LoginLocators:
    # Primeira etapa - Email
    EMAIL_INPUT = (By.ID, "username")
    CONTINUE_BUTTON = (By.ID, "login-next-button")
    
    # Verificação OTP
    OTP_STEP_DIV = (By.CLASS_NAME, "OTPStep")  # Div principal da etapa OTP
    OTP_SUBTITLE = (By.CLASS_NAME, "OTPStep__subtitle")  # Subtítulo com o email
    OTP_INPUTS = (By.CSS_SELECTOR, "input[type='tel'][maxlength='1']")  # Campos de input do código
    OTP_CONTINUE_BUTTON = (By.CSS_SELECTOR, "button.Button.Button--primary")  # Botão continuar
    OTP_RESEND_BUTTON = (By.CSS_SELECTOR, "button.Button.Button--secondary")  # Botão reenviar código
