#!/usr/bin/env/python

import pandas as pd
from datetime import datetime
from datetime import timedelta

from Scrapper import Scrapper
from Wrangler import Wrangler

CURRENT_YEAR = 2021
CURRENT_YEAR_ID = 1

TEAM_NUMBER_ID = {
    "Atlanta Hustle": 1,
    "Austin Sol": 2,
    "Boston Glory": 3,
    "Chicago Union": 4,
    "Dallas Roughnecks": 5,
    "DC Breeze": 6,
    "Detroit Mechanix": 7,
    "Indianapolis AlleyCats": 8,
    "Los Angeles Aviators": 9,
    "Madison Radicals": 10,
    "Minnesota Wind Chill": 11,
    "Montreal Royal": 12,
    "New York Empire": 13,
    "Ottawa Outlaws": 14,
    "Philadelphia Phoenix": 15,
    "Pittsburgh Thunderbirds": 16,
    "Raleigh Flyers": 17,
    "San Diego Growlers": 18,
    "San Jose Spiders": 19,
    "Seattle Cascades": 20,
    "Tampa Bay Cannons": 21,
    "Toronto Rush": 22,
}


class Updater(object):

    """ Update CSV file with this week new data """

    def __init__(self, download_dir: str):
        """TODO: to be defined. """
        self.download_dir = download_dir
        self.scrapper = Scrapper(self.download_dir)
        self.wrangler = Wrangler(self.download_dir)

    def update_files(self) -> None:
        """ Update CSV files """
        self.download_game_stats()
        self.update_team_season_player_stats()
        self.update_team_stats()
        self.update_all_time_player_stats()
        self.update_season_player_stats()

    def update_team_season_player_stats(self) -> None:
        """ Update {team}_{current_year}.csv
            -> only update teams that have played this week
        """
        # find teams that have played this week
        teams = self.find_teams_that_played_this_week()
        # update teams sheet
        for index, team in enumerate(teams):
            team_id = TEAM_NUMBER_ID[team]
            print(f"Updating {team}_{CURRENT_YEAR}.csv sheet...")
            self.scrapper.download_team_season_player_stats(
                CURRENT_YEAR_ID, team_id=team_id)

    def find_game_date_range(self) -> [str, str]:
        """ Get date range to search for new games: YYYY-MM-DD """
        today_date = datetime.today().strftime('%Y-%m-%d')
        NUM_OF_DAYS_IN_WEEK = 7
        last_week_date = (datetime.strptime(
            today_date, '%Y-%m-%d') - timedelta(days=NUM_OF_DAYS_IN_WEEK))
        last_week_date = str(last_week_date)[:10]  # truncate time
        return last_week_date, today_date  # start_date, end_date

    def find_teams_that_played_this_week(self) -> list:
        """ Find teams that played in the last 7 days """
        # read schedule
        schedule_path = f"{self.download_dir}GameStats/schedule_{CURRENT_YEAR}.csv"
        df = pd.read_csv(schedule_path, sep=',')

        # find date where we should search for new games
        start_date, end_date = self.find_game_date_range()
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        games_df = df.loc[mask]  # all games that are within date range

        # get teams that played inside date range
        home_df = games_df['home']
        away_df = games_df['away']
        teams = list(pd.concat([home_df, away_df]))
        return teams

    def update_team_stats(self) -> None:
        """ Update TeamStats_{current_year}.csv sheet
            -> this sheet is updated everytime a game is played
        """
        url = f"https://theaudl.com/stats/team?year={CURRENT_YEAR_ID}"
        self.scrapper.download_team_stats(url)

    def update_all_time_player_stats(self) -> None:
        """ Update AllTimePlayerStats_{current_year}.csv
            -> this sheet is updated evertime a game is played
        """
        self.scrapper.download_all_time_player_stats()

    def update_season_player_stats(self) -> None:
        """ Update SeasonPlayerStats_{current_year}.csv
            -> this sheet is updated evertime a game is played
        """
        self.wrangler.download_season_player_stats()

    def download_game_stats(self) -> None:
        """ TODO: download all stats from this week games with GameScrapper """
        # find games that have played this week
        pass


def main() -> None:
    updater = Updater("Data/")
    #  updater.update_files()
    #  updater.find_teams_that_played_this_week()
    #  updater.update_team_season_player_stats()


if __name__ == "__main__":
    main()
