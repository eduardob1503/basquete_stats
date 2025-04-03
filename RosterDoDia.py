import requests
import datetime
import csv

# Sua chave de API
API_KEY = "1f830a1a768d4593ade9c8fed8734f17"

# URL para pegar a lista de jogadores de um time
URL_PLAYERS = "https://api.sportsdata.io/v3/nba/scores/json/Players/{team_id}"

# URL para pegar os jogos do dia
URL_GAMES = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{date}"

def get_todays_games():
    today = datetime.datetime.today().strftime("%Y-%m-%d")  # Formato YYYY-MM-DD
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    
    response = requests.get(URL_GAMES.format(date=today), headers=headers)
    
    if response.status_code != 200:
        print(f"Erro ao acessar a API dos jogos. Código: {response.status_code}")
        return []
    
    games = response.json()
    
    games_today = []
    for game in games:
        home_team = game["HomeTeam"]
        away_team = game["AwayTeam"]
        games_today.append({"home_team": home_team, "away_team": away_team})
    
    return games_today

def get_players_for_team(team_id):
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    
    response = requests.get(URL_PLAYERS.format(team_id=team_id), headers=headers)
    
    if response.status_code != 200:
        print(f"Erro ao acessar os jogadores do time {team_id}. Código: {response.status_code}")
        return []
    
    players = response.json()
    
    # Filtrando apenas os nomes dos jogadores
    player_names = []
    for player in players:
        first_name = player.get("FirstName", "")
        last_name = player.get("LastName", "")
        full_name = f"{first_name} {last_name}"
        player_names.append(full_name)
    
    return player_names

# Pegar os jogos de hoje
games_today = get_todays_games()

# Criar dois arquivos CSV para salvar os dados
with open('players_with_team.csv', mode='w', newline='', encoding='utf-8') as file_with_team, \
     open('players_without_team.csv', mode='w', newline='', encoding='utf-8') as file_without_team:
    
    writer_with_team = csv.writer(file_with_team)
    writer_without_team = csv.writer(file_without_team)
    
    writer_with_team.writerow(['Team', 'Player Name'])  # Cabeçalho com time
    writer_without_team.writerow(['Player Name'])  # Cabeçalho sem time
    
    # Para cada jogo, pegar os jogadores dos times envolvidos
    for game in games_today:
        home_team = game["home_team"]
        away_team = game["away_team"]
        
        # Jogadores do time da casa
        home_team_players = get_players_for_team(home_team)
        for player in home_team_players:
            writer_with_team.writerow([home_team, player])
            writer_without_team.writerow([f"*{player},&"])  # Formatação com um asterisco, vírgula e "&"
        
        away_team_players = get_players_for_team(away_team)
        for player in away_team_players:
            writer_with_team.writerow([away_team, player])
            writer_without_team.writerow([f"*{player},&"])
