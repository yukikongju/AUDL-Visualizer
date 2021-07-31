#!/usr/bin/env/python

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

AUDL_DEBUT = 2012
CURRENT_YEAR = 2021
NUMBER_OF_TEAMS = 22
COVID_YEAR = 2020


class Scrapper(object):

    """Docstring for Scrapper. """

    def __init__(self, download_dir):
        """TODO: to be defined. """
        self.download_dir = download_dir

    def download_all_team_stats(self):
        """ Download team stats cheet for all seasons """
        base_url = "https://theaudl.com/stats/team?year="
        num_seasons = self.get_number_of_seasons()
        for season in range(1, num_seasons+1):
            url = base_url + str(season)
            df = pd.read_html(url)[0]
            year = self.get_year_from_team_url(url)
            download_path = self.download_dir + "Team_Stats/" +\
                "team_stats_" + str(year) + '.csv'
            df.to_csv(download_path, sep=',', index=False)

    def get_year_and_team_from_team_season_player_url(self, url):
        """ Get Year and team from url """
        # https://stackoverflow.com/questions/53459163/scraping-from-dropdown-option-value-python-beautifulsoup
        response = requests.get(url)
        soup = bs(response.content, features="lxml")
        items = soup.select('option[selected]')
        values = [item.text for item in items]
        return values[0], values[1]  # return year, team

    def get_year_from_team_url(self, url):
        """ Get Year from url """
        response = requests.get(url)
        soup = bs(response.content, features="lxml")
        items = soup.select('option[selected]')
        values = [item.text for item in items]
        return values[0]  # return year

    def download_all_team_season_player_stats(self):
        """ Download stats sheet for all given team in all seasons """
        base_url = "https://theaudl.com/stats/team-season-players?year="
        url = "https://theaudl.com/stats/team-season-players?year=4&aw_team_id=14"
        year = CURRENT_YEAR - season  # TO FIX: skip a year
        df = pd.read_html(url)[0]
        print(df)

    def update_current_team_stats(self):
        pass

    def get_number_of_seasons(self):
        """ Get Number of Season since inauguration -> no season in 2020 (covid)"""
        return CURRENT_YEAR - AUDL_DEBUT


if __name__ == "__main__":
    scrapper = Scrapper(download_dir="Data/")
    scrapper.download_all_team_stats()
    #  scrapper.download_all_team_season_player_stats()