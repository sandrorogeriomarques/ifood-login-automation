import pytest
from config.config import BASE_URL

def test_open_login_page(driver):
    """
    Teste básico para verificar se a página de login abre corretamente
    """
    # Abre a página de login
    driver.get(BASE_URL)
    
    # Aguarda um momento para verificar se a página carregou
    assert "ifood" in driver.current_url.lower(), "URL não contém 'ifood'"
    
    # Verifica o título da página
    assert driver.title != "", "A página não carregou corretamente"
