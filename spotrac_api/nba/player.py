from contract import Contract
from constants import TEAMS, BASE_URL
import requests
from transaction import Transaction
from bs4 import BeautifulSoup

class Player:

    def __init__(self, team: str, player_id: str):
        self._url = self.build_url(team, player_id)
        self._raw_data = self.fetch_html(self._url)
        self._current_player = self.parse_current_player(self._raw_data)
        self._name = self.parse_name(self._raw_data)
        self._position = self.parse_position(self._raw_data)
        self._age = self.parse_age(self._raw_data)
        self._experience = self.parse_experience(self._raw_data)
        self._drafted = self.parse_drafted(self._raw_data)
        self._college = self.parse_college(self._raw_data)
        self._agents = self.parse_agents(self._raw_data)
        if self._current_player: self._current_contract = Contract(self._raw_data)
        else: self._current_contract = None
        self._transactions = self.parse_transactions(self._raw_data)

    def build_url(self, team: str, player_id: str) -> str:
        """
        Builds the url from which we will retrieve player data.
        """
        return f'{BASE_URL}{TEAMS[team].lower()}/{player_id}/'
    
    def fetch_html(self, url: str) -> BeautifulSoup:
        """
        Returns a BeautifulSoup object with all the raw data from a player's page.
        """
        # do error handling for invalid responses

        response = requests.get(url)
        if response.status_code == 200: return BeautifulSoup(response.text, 'html.parser')
    
    def parse_current_player(self, raw_data: BeautifulSoup) -> bool:
        """
        Returns a boolean that indicates whether the player is a current player or not.
        """
        headers = raw_data.find_all('h2')
        for header in headers:
            if header.text == 'Current Contract': return True
        return False
    
    def parse_name(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's name.
        """
        return raw_data.find('h1').text

    def parse_position(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's position.
        """
        return raw_data.find('span', {'class': 'player-item position'}).text
    
    def parse_age(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's age in years and days. E.g. 23-90d
        """
        return raw_data.find('span', {'class': 'player-infoitem'}).text.replace(' ', '')

    def parse_experience(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's years of experience.
        """
        return raw_data.find_all('span', {'class': 'player-item'})[2].text.replace('Exp: ', '')

    def parse_drafted(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's draft information.
        """
        return raw_data.find_all('span', {'class': 'player-item'})[3].text.replace('Drafted: ', '')

    def parse_college(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's college.
        """
        return raw_data.find_all('span', {'class': 'player-item'})[4].text.replace('College: ', '')

    def parse_agents(self, raw_data: BeautifulSoup) -> str:
        """
        Parses BeautifulSoup object and returns the player's agent(s).
        """
        return raw_data.find_all('span', {'class': 'player-item'})[5].text.replace('Agent(s): ', '')

    def parse_transactions(self, raw_data: BeautifulSoup) -> list[Transaction]:
        """
        Parses BeautifulSoup object and returns a list of Transaction objects
        associated with the player.
        """
        transactions_list = []
        for transaction in raw_data.find('li', {'id': 'transactions'}).find_all('div', {'class': 'transitem'}):
            date = transaction.find('span', {'class': 'transdate'}).text.split(' ')
            month = date[0]
            day = date[0]
            year = date[0]
            notes = transaction.find('span', {'class': 'transdesc'}).text
            transactions_list.append(Transaction(month = month, day = day, year = year, notes = notes))
        return transactions_list
            



def main():
    player = Player(team = 'nop', player_id = 'zion-williamson-31558')
    print(player._current_player)
    print(player._name)
    print(player._position)
    print(player._age)
    print(player._experience)
    print(player._drafted)
    print(player._college)
    print(player._agents)
    print(player._current_contract.avg_salary)
    for transaction in player._transactions:
        print(transaction.notes)

if __name__ == '__main__': main()