class ContractYear:

    def __init__(self, base_salary: str, likely_incentives: str, unlikely_incentives: str,
    current_year: bool, season: str, age: int, option: str, trade_bonus: str, cap_hit: str,
    pct_of_cap: str, yearly_cash: str, guaranteed_money: str):
        self._base_salary = base_salary
        self._likely_incentives = likely_incentives
        self._unlikely_incentives = unlikely_incentives
        self._current_year = current_year
        self._season = season
        if age is not None: self._age = int(age)
        else: age = None
        self._option = option
        self._trade_bonus = trade_bonus
        self._cap_hit = cap_hit
        self._pct_of_cap = pct_of_cap
        self._yearly_cash = yearly_cash
        self._guaranteed_money = guaranteed_money
    
    @property
    def base_salary(self) -> str:
        """
        Returns a player's base salary as a ``string``. E.g. '$5,000,000'
        """
        return self._base_salary

    @property
    def base_salary_int(self) -> int:
        """
        Returns a player's base salary as an ``int``. E.g. 5000000
        """
        return self.dollars_to_int(self._base_salary)

    @property
    def likely_incentives(self) -> str:
        """
        Returns a player's likely incentives as a ``string``. E.g. '$1,000,000'
        """
        return self._likely_incentives

    @property
    def likely_incentives_int(self) -> int:
        """
        Returns a player's likely incentives as an ``int``. E.g. 1000000
        """
        return self.dollars_to_int(self._likely_incentives)

    @property
    def unlikely_incentives(self) -> str:
        """
        Returns a player's unlikely incentives as a ``string``. E.g. '$1,000,000'
        """
        return self._unlikely_incentives

    @property
    def unlikely_incentives_int(self) -> int:
        """
        Returns a player's unlikely incentives as an ``int``. E.g. 1000000
        """
        return self.dollars_to_int(self._unlikely_incentives)

    @property
    def current_year(self) -> bool:
        """
        Returns whether the contract year represents the current year.
        """
        return self._current_year

    @property
    def season(self) -> str:
        """
        Returns the season of the contract year as a ``string``. E.g. '2023-24'
        """
        return self._season

    @property
    def season_tuple(self) -> tuple[int, int]:
        """
        Returns the season of the contract as a tuple. E.g. (2023, 2024)
        """
        seasons = self._season.split('-')
        century = seasons[0][0:2]
        if seasons[1] == '00':
            seasons[1] = str(int(century) + 1) + seasons[1]
        else: seasons[1] = century + seasons[1]
        return (int(seasons[0]), int(seasons[1]))

    @property
    def age(self) -> int:
        """
        Returns the player's age during the given contract year as an ``int``.
        """
        return self._age

    @property
    def option(self) -> str:
        """
        Returns the type of option, if any, associated with the given contract year.
        """
        return self._option

    @property
    def trade_bonus(self) -> str:
        """
        Returns a player's trade bonus as a ``string``. E.g. '$1,000,000'
        """
        return self._trade_bonus

    @property
    def trade_bonus_int(self) -> int:
        """
        Returns a player's trade bonus as an ``int``. E.g. 1000000
        """
        return self.dollars_to_int(self._trade_bonus)

    @property
    def cap_hit(self) -> str:
        """
        Returns a player's cap hit as a ``string``. E.g. '$1,000,000'
        """
        return self._cap_hit
 
    @property
    def cap_hit_int(self) -> int:
        """
        Returns a player's cap hit as an ``int``. E.g. 1000000
        """
        return self.dollars_to_int(self._cap_hit)

    @property
    def pct_of_cap(self) -> str:
        """
        Returns the percentage of the salary cap a player's salary takes as a ``string``.
        E.g. 29.50%
        """
        return self._pct_of_cap

    @property
    def pct_of_cap_decimal(self) -> float:
        """
        Returns the percentage of the salary cap a player's salary takes as a decimal.
        E.g. 0.295
        """
        return float(self._pct_of_cap.replace('%','')) / 100

    @property
    def yearly_cash(self) -> str:
        """
        Returns a player's yearly cash as a ``string``. E.g. '$20,000,000'
        """
        return self._yearly_cash
 
    @property
    def yearly_cash_int(self) -> int:
        """
        Returns a player's yearly cash as an ``int``. E.g. 20000000
        """
        return self.dollars_to_int(self._yearly_cash)

    @property
    def guaranteed_money(self) -> str:
        """
        Returns a player's guaranteed money as a ``string``. E.g. '$20,000,000'
        """
        return self._guaranteed_money

    @property
    def guaranteed_money_int(self) -> int:
        """
        Returns a player's guaranteed money as an ``int``. E.g. 20000000
        """
        return self.dollars_to_int(self._guaranteed_money)

    def dollars_to_int(self, amount: str) -> int:
        """
        Converts a dollar amount (string) to an int
        """
        return int(amount.replace('$', '').replace(',', ''))
