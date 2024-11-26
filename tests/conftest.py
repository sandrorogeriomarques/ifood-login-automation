import pytest
from src.utils.driver_factory import get_driver

@pytest.fixture(scope="function")
def driver():
    """
    Fixture que fornece uma instância do WebDriver para cada teste.
    """
    driver = get_driver()
    yield driver
    driver.quit()
