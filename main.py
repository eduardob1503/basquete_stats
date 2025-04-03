import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import unidecode  # Biblioteca para remover acentos

# Lista de jogadores a serem pesquisados
players = [
"Khris Middleton",
"Marcus Smart",
"Richaun Holmes",
"Malcolm Brogdon",
"Jordan Poole",
"Saddiq Bey",
"Anthony Gill",
"Corey Kispert",
"JT Thor",
"Justin Champagnie",
"Bilal Coulibaly",
"Colby Jones",
"Tristan Vukcevic",
"Jaylen Martin",
"Kyshawn George",
"Bub Carrington",
"Alexandre Sarr",
"AJ Johnson",
"Cory Joseph",
"Kentavious Caldwell-Pope",
"Gary Harris",
"Jonathan Isaac",
"Wendell Carter",
"Moritz Wagner",
"Goga Bitadze",
"Cole Anthony",
"Trevelin Queen",
"Franz Wagner",
"Jalen Suggs",
"Ethan Thompson",
"Mac McClung",
"Paolo Banchero",
"Caleb Houstan",
"Anthony Black",
"Jett Howard",
"Tristan da Silva",
"D'Angelo Russell",
"De'Anthony Melton",
"Cameron Johnson",
"Nicolas Claxton",
"Ziaire Williams",
"Cam Thomas",
"Keon Johnson",
"Day'Ron Sharpe",
"Trendon Watford",
"Tyrese Martin",
"Tyson Etienne",
"Noah Clowney",
"Dariq Whitehead",
"Maxwell Lewis",
"Jalen Wilson",
"Drew Timme",
"Tosan Evbuomwan",
"Reece Beekman",
"Mike Conley",
"Julius Randle",
"Rudy Gobert",
"Joe Ingles",
"Donte DiVincenzo",
"Nickeil Alexander-Walker",
"Naz Reid",
"Anthony Edwards",
"Jaden McDaniels",
"Luka Garza",
"Bones Hyland",
"Leonard Miller",
"Josh Minott",
"Jaylen Clark",
"Rob Dillingham",
"Terrence Shannon",
"Tristen Newton",
"Jesse Edwards",
"Kevin Love",
"Kyle Anderson",
"Andrew Wiggins",
"Alec Burks",
"Terry Rozier",
"Bam Adebayo",
"Duncan Robinson",
"Haywood Highsmith",
"Tyler Herro",
"Davion Mitchell",
"Josh Christopher",
"Dru Smith",
"Nikola Jović",
"Jaime Jaquez",
"Kel'el Ware",
"Pelle Larsson",
"Keshad Johnson",
"Isaiah Stevens",
"Luke Kennard",
"Jaren Jackson",
"Marvin Bagley III",
"Ja Morant",
"Brandon Clarke",
"John Konchar",
"Desmond Bane",
"Lamar Stevens",
"Santi Aldama",
"Jay Huff",
"Scotty Pippen",
"Vince Williams",
"GG Jackson II",
"Zach Edey",
"Jaylen Wells",
"Cam Spencer",
"Zyon Pullin",
"Yuki Kawamura",
"Kyle Lowry",
"Eric Gordon",
"Joel Embiid",
"Paul George",
"Andre Drummond",
"Kelly Oubre",
"Guerschon Yabusele",
"Lonnie Walker IV",
"Chuma Okeke",
"Tyrese Maxey",
"Jared Butler",
"Quentin Grimes",
"Jeff Dowtin",
"Phillip Wheeler",
"Jalen Hood-Schifino",
"Colin Castleton",
"Ricky Council IV",
"Marcus Bagley",
"Jared McCain",
"Justin Edwards",
"Adem Bona",
"Alex Reese",
"Giannis Antetokounmpo",
"Brook Lopez",
"Damian Lillard",
"Bobby Portis",
"Pat Connaughton",
"Taurean Prince",
"Kyle Kuzma",
"Gary Trent",
"Kevin Porter",
"Jericho Sims",
"Ryan Rollins",
"Jamaree Bouyea",
"AJ Green",
"Stanley Umude",
"Andre Jackson",
"Chris Livingston",
"Pete Nance",
"Tyler Smith",
"Garrett Temple",
"Brandon Ingram",
"Jakob Poeltl",
"Chris Boucher",
"RJ Barrett",
"Immanuel Quickley",
"Scottie Barnes",
"A.J. Lawson",
"Ochai Agbaji",
"Cole Swider",
"Jared Rhoden",
"Orlando Robinson",
"Gradey Dick",
"Ja'Kobe Walter",
"Jonathan Mogbo",
"Jamal Shead",
"Ulrich Chomche",
"Jamison Battle",
"Jerami Grant",
"Deandre Ayton",
"Anfernee Simons",
"Robert Williams",
"Duop Reath",
"Matisse Thybulle",
"Deni Avdija",
"Dalano Banton",
"Shaedon Sharpe",
"Bryce McGowens",
"Jabari Walker",
"Justin Minaya",
"Scoot Henderson",
"Rayan Rupert",
"Kris Murray",
"Sidy Cissoko",
"Toumani Camara",
"Donovan Clingan",
"LeBron James",
"Markieff Morris",
"Alex Len",
"Dorian Finney-Smith",
"Maxi Kleber",
"Luka Dončić",
"Jarred Vanderbilt",
"Shake Milton",
"Gabe Vincent",
"Jaxson Hayes",
"Rui Hachimura",
"Austin Reaves",
"Jordan Goodwin",
"Christian Koloko",
"Trey Jemison",
"Dalton Knecht",
"Bronny James",
"Draymond Green",
"Stephen Curry",
"Jimmy Butler ",
"Kevon Looney",
"Buddy Hield",
"Gary Payton",
"Kevin Knox",
"Moses Moody",
"Jonathan Kuminga",
"Braxton Key",
"Gui Santos",
"Pat Spencer",
"Trayce Jackson-Davis",
"Brandin Podziemski",
"Quinten Post",
"Jackson Rowe",
"Taran Armstrong"
]

