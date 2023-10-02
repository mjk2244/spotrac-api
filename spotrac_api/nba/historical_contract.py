from bs4 import BeautifulSoup

class HistoricalContract:

    def __init__(self, raw_data: BeautifulSoup):
        self._raw_data = raw_data
        self._years = self.parse_years(self._raw_data)
        self._terms = self.parse_terms(self._raw_data)
        self._avg_salary = self.parse_aav(self._raw_data)
        self._gtd_at_sign = self.parse_gtd_at_sign(self._raw_data)
        self._signed_using = self.parse_signed_using(self._raw_data)
        self._free_agent = self.parse_free_agent(self._raw_data)