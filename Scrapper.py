#!/usr/bin/env/python

import pandas as pd
import requests
from bs4 import BeautifulSoup

AUDL_DEBUT = 2012  # league foundation
CURRENT_YEAR = 2021


class Scrapper(object):

    """Docstring for Scrapper. """

    def __init__(self, download_dir):
        """TODO: to be defined. """
        self.download_dir = download_dir

    def download_all_team_stats(self):
        """ Download stats sheet for a given team on a specific season """
        base_url = "https://theaudl.com/stats/team?year="
        num_seasons = self.get_number_of_seasons()
        for season in range(num_seasons):
            url = base_url + str(season+1)
            df = pd.read_html(url)[0]
            year = CURRENT_YEAR - season  # TO FIX: skip a year
            #  year = get_year()
            download_path = self.download_dir + \
                "team_stats_" + str(year) + '.csv'
            df.to_csv(download_path, sep=',', index=False)

    def get_year(self):
        """ TODO: Fix year """
        pass

    def get_team_season_player_stats(self, team, season_id):
        #  self.base_url = "https://theaudl.com/stats/team-season-players"
        pass

    def update_current_team_stats(self):
        pass

    def get_number_of_seasons(self):
        """ Get Number of Season since inauguration -> no season in 2020 (covid)"""
        return CURRENT_YEAR - AUDL_DEBUT


if __name__ == "__main__":
    scrapper = Scrapper(download_dir="Data/")
    scrapper.download_all_team_stats()
