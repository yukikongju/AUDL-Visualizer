#!/usr/bin/env/python

import pandas as pd
import requests
from bs4 import BeautifulSoup

AUDL_DEBUT = 2012
CURRENT_YEAR = 2021
NUMBER_OF_TEAMS = 22
COVID_YEAR = 2020


class Scrapper(object):

    """Docstring for Scrapper. """

    def __init__(self, download_dir: str):
        """TODO: to be defined. """
        self.download_dir = download_dir

    def download_all_team_stats(self) -> None:
        """ Download team stats cheet for all seasons """
        base_url = "https://theaudl.com/stats/team?year="
        num_seasons = self.get_number_of_seasons()
        for season in range(1, num_seasons+1):
            #  url = base_url + str(season)
            self.download_team_stats(url=base_url+str(season))

    def download_team_stats(self, url: str) -> None:
        year = self.get_year_from_team_url(url)
        df = pd.read_html(url)[0]
        download_path = self.download_dir + "Team_Stats/" +\
            "TeamStats_" + str(year) + '.csv'
        #  download_path = f"{self.download_dir}Team_Stats/TeamStats_{str(year)}.csv"
        df.to_csv(download_path, sep=',', index=False)
        print(f"Succesfully downloaded Team Stats for {year}")

    def get_year_and_team_from_team_season_player_url(self, url: str) -> [int, str]:
        """ Get Year and team from url """
        # https://stackoverflow.com/questions/53459163/scraping-from-dropdown-option-value-python-beautifulsoup
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="lxml")
        items = soup.select('option[selected]')
        values = [item.text for item in items]
        return values[0], values[1]  # return year, team

    def get_year_from_team_url(self, url: str) -> int:
        """ Get Year from url """
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="lxml")
        items = soup.select('option[selected]')
        values = [item.text for item in items]
        return values[0]  # return year

    def download_all_team_season_player_stats(self) -> None:
        """ Download stats sheet for all given team in all seasons """
        for year_id in range(1, self.get_number_of_seasons()+1):
            for team_id in range(1, NUMBER_OF_TEAMS+1):
                self.download_team_season_player_stats(year_id, team_id)

    def download_team_season_player_stats(self, year_id: int, team_id: int) -> None:
        base_url = "https://theaudl.com/stats/team-season-players?year="
        url = base_url + str(year_id) + '&aw_team_id=' + str(team_id)
        year, team = self.get_year_and_team_from_team_season_player_url(url)
        try:  # if the team exists that year
            df = pd.read_html(url)[0]
            df = df.rename(columns={'Unnamed: 0': 'Player'})
            team_ = team.replace(" ", "")
            download_path = self.download_dir + \
                'Team_Season_Player_Stats/' + team_ + '_' + year + '.csv'
            df.to_csv(download_path, sep=',', index=False)
            print(
                f"Succesfully updated {year} {team} players stats")
        except ValueError:
            print(f"{team} was not part of AUDL that year")

    def get_number_of_seasons(self) -> int:
        """ Get Number of Season since inauguration -> no season in 2020 (covid)"""
        return CURRENT_YEAR - AUDL_DEBUT

    def download_all_time_player_stats(self) -> None:
        """ Download all-time player stats sheet """
        hasPlayerLeft = True
        base_url = "https://theaudl.com/stats/players-all-time?page="
        page = 1
        dfs = []  # store all dataframe from each pages
        while(hasPlayerLeft):
            try:
                url = base_url + str(page)
                page_df = pd.read_html(url)[0]
                dfs.append(page_df)
                print(f"Updating page {page} ...")
                page = page + 1
            except ValueError:
                print("No more players to add to dataframe")
                hasPlayerLeft = False

        # concatenate all page dataframe into single one
        df = pd.concat(dfs)

        # remove duplicate rows
        df.drop_duplicates()

        # save dataframe to csv
        download_path = self.download_dir + 'AllTimePlayerStats.csv'
        df.to_csv(download_path, sep=',', index=False)

    def download_season_schedule(self) -> None:
        """ Get season match schedule: game_id, date, home, away, score """
        NUM_OF_WEEKS = 12  # number of weeks in season
        base_url = "https://theaudl.com/league/schedule/week-"

        # fetch all matches in season by iterating through all weeks
        games = []
        for week in range(1, NUM_OF_WEEKS+1):
            url = base_url + str(week)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            # fetch page
            hrefs = soup.findAll('span', {"class": "audl-schedule-gc-link"})
            names = soup.findAll('td', {"class": "audl-schedule-team-name"})
            locations = soup.findAll('td', {"class": "audl-schedule-location"})

            i = 0
            for index, _ in enumerate(locations):
                href = hrefs[index].find('a')['href']
                game_id = href.replace('/league/game/', '')
                date = game_id[:10]  # truncate before team symbols
                location = locations[index].text

                # adding home/away team (fast pointer)
                away_team = names[i].text
                i = i+1
                home_team = names[i].text
                i = i+1

                # adding game
                game_url = "https://theaudl.com/stats/game/" + game_id
                game = [game_id, date, away_team, home_team,
                        location, game_url]
                games.append(game)

        # create season dataframe
        COLUMN_NAMES = ['ID', 'date', 'away', 'home', 'location', 'url']
        df = pd.DataFrame(games, columns=COLUMN_NAMES)

        # save season data frame as csv file
        download_path = self.download_dir + 'GameStats/schedule_' +\
            date[:4] + '.csv'
        df.to_csv(download_path, sep=',', index=False)

    def update_current_team_stats(self) -> None:
        """ Update current season team stats sheet """
        pass


def main():
    scrapper = Scrapper(download_dir="Data/")
    #  scrapper.download_all_team_stats()
    #  scrapper.download_all_team_season_player_stats()
    #  scrapper.download_all_time_player_stats()
    #  scrapper.download_season_schedule()


if __name__ == "__main__":
    main()
