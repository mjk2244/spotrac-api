from contract_year import ContractYear
from bs4 import BeautifulSoup
import requests

class Contract:

    def __init__(self, contract_data: BeautifulSoup):
        self._raw_data = contract_data
        self._contract_years = self.parse_contract_years(contract_data)
        self._summary = self.parse_summary(contract_data)
        self._terms = self.parse_terms(contract_data)
        self._length = len(self._contract_years)
        self._avg_salary = self.parse_aav(contract_data)
        self._gtd_at_sign = self.parse_gtd_at_sign(contract_data)
        self._signed_using = self.parse_signed_using(contract_data)
        self._free_agent = self.parse_free_agent(contract_data)
        self._notes = self.parse_notes(contract_data)
        

    def parse_contract_years(self, contract_data: BeautifulSoup) -> list[ContractYear]:
        """
        Returns a list of ContractYear objects associated with the contract from a
        BeautifulSoup object.
        """
        contract_years = [] # initialize list to return
        contract_rows = contract_data.find('table', {'class': 'salaryTable current'}).find_all('tr')
        contract_rows = contract_rows[1:len(contract_rows) - 3] # exclude non-contract row entries
        for row in contract_rows:
            if row.find('td', {'class': 'current-year'}) == None: current_year = False
            else: current_year = True
            entries = row.find_all('td')
            season = entries[0].text
            age = entries[2].text
            if entries[3].text == '': option = None
            else: option = entries[3].text
            base_salary = entries[4].text
            if entries[5].text == '-': likely_incentives = '$0'
            else: likely_incentives = entries[5].text
            if entries[6].text == '-': unlikely_incentives = '$0'
            else: unlikely_incentives = entries[6].text
            if entries[7].text == '-': trade_bonus = '$0'
            else: trade_bonus = entries[7].text
            cap_hit = entries[8].text
            pct_of_cap = entries[9].text
            yearly_cash = entries[10].text
            guaranteed_money = entries[11].text

            contract_years.append(ContractYear(base_salary = base_salary, likely_incentives = likely_incentives,
            unlikely_incentives = unlikely_incentives, current_year = current_year, season = season, age = age,
            option = option, trade_bonus = trade_bonus, cap_hit = cap_hit, pct_of_cap = pct_of_cap,
            yearly_cash = yearly_cash, guaranteed_money = guaranteed_money))
        return contract_years
    
    def parse_summary(self, contract_data: BeautifulSoup) -> str:
        """
        Returns a text summary of the contract from a BeautifulSoup object.
        E.g. 'Bradley Beal signed a 5 year / $251,019,650 contract with the Washington Wizards,
        including $251,019,650 guaranteed, and an annual average salary of $50,203,930. In 2023-24,
        Beal will earn a base salary of $46,741,590, while carrying a cap hit of $46,741,590 and a
        dead cap value of $46,741,590.'
        """
        return contract_data.find('p', {'class': 'currentinfo'}).text

    def parse_terms(self, contract_data: BeautifulSoup) -> str:
        """
        Returns the basic terms of the contract from a BeautifulSoup object.
        E.g. '5 yr(s) / $251,019,650'
        """
        return contract_data.find_all('span', {'class': 'playerValue'})[0].text

    def parse_aav(self, contract_data: BeautifulSoup) -> str:
        """
        Returns the contract's average annual value from a BeautifulSoup object.
        """
        return contract_data.find_all('span', {'class': 'playerValue'})[1].text

    def parse_gtd_at_sign(self, contract_data: BeautifulSoup) -> str:
        """
        Returns the money guaranteed at signing from a BeautifulSoup object.
        """
        return contract_data.find_all('span', {'class': 'playerValue'})[2].text
    
    def parse_signed_using(self, contract_data: BeautifulSoup) -> str:
        """
        Returns what mechanisms the contract was signed with from a
        BeautifulSoup object.
        """
        return contract_data.find_all('span', {'class': 'playerValue'})[3].text

    def parse_free_agent(self, contract_data: BeautifulSoup) -> str:
        """
        Returns when the player will be a free agent from a BeautifulSoup object.
        """
        return contract_data.find_all('span', {'class': 'playerValue'})[4].text

    def parse_notes(self, contract_data: BeautifulSoup) -> list[str]:
        """
        Returns a list of notes about the contract from a BeautifulSoup object.
        """
        to_return = []
        notes = contract_data.find('div', {'class': 'contract-details'}).find_all('li')
        for note in notes:
            to_return.append(note.text)
        return to_return

    def contract_years(self) -> list[ContractYear]:
        """
        Returns a list of ContractYear objects.
        """
        return self._contract_years
    
    def summary(self) -> str:
        """
        Returns the contract summary.
        """
        return self._summary
    
    def terms(self) -> str:
        """
        Returns the terms of the contract.
        """
        return self._terms
    
    def length(self) -> int:
        """
        Returns the number of years in the contract.
        """
        return self._length
    
    def years_remaining(self) -> int:
        """
        Returns the number of years left in the contract,
        including the current year.
        """
        i = 0
        while self._contract_years[i]._current_year == False:
            i += 1
        return self._length - i

    def avg_salary(self) -> str:
        """
        Returns the average salary of a contract as a string
        """
        return self._avg_salary
    
    def avg_salary_int(self) -> str:
        """
        Returns the average salary of a contract as a string.
        """
        return self.dollars_to_int(self._avg_salary)

    def gtd_at_sign(self) -> str:
        """
        Returns the amount guaranteed at signing as a string.
        """
        return self._gtd_at_sign
    
    def gtd_at_sign_int(self) -> int:
        """
        Returns the amount guaranteed at signing as a string.
        """
        return self.dollars_to_int(self._gtd_at_sign)
    
    def signed_using(self) -> int:
        """
        Returns the mechanisms the contract was signed with.
        """
        return self._signed_using
    
    def free_agent(self) -> str:
        """
        Returns when the player will be a free agent, as well
        as what kind of free agent, as a string. E.g. '2027 / UFA'
        """
        return self._free_agent
    
    def free_agent_tuple(self) -> tuple[int, str]:
        """
        Returns when the player will be a free agent, as well
        as what kind of free agent, as a tuple. E.g. (2027, 'UFA')
        """
        fa = self._free_agent.split(' / ')
        return (int(fa[0]), fa[1])
    
    def notes(self) -> list[str]:
        """
        Returns a list of notes associated with the contract.
        """
        return self._notes

    
    def dollars_to_int(self, amount: str) -> int:
        """
        Converts a dollar amount (string) to an int
        """
        return int(amount.replace('$', '').replace(',', ''))
