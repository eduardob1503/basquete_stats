import requests
import csv
from datetime import datetime

# Sua chave de API (substitua com a chave obtida após o cadastro)
API_KEY = "1f830a1a768d4593ade9c8fed8734f17"

# URL da API de jogos da NBA
URL = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{date}"

# Função para pegar os jogos de hoje
def get_todays_games():
    # Obter a data de hoje no formato YYYY-MM-DD
    today = datetime.today().strftime("%Y-%m-%d")

    # Cabeçalhos com a chave de API
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    
    # Requisição para obter os jogos do dia
    response = requests.get(URL.format(date=today), headers=headers)
    
    if response.status_code != 200:
        print(f"Erro ao acessar a API. Código: {response.status_code}")
        return []
    
    games = response.json()
    
    if not games:
        print("Nenhum jogo encontrado para hoje.")
        return []

    games_today = []
    
    # Listar os jogos
    for game in games:
        # Aqui estamos acessando diretamente os nomes dos times
        home_team = game["HomeTeam"]
        away_team = game["AwayTeam"]
        game_time = game["DateTime"]
        
        games_today.append({
            "home_team": home_team,
            "away_team": away_team,
            "game_time": game_time
        })
    
    return games_today

# Função para exportar os jogos para um arquivo CSV
def export_to_csv(games):
    # Nome do arquivo CSV
    filename = "jogos_de_hoje.csv"
    
    # Abrir o arquivo CSV em modo de escrita
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["away_team", "home_team", "game_time"])
        
        # Escrever o cabeçalho
        writer.writeheader()
        
        # Escrever os dados dos jogos
        writer.writerows(games)
    
    print(f"Dados exportados para {filename}")

# Executando a função para obter os jogos de hoje
games_today = get_todays_games()

# Exportando os jogos para o CSV
if games_today:
    export_to_csv(games_today)
else:
    print("Nenhum jogo encontrado para hoje.")
