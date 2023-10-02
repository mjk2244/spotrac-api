MONTHS = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

class Transaction:
    
    def __init__(self, month: str, day: int, year: int, notes: str):
        self._month = month
        self._day = day
        self._year = year
        self._notes = notes
    
    @property
    def month(self):
        """
        Returns the month of the transaction as a string. E.g. 'Jul'
        """
        return self._month
    
    @property
    def month_int(self):
        """
        Returns the month of the transaction as an ``int``. E.g. 7
        """
        return MONTHS[self._month]
    
    @property
    def day(self) -> str:
        """
        Returns the day of the transaction.
        """
        return self._day

    @property
    def day_int(self) -> int:
        """
        Returns the day of the transaction as an ``int``.
        """
        return int(self._day)
    
    @property
    def year(self) -> str:
        """
        Returns the year of the transaction.
        """
        return self._year

    @property
    def year_int(self) -> int:
        """
        Returns the year of the transaction as an ``int``.
        """
        return int(self._year)
    
    @property
    def notes(self) -> str:
        """
        Returns the notes of the transaction.
        """
        return self._notes
    
    @property
    def full_date(self) -> str:
        """
        Returns the full date of the transaction formatted as a string. E.g. 'Jul 06 2022'
        """
        return f'{self._month} {self._day} {self._year}'

    def __str__(self) -> str:
        """
        String representation of a Transaction object.
        """
        return f'{self.full_date}\n{self.notes}'