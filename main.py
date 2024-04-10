# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

global all_games


def scrape_page():
    global all_games

    # get the raw html of the webpage
    page_to_scrape = requests.get("https://sports.yahoo.com/mlb/odds/")
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")

    # get the html of the table that contains all the games
    wrapper = soup.find_all("table", {"class": "W(100%) Maw(750px)"}, recursive=True)

    all_games = list()

    # iterate over each game (1 pair of teams)
    for game_num, game in enumerate(wrapper):
        game_data = list()
        print(f"===== GAME {game_num}=====")

        game_html_soup = BeautifulSoup(str(game), "html.parser")

        # TODO: get the game date
        game_date = "2024-04-09"

        # iterate over each team in each game
        teams_wrapper_html = game_html_soup.findAll("tbody")
        teams_html_soup = BeautifulSoup(str(teams_wrapper_html), "html.parser")
        teams_html = teams_html_soup.findAll("tr")

        for team_html in teams_html:
            team_data = list()

            team_name_html = team_html.find("span", attrs={"class": "Fw(600) Pend(4px) Ell D(ib) Maw(190px) Va(m)"})
            team_name = team_name_html.text

            team_data.append(game_num)
            team_data.append(game_date)
            team_data.append(team_name)

            team_money_line_html = team_html.findAll("span", {"class": "Lh(19px)"})

            for ml in team_money_line_html:
                team_data.append(ml.text)
            print(team_data)

            game_data.append(team_data)

        all_games.append(game_data)


def debug():
    url = 'https://sports.yahoo.com/mlb/odds/'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    games_data = soup.find_all('div', class_='game')

    data_list = []
    for game in games_data:
        home_team = game.find('span', class_='team home').text.strip()
        away_team = game.find('span', class_='team away').text.strip()
        home_odds = game.find('span', class_='line home').text.strip()
        away_odds = game.find('span', class_='line away').text.strip()
        data_list.append([home_team, away_team, home_odds, away_odds])

    df = pd.DataFrame(data_list, columns=['Home Team', 'Away Team', 'Home Odds', 'Away Odds'])
    df.to_csv('mlb_odds.csv', index=False)


# output
def write_to_csv():
    with open('out.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['game_id', 'date', 'team', 'moneyline', 'runspread', 'runspread_odds', 'totalruns', 'totalruns_odds']
        writer.writerow(header)
        for i in all_games:
            writer.writerows(i)
    print(all_games)


if __name__ == '__main__':
    scrape_page()
    write_to_csv()