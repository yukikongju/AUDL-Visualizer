#!/usr/bin/env/python

import pandas as pd


class Wrangler(object):

    """Docstring for Wrangler. """

    def __init__(self, download_dir: str):
        """TODO: to be defined. """
        self.download_dir = download_dir

    def download_season_player_stats(self, year: int) -> None:
        """ Download season player stats by concatenating all team player stats """
        # get all teams in a given season
        team_stats_path = self.download_dir + \
            'Team_Stats/' + 'TeamStats_' + str(year) + '.csv'
        teams_df = pd.read_csv(team_stats_path)
        teams = list(teams_df["Team"])

        # get players dataframe for each team in specified season
        dfs = []
        for index, team in enumerate(teams):
            team_name_ = team.replace(" ", "")
            df_path = self.download_dir + 'Team_Season_Player_Stats/' +\
                team_name_ + '_' + str(year) + '.csv'
            try:  # if players df exists
                df_temp = pd.read_csv(df_path)
                df_temp['Team'] = team  # add players team column
                dfs.append(df_temp)
                print(f"Concatenated {team}")
            except FileNotFoundError:
                print(f"{team}.csv does not exist. Skip ... ")

        # concat players list
        players_df = pd.concat(dfs)

        # move 'Team' column to second column
        column_to_move = players_df.pop('Team')
        players_df.insert(1, 'Team', column_to_move)

        # save players dataframe to csv file
        download_path = self.download_dir + 'Season_Player_Stats/' + \
            'SeasonPlayerStats_' + str(year) + '.csv'
        players_df.to_csv(download_path, sep=',', index=False)


def main():
    wrangler = Wrangler(download_dir="Data/")
    wrangler.download_season_player_stats(2019)


if __name__ == "__main__":
    main()
