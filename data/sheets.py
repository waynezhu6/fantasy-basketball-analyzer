import csv


def generate_csv(filename, lines):
    """Writes a csv with filename.csv to root"""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in lines:
            writer.writerow(line)


def update_row(row, index):
    for i in range(len(row)):
        sheet.update_cell(index, i + 1, row[i])


def generate_overview(players):
    lines = []
    row = ["Name", "Games", "FG%", "FT%", "3PTS",
           "PTS", "REB", 'AST', "ST", "BLK", "TO"]
    lines.append(row)

    for i in range(len(players)):
        p = players[i]
        s = p.stats
        row = [p.name, s["G/W"], s["FG%"], s["FT%"], s["3FGM/G"],
               s["PPG"], s["RPG"], s["APG"], s["SPG"], s["BPG"], s["TPG"]]
        lines.append(row)

    filename = "stats/overview.csv"
    generate_csv(filename, lines)


def generate_team_overview(team):
    name = team.name
    path = f"stats/{name.replace(' ', '_')}.csv."

    row = ["name", "team", "G/W", "MPG", "FGA/G", "FGM/G", "FG%", "FTA/G",
           "FTM/G", "FT%", "3FGM/G", "PPG", "RPG", "APG", "SPG", "BPG", "TPG"]
    lines = [row]

    for player in team.roster:
        line = []
        for stat in row:
            line.append(player[stat])
        lines.append(line)

    lines.append([])
    lines.append(row)
    start = len(lines) + 1

    chars = ["c", "e", "f", "h", "i", "k", "l", "m", "n", "o", "p", "q"]

    index = 2
    for player in team.roster:
        line = []
        for i in range(len(row)):
            if chr(97 + i) == "c":
                line.append(player["G/W"])
            elif chr(97 + i) in chars:
                s = f"={chr(97 + i)}{index}*c{len(lines) + 1}"
                line.append(s)
            else:
                s = f"={chr(97 + i)}{index}"
                line.append(s)
        index += 1
        lines.append(line)

    line = []
    for i in range(17):
        if chr(97 + i) in chars:
            s = f"=SUM({chr(97 + i)}{start}:{chr(97 + i)}{len(lines)})"
            line.append(s)
        elif chr(97 + i) == 'g':
            s = f"=f{len(lines) + 1}/e{len(lines) + 1}"
            line.append(s)
        elif chr(97 + i) == 'j':
            s = f"=i{len(lines) + 1}/h{len(lines) + 1}"
            line.append(s)
        else:
            line.append("")

    lines.append(line)
    generate_csv(path, lines)