# URL base do Basketball Reference
BASE_URL = "https://www.basketball-reference.com/players"

def format_player_name(player_name):
    player_name = unidecode.unidecode(player_name)  # Remove acentos
    name_parts = player_name.split()
    last_name = name_parts[-1].lower()
    first_name = name_parts[0].lower()
    return f"{BASE_URL}/{last_name[0]}/{last_name[:5]}{first_name[:2]}01.html"

def get_player_stats(player_name):
    player_url = format_player_name(player_name)
    response = requests.get(player_url)
    
    if response.status_code == 404:
        print(f"Erro 404: Página não encontrada para {player_name}.")
        return None
    elif response.status_code == 429:
        print(f"Erro 429: Excesso de requisições. Encerrando a coleta.")
        return "STOP"
    elif response.status_code != 200:
        print(f"Erro ao acessar a página de {player_name}. Status: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    stats_table = soup.find("table", {"id": "per_game_stats"})
    
    if stats_table:
        rows = stats_table.find_all("tr")
        player_stats = []
        
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) > 0:
                try:
                    season = cols[0].text.strip()
                    if season == "Did not play - injury" or not season:
                        continue
                    player_stats.append({
                        "Jogador": player_name,
                        "Temporada": season,
                        "Equipe": cols[1].text.strip(),
                        "Liga": cols[2].text.strip(),
                        "Posição": cols[3].text.strip(),
                        "Jogos": cols[4].text.strip(),
                        "Jogos como Titular": cols[5].text.strip(),
                        "Minutos": cols[6].text.strip(),
                        "FG": cols[7].text.strip(),
                        "FGA": cols[8].text.strip(),
                        "FG%": cols[9].text.strip(),
                        "3P": cols[10].text.strip(),
                        "3PA": cols[11].text.strip(),
                        "3P%": cols[12].text.strip(),
                        "2P": cols[13].text.strip(),
                        "2PA": cols[14].text.strip(),
                        "2P%": cols[15].text.strip(),
                        "eFG%": cols[16].text.strip(),
                        "FT": cols[17].text.strip(),
                        "FTA": cols[18].text.strip(),
                        "FT%": cols[19].text.strip(),
                        "ORB": cols[20].text.strip(),
                        "DRB": cols[21].text.strip(),
                        "TRB": cols[22].text.strip(),
                        "AST": cols[23].text.strip(),
                        "STL": cols[24].text.strip(),
                        "BLK": cols[25].text.strip(),
                        "TOV": cols[26].text.strip(),
                        "PF": cols[27].text.strip(),
                        "PTS": cols[28].text.strip(),
                        "TRP-DOU": cols[29].text.strip(),
                    })
                except IndexError:
                    continue
        return player_stats
    
    print(f"Dados não encontrados para {player_name}.")
    return None

# Coletar dados para os jogadores
data = []
for index, player in enumerate(players):
    player_stats = get_player_stats(player)
    if player_stats == "STOP":
        break
    elif player_stats:
        last_season = player_stats[-1]
        data.append(last_season)
    
    # A cada 10 jogadores, espera 30 segundos
    if (index + 1) % 10 == 0:
        print("Aguardando 30 segundos para evitar bloqueio...")
        time.sleep(30)

# Criar um DataFrame e salvar no CSV formatado
df = pd.DataFrame(data)
cols_to_round = ["FG%", "3P%", "2P%", "eFG%", "FT%"]
for col in cols_to_round:
    df[col] = pd.to_numeric(df[col], errors="coerce").round(3)

df.to_csv("estatisticas_ultima_temporada_jogadores_completo.csv", index=False, sep=";", float_format="%.2f")
print("Dados salvos com sucesso!")
