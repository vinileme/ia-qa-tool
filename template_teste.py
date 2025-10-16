# template_teste.py
# Este é um modelo de teste robusto que será preenchido pela IA.

import pytest
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- DADOS DO TESTE (Serão preenchidos pela IA) ---
URL_LOGIN = "{URL_LOGIN}"
USER_INPUT_ID = "{USER_INPUT_ID}"
PASSWORD_INPUT_ID = "{PASSWORD_INPUT_ID}"
LOGIN_BUTTON_ID = "{LOGIN_BUTTON_ID}"
SUCCESS_URL_CONTAINS = "{SUCCESS_URL_CONTAINS}"
# ---------------------------------------------------

@pytest.fixture
def driver_setup(request):
    driver = webdriver.Chrome()
    yield driver
    # Bloco de Teardown para screenshots
    if request.node.rep_call.failed:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"ERRO_{request.node.name}_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
    else:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"SUCESSO_{request.node.name}_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
    driver.quit()

def test_login_com_sucesso(driver_setup):
    driver = driver_setup
    wait = WebDriverWait(driver, 10)
    driver.get(URL_LOGIN)
    
    # Preencher utilizador
    user_input = wait.until(EC.visibility_of_element_located((By.ID, USER_INPUT_ID)))
    user_input.send_keys("standard_user")
    
    # Preencher palavra-passe
    pass_input = wait.until(EC.visibility_of_element_located((By.ID, PASSWORD_INPUT_ID)))
    pass_input.send_keys("secret_sauce")
    
    # Clicar no botão de login
    login_button = wait.until(EC.element_to_be_clickable((By.ID, LOGIN_BUTTON_ID)))
    login_button.click()
    
    # Validar o sucesso
    wait.until(EC.url_contains(SUCCESS_URL_CONTAINS))
    assert SUCCESS_URL_CONTAINS in driver.current_url
