import requests
from bs4 import BeautifulSoup

# URL da página de odds da Bet365 para um jogo específico
url = "https://www.oddsportal.com/basketball/usa/nba/"

# Fazer a requisição
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Exemplo: Encontrar odds de um time
odds = soup.find_all('div', class_='odd')

# Exibir as odds
for odd in odds:
    print(odd.text)
