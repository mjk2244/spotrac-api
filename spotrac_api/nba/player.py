from contract import Contract
from constants import TEAMS, BASE_URL
import requests
from requests.exceptions import HTTPError
from transaction import Transaction
from bs4 import BeautifulSoup
from exceptions import InvalidTeamException, InvalidPlayerException, InvalidSeasonException

class Player:

    def __init__(self, name: str, team = 'Brooklyn Nets'):

        """
        An object containing a player's biographical, contract, and historical transaction data.

        Args:
            team (str): Optional, The team the player is on. Can be the team's full name (e.g. 'New Orleans Pelicans')
            or the team's abbreviation (e.g. 'NOP'). If a retired player, the team the player was last on.
            name (str): The full name of the player.

        Returns:
            A Player object containing biographical, contract, and historical transaction data
            from a player's Spotrac page.

        """

        self._url = self.build_url(team, name)
        self._raw_data = self.fetch_html(self._url)
        self._current = self.parse_current(self._raw_data)
        self._name = self.parse_name(name, self._raw_data)
        self._position = self.parse_position(self._raw_data)
        self._age = self.parse_age(self._raw_data)
        self._team = self.parse_team(self._raw_data)
        self._experience = self.parse_experience(self._raw_data)
        self._drafted = self.parse_drafted(self._raw_data)
        self._college = self.parse_college(self._raw_data)
        self._agent = self.parse_agent(self._raw_data)
        self._career_earnings = self.parse_career_earnings(self._raw_data)
        if self._current:
            self._current_contract = Contract(self._raw_data)
            self._future_career_earnings = self.parse_future_career_earnings(self._raw_data)
        else:
            self._current_contract = None
            self._future_career_earnings = self._career_earnings
        self._transactions = self.parse_transactions(self._raw_data)

    def build_url(self, team: str, name: str) -> str:
        """
        Builds the url from which we will retrieve player data.
        """
        if team.lower() not in TEAMS.keys():
            raise InvalidTeamException()
        else:
            name_split = name.split()
            name_slug = name_split[0]
            for i in range(1, len(name_split)):
                name_slug += '-' + name_split[i]

            return f'{BASE_URL}{TEAMS[team.lower()]["slug"]}/{name_slug}/'
    
    def fetch_html(self, url: str) -> BeautifulSoup:
        """
        Returns a BeautifulSoup object with all the raw data from a player's page.
        """
        # do error handling for invalid responses

        response = requests.get(url)
        if response.status_code == 200: return BeautifulSoup(response.text, 'html.parser')
        else: raise HTTPError()
    
    def parse_current(self, raw_data: BeautifulSoup) -> bool:
        """
        Returns a boolean that indicates whether the player is a current player or not.
        """
        headers = raw_data.find_all('h2')
        for header in headers:
            if header.text == 'Current Contract': return True
        return False
    
    def parse_name(self, name, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's name.
        """
        if raw_data.find('h1').text.lower()[:-1] != name.lower():
            raise InvalidPlayerException(player = name)

        return raw_data.find('h1').text[:-1]

    def parse_position(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's position.
        """
        return raw_data.find('span', {'class': 'player-item position'}).text
    
    def parse_age(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's age in years and days. E.g. 23-90d
        """
        for x in raw_data.find_all('span', {'class': 'player-item'}):
            if 'Age:' in x.text:
                return x.text.replace('Age: ', '').replace(' ', '')

    def parse_team(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's team, or latest team if no longer in the league.
        """
        return raw_data.find('meta', {'name': 'keywords'})['content'].split(', ')[1]

    def parse_experience(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's years of experience.
        """
        for x in raw_data.find_all('span', {'class': 'player-item'}):
            if 'Exp: ' in x.text:
                if x.text.replace('Exp: ', '')[0] == ' ': return '0 Years'
                return x.text.replace('Exp: ', '')

    def parse_drafted(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's draft information.
        """
        for x in raw_data.find_all('span', {'class': 'player-item'}):
            if 'Drafted: ' in x.text:
                return x.text.replace('Drafted: ', '')
        return None

    def parse_college(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's college.
        """
        for x in raw_data.find_all('span', {'class': 'player-item'}):
            if 'College: ' in x.text:
                if x.text.replace('College: ', '') == '':
                    return None
                return x.text.replace('College: ', '')
        return None

    def parse_agent(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's agent(s).
        """
        for x in raw_data.find_all('span', {'class': 'player-item'}):
            if 'Agent(s): ' in x.text:
                if x.text.replace('Agent(s): ', '') == '': return None
                return x.text.replace('Agent(s): ', '')
        return None

    def parse_transactions(self, raw_data: BeautifulSoup) -> list[Transaction]:
        """
        Parses BeautifulSoup object and returns a list of Transaction objects
        associated with the player.
        """
        transactions_list = []
        for transaction in raw_data.find('li', {'id': 'transactions'}).find_all('div', {'class': 'transitem'}):
            date = transaction.find('span', {'class': 'transdate'}).text.split(' ')
            month = date[0]
            day = date[1]
            year = date[2]
            notes = transaction.find('span', {'class': 'transdesc'}).text
            transactions_list.append(Transaction(month = month, day = day, year = year, notes = notes))
        return transactions_list
    
    def parse_career_earnings(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns player's career earnings thus far.
        """
        return raw_data.find('span', {'class': 'earningsvalue'}).text

    def parse_future_career_earnings(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns what a player's career earnings will be
        at the end of their contract.
        """
        if len(raw_data.find_all('span', {'class': 'earningsvalue'})) > 1:
            return raw_data.find_all('span', {'class': 'earningsvalue'})[1].text
        return self._career_earnings
    
    @property
    def current(self) -> bool:
        """
        Returns whether the player is a current player or not.
        """
        return self._current

    @property
    def name(self) -> str:
        """
        Returns the player's name.
        """
        return self._name
    
    @property
    def position(self) -> str:
        """
        Returns the player's position.
        """
        return self._position

    @property
    def age(self) -> str:
        """
        Returns the player's age as a ``string``, in the format [years]-[days]. E.g. 23-90d
        """
        return self._age

    @property
    def age_int(self) -> int:
        """
        Returns the player's age as an ``int``. E.g. 23
        """
        if self.age is not None: return int(self._age[0:2])
        return None

    @property
    def team(self) -> str:
        """
        Returns the team the player is on or was last on (if not a current player).
        """
        return self._team

    @property
    def years_experience(self) -> str:
        """
        Returns the player's years of experience as a ``string``. E.g. '4 Years'
        """
        return self._experience
    
    @property
    def years_experience_int(self) -> int:
        """
        Returns the player's years of experience as an ``int``. E.g. 4
        """
        return int(self._experience.split(' ')[0])
    
    @property
    def college(self) -> int:
        """
        Returns the player's college, if any.
        """
        return self._college
    
    @property
    def drafted(self) -> str:
        """
        Returns the player's draft information.
        """
        return self._drafted

    @property
    def career_earnings(self) -> str:
        """
        Returns the player's career earnings as a ``string``.
        """
        return self._career_earnings
    
    @property
    def career_earnings_int(self) -> int:
        """
        Returns the player's career earnings as an ``int``.
        """
        return self.dollars_to_int(self._career_earnings)

    @property
    def future_career_earnings(self) -> str:
        """
        Returns what a player's career earnings will be at the end of their
        current contract as a ``string``.
        """
        return self._future_career_earnings
    
    @property
    def future_career_earnings_int(self) -> int:
        """
        Returns what a player's career earnings will be at the end of their
        current contract as an ``int``.
        """
        return self.dollars_to_int(self._future_career_earnings)

    @property
    def transactions(self):
        """
        Returns a list of Transaction objects associated with the player
        """
        return self._transactions
    
    @property   
    def agent(self):
        """
        Returns the player's agent(s), if any.
        """
        return self._agent

    def avg_salary(self, string = True):
        """
        Returns the player's average salary on their current contract.

        Args:
            string (bool): Determines if salary will be returned as a ``string``
            (e.g. '$5,000,000') or an ``int`` (e.g. 5000000). Default is True.
        
        Returns:
            Player's average salary on their current contract either as a ``string``
            or an ``int``.
        """
        if string: return self._current_contract.avg_salary
        else: return self._current_contract.avg_salary_int

    def base_salary(self, season: str, string = True):
        """
        Returns the player's base salary in a given season.

        Args:
            season (str): The season for which the base salary will be returned. E.g. '2022-23'
            string (bool): Determines if salary will be returned as a ``string``
            (e.g. '$5,000,000') or an ``int`` (e.g. 5000000). Default is True.
        
        Returns:
            Player's base salary in a given season either as a ``string`` or an ``int``.

        Raises:
            InvalidSeasonException: Season was not formatted properly

        """
        self.validate_season(season)

        # first check current contract
        for contract_year in self._current_contract.contract_years:
            if season == contract_year._season:
                if string: return contract_year.base_salary
                else: return contract_year.base_salary_int

        # then check past contract years
        for row in self._raw_data.find('table', {'class': 'earningstable'}).find_all('tr'):
            if len(row.find_all('td')) > 0:
                data = row.find_all('td')
                if season in data[0].text:
                    if string: return data[3].text
                    else: return self.dollars_to_int(data[3].text)
        
        # error handling if season not found
    
    def validate_season(self, season: str):
        """
        Ensures that season strings are formatted properly.
        """
        if '-' not in season: raise InvalidSeasonException(season)
        season_split = season.split('-')
        if len(season_split[0]) != 4 or len(season_split[1]) != 2: raise InvalidSeasonException(season)
        if (int(season_split[0][2:4]) + 1) % 100 != int(season_split[1]):
            raise InvalidSeasonException(season)


    def get_transactions(self, years: list[int] = None) -> list[Transaction]:
        """
        Returns a list of Transaction objects associated with the player.

        Args:
            seasons (list[str]): A list of years (as ``int``s) to limit the query to.
        
        Returns:
            A list of Transaction objects associated with the player in the
            specified year range. Returns all historical transactions if 
            year range is not specified.
        """
        if years == None: return self.transactions
        transactions = []
        for transaction in self.transactions:
            if transaction.year_int in years: transactions.append(transaction)
        return transactions



    def dollars_to_int(self, amount: str) -> int:
        """
        Converts a dollar amount (``string``) to an int
        """
        return int(amount.replace('$', '').replace(',', ''))
    

    def __str__(self) -> str:
        """
        String representation of a Player object.
        """
        if self._current:
            for contract_year in self._current_contract.contract_years:
                if contract_year.current_year:
                    season = contract_year.season
                    current_salary = contract_year.base_salary
            return f"""{self.name} ({self.position})
Current team: {self.team}
{season} salary: {current_salary}
            """
        else:
            return f"""{self.name} ({self.position})
Last played for: {self.team}
Career earnings: {self.career_earnings}"""


def main():
    player = Player(team = 'nop', name = 'Zion Williamson')
    print(player._name)
    print(player._position)
    print(player._age)
    print(player._experience)
    print(player._drafted)
    print(player._college)
    print(player._agent)
    print(player._current_contract.avg_salary)
    for transaction in player._transactions:
        #print(transaction.full_date)
        #print(transaction.notes)
        print(transaction)
    print(player.age)
    print(player.age_int)
    print(player.team)
    print(player.drafted)
    print(player.career_earnings)
    print(player.career_earnings_int)
    print(player.future_career_earnings)
    print(player.future_career_earnings_int)
    print(player.avg_salary(True))
    print(player.avg_salary(False))
    print(player.base_salary('2020-21', True))
    print(player.base_salary('2020-21', False))


    bum = Player('lebron james', 'lal')
    print(bum.base_salary('2022-23'))

    x = Player('Duop Reath')
    print(x.agent)
    print(x.college)

    y = Player('Ben Wallace', 'det')
    print(y.years_experience)
    print(y.college)
    print(y.agent)
    print(y.age)
    print(y.transactions)

if __name__ == '__main__': main()