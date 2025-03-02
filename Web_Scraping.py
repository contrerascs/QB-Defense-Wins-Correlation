from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_qb_stats(driver, year):
    """Extrae las estadísticas de QBs para un año específico."""
    web = f'https://www.pro-football-reference.com/years/{year}/kicking.htm'
    driver.get(web)

    # Esperar a que cargue la página
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Scroll para hacer visible el botón
    driver.execute_script("window.scrollTo(0, 850);")  
    time.sleep(2)

    # Click en "Share & Export"
    share_export_menu = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//li[@class="hasmore"]/span[text()="Share & Export"]'))
    )
    share_export_menu.click()

    # Click en "Get table as CSV (for Excel)"
    csv_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Get table as CSV (for Excel)")]'))
    )
    csv_button.click()

    # Obtener los datos del elemento <pre>
    pre_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "csv_kicking"))
    )
    csv_data = pre_element.text

    # Guardar en archivo TXT
    with open(f"data_txt/kickers/kickers_stats_{year}.txt", "w", encoding="utf-8") as file:
        file.write(csv_data)

    print(f"Datos de {year} guardados correctamente.")

# Configurar Selenium (iniciar el navegador una sola vez)
path = 'D:/Sam Contreras/Documents/Programacion/Python/ChromeDriver/chromedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

try:
    for year in range(1989, 2023):
        get_qb_stats(driver, year)
        time.sleep(3)  # Espera entre peticiones para evitar bloqueos del sitio

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()  # Cerrar el navegador al final
    print("Scraping finalizado.")