import requests
from bs4 import BeautifulSoup


def get_stats(player_name):
    """Gets the stats for player"""
    page = _get_page(player_name)
    page_content = _get_page_content(page)
    stats = _format_stats(page_content, player_name)
    return stats


def get_schedule():
    raw = _get_raw_schedule()
    return _format_schedule(raw)


def _get_page(player_name):
    """Returns the corresponding Fox Sports stats page"""
    formatted_name = _format_name(player_name)
    url = "https://www.foxsports.com/nba/" + formatted_name + "-player-stats"
    page = requests.get(url)
    return page


def _get_page_content(page):
    """Returns array of stats from raw HTML"""
    soup = BeautifulSoup(page.content, "html.parser")
    for script in soup(['script', 'head']):
        script.extract()
    soup = soup.find('div', class_='wisbb_expandableTable wisbb_teamFixed wisbb_statsTable')
    soup = soup.find_all('tr', 'wisbb_fvStand')
    raw_text = soup[len(soup) - 2].get_text()
    raw_text = raw_text.splitlines()
    del raw_text[0]
    del raw_text[2]
    return raw_text


def _format_name(player_name):
    """Formats player name into name-name format"""
    player_name = _catch_name_exceptions(player_name)
    formatted_str = ""
    for i in range(len(player_name)):
        if player_name[i] == " ":
            formatted_str += "-"
        elif player_name[i] == ".":
            pass
        else:
            formatted_str += player_name[i]
    return formatted_str


def _catch_name_exceptions(name):
    """Catching some truly stupid naming exceptions"""
    if name == "Troy Brown Jr.":
        return "Troy Brown"
    elif name == "Danuel House Jr.":
        return "Danuel House"
    elif name == "Marcus Morris Sr.":
        return "Marcus Morris"
    else:
        return name


def _format_stats(raw_stats, player_name):
    """formats raw stats into a dict"""
    obj = {
        "name": player_name,
        "year": raw_stats[0],
        "team": raw_stats[1].strip(),
        "GP": raw_stats[2],
        "GS": raw_stats[3],
        "G/W": None,
        "MPG": raw_stats[4],
        "FGA/G": raw_stats[5],
        "FGM/G": raw_stats[6],
        "FG%": raw_stats[7],
        "3FGA/G": raw_stats[8],
        "3FGM/G": raw_stats[9],
        "3FG%": raw_stats[10],
        "FTA/G": raw_stats[11],
        "FTM/G": raw_stats[12],
        "FT%": raw_stats[13],
        "ORPG": raw_stats[14],
        "DRPG": raw_stats[15],
        "RPG": raw_stats[16],
        "APG": raw_stats[17],
        "SPG": raw_stats[18],
        "BPG": raw_stats[19],
        "TPG": raw_stats[20],
        "PPG": raw_stats[21],
    }
    return obj


def _get_raw_schedule():
    """Gets raw html data and returns raw weekly schedule list"""
    url = "https://hashtagbasketball.com/advanced-nba-schedule-grid"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    for script in soup(['script', 'head', 'input', 'th']):
        script.extract()
    soup = soup.find('table')
    table = []
    for row in soup.findAll('tr'):
        table.append(row.findAll('td'))
    return table


def _format_schedule(raw_lst):
    """Receives raw list data, returns a dict of games per team this week"""
    # bkn, gsw, lac, lal, nop, nyk, okc, phx, sas

    lookup = {
        "Brooklyn Nets": "BKN",
        "Golden State Warriors": "GSW",
        "Los Angeles Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Oklahoma City Thunder": "OKC",
        "Phoenix Suns": "PHX",
        "San Antonio Spurs": "SAS"
    }

    return_dict = {}
    lst = raw_lst[2:len(raw_lst)]
    for team in lst:
        team_name = team[0].string
        n_games = team[1].string
        if team_name != "Team":
            if team_name in lookup:
                return_dict[lookup[team_name]] = n_games
            else:
                temp = team_name[0:3].upper()
                return_dict[temp] = n_games

    return return_dict
