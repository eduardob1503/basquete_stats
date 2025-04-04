import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import unidecode  # Biblioteca para remover acentos

# Lista de jogadores a serem pesquisados
players = [
"Taj Gibson",
"Jusuf Nurkić",
"Seth Curry",
"Miles Bridges",
"Josh Okogie",
"Grant Williams",
"DaQuan Jeffries",
"LaMelo Ball",
"Josh Green",
"Tre Mann",
"Mark Williams",
"Wendell Moore",
"Moussa Diabaté",
"Jaylen Sims",
"Brandon Miller",
"Nick Smith",
"Damion Baugh",
"Tidjane Salaün",
"KJ Simpson",
"Jonas Valančiūnas",
"DeMar DeRozan",
"Doug McDermott",
"Jae Crowder",
"Zach LaVine",
"Trey Lyles",
"Domantas Sabonis",
"Markelle Fultz",
"Malik Monk",
"Mason Jones",
"Keegan Murray",
"Keon Ellis",
"Jake LaRavia",
"Devin Carter",
"Isaiah Crawford",
"Isaac Jones",
"James Johnson",
"Myles Turner",
"T.J. McConnell",
"Pascal Siakam",
"Thomas Bryant",
"Tony Bradley",
"Obi Toppin",
"Tyrese Haliburton",
"Aaron Nesmith",
"Isaiah Jackson",
"Bennedict Mathurin",
"Andrew Nembhard",
"Quenton Jackson",
"Jarace Walker",
"Ben Sheppard",
"Johnny Furphy",
"Enrique Freeman",
"RayJ Dennis",
"Jordan Clarkson",
"Lauri Markkanen",
"John Collins",
"Collin Sexton",
"Svi Mykhailiuk",
"Kenyon Martin",
"Jaden Springer",
"Micah Potter",
"Walker Kessler",
"Johnny Juzang",
"Taylor Hendricks",
"Keyonte George",
"Brice Sensabaugh",
"Oscar Tshiebwe",
"Cody Williams",
"Kyle Filipowski",
"Isaiah Collier",
"Elijah Harkless",
"Jrue Holiday",
"Al Horford",
"Kristaps Porzingis",
"Jaylen Brown",
"Jayson Tatum",
"Derrick White",
"Luke Kornet",
"Torrey Craig",
"Payton Pritchard",
"Xavier Tillman",
"Neemias Queta",
"Sam Hauser",
"JD Davison",
"Jordan Walsh",
"Drew Peterson",
"Miles Norris",
"Baylor Scheierman",
"Bradley Beal",
"Mason Plumlee",
"Kevin Durant",
"Tyus Jones",
"Devin Booker",
"Damion Lee",
"Monté Morris",
"Royce O'Neale",
"Grayson Allen",
"Bol Bol",
"Cody Martin",
"Nick Richards",
"Vasilije Micić",
"TyTy Washington",
"Collin Gillespie",
"Ryan Dunn",
"Oso Ighodaro",
"Jalen Bridges",
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
"Dennis Schröder",
"Tobias Harris",
"Tim Hardaway",
"Malik Beasley",
"Isaiah Stewart",
"Paul Reed",
"Cade Cunningham",
"Lindy Waters",
"Jaden Ivey",
"Jalen Duren",
"Ron Harper",
"Simone Fontecchio",
"Ausar Thompson",
"Bobi Klintman",
"Marcus Sasser",
"Ron Holland II",
"Daniss Jenkins",
"Tolu Smith",
"Nikola Vučević",
"Lonzo Ball",
"Zach Collins",
"Kevin Huerter",
"Jevon Carter",
"Coby White",
"Talen Horton-Tucker",
"Patrick Williams",
"Jalen Smith",
"Tre Jones",
"Josh Giddey",
"Ayo Dosunmu",
"E.J. Liddell",
"Dalen Terry",
"Julian Phillips",
"Matas Buzelis",
"Jahmir Young",
"Emanuel Miller",
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
"Jeff Green",
"Steven Adams",
"Fred VanVleet",
"Dillon Brooks",
"Aaron Holiday",
"Jock Landale",
"Jae'Sean Tate",
"Alperen Sengün",
"Jalen Green",
"Jabari Smith",
"Tari Eason",
"David Roddy",
"Nate Williams",
"Amen Thompson",
"Cam Whitmore",
"Reed Sheppard",
"N'Faly Dante",
"Jack McVeigh",
"Alex Caruso",
"Isaiah Hartenstein",
"Shai Gilgeous-Alexander",
"Kenrich Williams",
"Luguentz Dort",
"Isaiah Joe",
"Aaron Wiggins",
"Chet Holmgren",
"Ousmane Dieng",
"Jalen Williams",
"Jaylin Williams",
"Cason Wallace",
"Adam Flagler",
"Nikola Topić",
"Dillon Jones",
"Ajay Mitchell",
"Branden Carlson",
"Alex Ducas",
"Harrison Barnes",
"Chris Paul",
"Bismack Biyombo",
"De'Aaron Fox",
"Jordan McLaughlin",
"Keldon Johnson",
"Devin Vassell",
"Charles Bassey",
"Sandro Mamukelashvili",
"David Duke",
"Malaki Branham",
"Jeremy Sochan",
"Blake Wesley",
"Julian Champagnie",
"Victor Wembanyama",
"Stephon Castle",
"Harrison Ingram",
"Riley Minix",
"Tristan Thompson",
"Jarrett Allen",
"Donovan Mitchell",
"Javonte Green",
"De'Andre Hunter",
"Darius Garland",
"Chuma Okeke",
"Ty Jerome",
"Dean Wade",
"Max Strus",
"Isaac Okoro",
"Sam Merrill",
"Evan Mobley",
"Luke Travers",
"Emoni Bates",
"Craig Porter",
"Jaylon Tyson",
"Nae'Qwan Tomlin",
"Draymond Green",
"Stephen Curry",
"Jimmy Butler",
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
"Taran Armstrong",
"DeAndre Jordan",
"Aaron Gordon",
"Russell Westbrook",
"Nikola Jokić",
"Dario Šarić",
"Jamal Murray",
"Vlatko Čančar",
"Michael Porter",
"Zeke Nnaji",
"Christian Braun",
"Peyton Watson",
"Julian Strawther",
"Jalen Pickett",
"Hunter Tyson",
"DaRon Holmes",
"PJ Hall",
"Trey Alexander",
"Spencer Jones",
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
"Kelly Olynyk",
"CJ McCollum",
"Elfrid Payton",
"Dejounte Murray",
"Bruce Brown",
"Zion Williamson",
"Kylor Kelley",
"Jeremiah Robinson-Earl",
"Brandon Boston",
"Herbert Jones",
"Trey Murphy",
"Jose Alvarado",
"Karlo Matković",
"Lester Quinones",
"Jamal Cain",
"Jordan Hawkins",
"Yves Missi",
"Antonio Reeves",
"Keion Brooks",
"James Harden",
"Nicolas Batum",
"Kawhi Leonard",
"Patty Mills",
"Norman Powell",
"Ben Simmons",
"Kris Dunn",
"Ivica Zubac",
"Bogdan Bogdanović",
"Derrick Jones",
"Drew Eubanks",
"Amir Coffey",
"Patrick Baldwin",
"Kobe Brown",
"Seth Lundy",
"Jordan Miller",
"Cam Christie",
"Trentyn Flowers",
"Anthony Davis",
"Klay Thompson",
"Dwight Powell",
"Kyrie Irving",
"Spencer Dinwiddie",
"Dante Exum",
"P.J. Washington",
"Daniel Gafford",
"Caleb Martin",
"Naji Marshall",
"Kai Jones",
"Kessler Edwards",
"Brandon Williams",
"Jaden Hardy",
"Max Christie",
"Dereck Lively",
"Olivier-Maxence Prosper"
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
