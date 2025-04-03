from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuração do Edge
edge_options = Options()
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--disable-blink-features=AutomationControlled")
edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Inicializar WebDriver
service = Service()
driver = webdriver.Edge(service=service, options=edge_options)

# URL direta para NBA na EstrelaBet
nba_url = "https://www.estrelabet.bet.br/pb?page=championship&championshipIds=2980"  # Altere para o link direto da NBA

driver.get(nba_url)

# Espera para garantir que a página da NBA foi carregada
time.sleep(5)

# Captura os jogos da NBA
try:
    # Aguardar até que os jogos sejam visíveis
    jogos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "EventBoxstyled__EventBoxContainerBase-sc-ksk2ut-32 EventBoxVariant2styled__EventBoxContainer-sc-a1yf3s-0 fJBYcG SiHuk"))  # Ajuste a classe para os jogos
    )

    if not jogos:
        raise Exception("Nenhum jogo encontrado na NBA.")
    print(f"Total de jogos encontrados: {len(jogos)}")

    # Iterar sobre os jogos encontrados
    for jogo in jogos:
        nome_jogo = jogo.text  # Nome do jogo (ex: "Lakers vs. Warriors")
        print(f"Jogo encontrado: {nome_jogo}")

        # Agora, capturamos as odds
        odds = jogo.find_elements(By.CLASS_NAME, "classe-da-odd")  # Ajuste a classe das odds
        for odd in odds:
            print(f"Odd encontrada: {odd.text}")

except Exception as e:
    print(f"Erro ao capturar os jogos: {e}")

# Fechar o navegador
driver.quit()
