class InvalidTeamException(Exception):

    def __init__(self, message = 'Invalid team name/abbreviation. Please check your spelling.'):
        """
        Occurs when an invalid team name is passed to a Team or Player object.
        """
        self.message = message
        super().__init__(message)

class InvalidPlayerException(Exception):

    def __init__(self, player):
        """
        Occurs when an invalid player name is passed to a Player object.
        """
        self.player = player
        self.message = f'Cannot find Spotrac page for {self.player}. Please check your spelling.'
        super().__init__(self.message) 

class InvalidSeasonException(Exception):

    def __init__(self, season):
        """
        Occurs when a season is not formatted properly.
        """
        self.season = season
        self.message = f'Season "{self.season}" is not formatted properly. Proper formatting: "2022-23"'
        super().__init__(self.message)