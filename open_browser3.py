"""Script principal para automação do iFood Gestor de Pedidos."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config.config import BASE_URL
from src.pages.login_page import LoginPage
from src.utils.driver_factory import DriverFactory
import os
from dotenv import load_dotenv
import time
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

def extrair_detalhes_pedido(driver, pedido):
    try:
        # Aguarda um momento para garantir que a página está estável
        time.sleep(1)
        
        # Encontra a área clicável do pedido (evitando o botão de despachar)
        area_clicavel = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test-id="preparing-order-order-card"]'))
        )
        
        # Rola até o elemento para garantir que está visível
        driver.execute_script("arguments[0].scrollIntoView(true);", area_clicavel)
        time.sleep(1)  # Pequena pausa após a rolagem
        
        # Tenta clicar usando JavaScript (mais confiável que o clique normal)
        driver.execute_script("arguments[0].click();", area_clicavel)
        
        # Aguarda os detalhes aparecerem
        time.sleep(2)  # Aguarda a animação de abertura
        
        try:
            detalhes = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tour-element="ORDER_DETAILS_COSTUMER_DATA"]'))
            )
            
            # Dicionário para armazenar os detalhes
            info_pedido = {}
            
            # Tenta extrair cada informação individualmente com tratamento de erro
            try:
                localizador = detalhes.find_element(By.CSS_SELECTOR, '[data-test-id="localizer-id"]')
                info_pedido['localizador'] = localizador.text if localizador else "Não encontrado"
            except:
                info_pedido['localizador'] = "Não disponível"
            
            try:
                horario = detalhes.find_element(By.CSS_SELECTOR, '.sc-bXMzgG.figlin')
                info_pedido['horario_pedido'] = horario.text if horario else "Não encontrado"
            except:
                info_pedido['horario_pedido'] = "Não disponível"
            
            try:
                telefone_element = detalhes.find_element(By.CSS_SELECTOR, '.ifdl-icon-telephone').find_element(By.XPATH, '..')
                info_pedido['telefone'] = telefone_element.text if telefone_element else "Não encontrado"
            except:
                info_pedido['telefone'] = "Não disponível"
            
            try:
                endereco_element = detalhes.find_element(By.CSS_SELECTOR, '.sc-dUOoGL.fMPdzP')
                info_pedido['endereco'] = endereco_element.text if endereco_element else "Não encontrado"
            except:
                info_pedido['endereco'] = "Não disponível"
            
            try:
                status_element = detalhes.find_element(By.CSS_SELECTOR, '.mVuiT')
                info_pedido['status'] = status_element.text if status_element else "Não encontrado"
            except:
                info_pedido['status'] = "Não disponível"
            
            try:
                horario_status = detalhes.find_element(By.CSS_SELECTOR, '.bfkxsF')
                info_pedido['horario_status'] = horario_status.text if horario_status else "Não encontrado"
            except:
                info_pedido['horario_status'] = "Não disponível"
            
            return info_pedido
            
        except Exception as e:
            print(f"Erro ao extrair informações detalhadas: {str(e)}")
            return None
            
    except Exception as e:
        print(f"Erro ao clicar no pedido: {str(e)}")
        return None

def monitorar_novos_pedidos(driver):
    print("\nMonitorando novos pedidos...")
    pedidos_processados = set()
    
    while True:
        try:
            # Procura por novos pedidos na seção "Em preparo"
            pedidos = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-test-id="preparing-order-order-card"]'))
            )
            
            for pedido in pedidos:
                try:
                    # Pega o número do pedido
                    numero_pedido = pedido.find_element(By.CSS_SELECTOR, '[type="order"]').text
                    
                    # Se já processamos este pedido, pula
                    if numero_pedido in pedidos_processados:
                        continue
                    
                    # Pega as informações básicas do pedido
                    try:
                        nome_cliente = pedido.find_element(By.CSS_SELECTOR, '[type="name"]').text
                    except:
                        nome_cliente = "Nome não disponível"
                        
                    try:
                        tempo_entrega = pedido.find_element(By.CSS_SELECTOR, '[type="action"]').text
                    except:
                        tempo_entrega = "Tempo não disponível"
                    
                    print("\n=== NOVO PEDIDO DETECTADO ===")
                    print(f"Número do Pedido: {numero_pedido}")
                    print(f"Nome do Cliente: {nome_cliente}")
                    print(f"Tempo de Entrega: {tempo_entrega}")
                    
                    # Extrai detalhes adicionais do pedido
                    detalhes = extrair_detalhes_pedido(driver, pedido)
                    if detalhes:
                        print("\n=== DETALHES DO PEDIDO ===")
                        print(f"Localizador: {detalhes['localizador']}")
                        print(f"Horário do Pedido: {detalhes['horario_pedido']}")
                        print(f"Telefone: {detalhes['telefone']}")
                        print(f"Endereço: {detalhes['endereco']}")
                        print(f"Status: {detalhes['status']}")
                        print(f"Horário do Status: {detalhes['horario_status']}")
                    
                    print("============================")
                    
                    # Marca o pedido como processado
                    pedidos_processados.add(numero_pedido)
                    
                except Exception as e:
                    print(f"Erro ao processar pedido: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Erro ao buscar pedidos: {str(e)}")
        
        # Aguarda antes de verificar novamente
        time.sleep(5)

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

        monitorar_novos_pedidos(driver)

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
