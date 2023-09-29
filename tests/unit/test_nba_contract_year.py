from spotrac_api.nba.contract_year import ContractYear
import pytest

@pytest.fixture
def contract_year():
    return ContractYear(base_salary = '$40,230,320',
    likely_incentives = '$2,000,000',
    unlikely_incentives = '$1,000,000',
    current_year = True,
    season = '2023-24',
    age = '24',
    option = 'Player',
    trade_bonus = '$3,000,000',
    cap_hit = '$40,230,320',
    pct_of_cap = '25.90%',
    yearly_cash = '$40,230,320',
    guaranteed_money = '$40,230,320'
    )

def test_base_salary(contract_year):
    assert contract_year.base_salary == '$40,230,320'

def test_base_salary_int(contract_year):
    assert contract_year.base_salary_int == 40230320

def test_likely_incentives(contract_year):
    assert contract_year.likely_incentives == '$2,000,000'

def test_likely_incentives_int(contract_year):
    assert contract_year.likely_incentives_int == 2000000

def test_unlikely_incentives(contract_year):
    assert contract_year.unlikely_incentives == '$1,000,000'

def test_unlikely_incentives_int(contract_year):
    assert contract_year.unlikely_incentives_int == 1000000

def test_current_year(contract_year):
    assert contract_year.current_year == True

def test_season(contract_year):
    assert contract_year.season == '2023-24'

def test_season_tuple(contract_year):
    assert contract_year.season_tuple == (2023, 2024)
    turn_of_century = ContractYear(base_salary = '$40,230,320',
    likely_incentives = '$2,000,000',
    unlikely_incentives = '$1,000,000',
    current_year = False,
    season = '1999-00',
    age = '24',
    option = 'Player',
    trade_bonus = '$3,000,000',
    cap_hit = '$40,230,320',
    pct_of_cap = '25.90%',
    yearly_cash = '$40,230,320',
    guaranteed_money = '$40,230,320'
    )
    assert turn_of_century.season_tuple == (1999, 2000)

def test_age(contract_year):
    assert contract_year.age == 24

def test_option(contract_year):
    assert contract_year.option == 'Player'

def test_trade_bonus(contract_year):
    assert contract_year.trade_bonus == '$3,000,000'

def test_trade_bonus_int(contract_year):
    assert contract_year.trade_bonus_int == 3000000

def test_cap_hit(contract_year):
    assert contract_year.cap_hit == '$40,230,320'

def test_cap_hit_int(contract_year):
    assert contract_year.cap_hit_int == 40230320

def test_pct_of_cap(contract_year):
    assert contract_year.pct_of_cap == '25.90%'

def test_pct_of_cap_decimal(contract_year):
    assert contract_year.pct_of_cap_decimal == 0.2590

def test_yearly_cash(contract_year):
    assert contract_year.yearly_cash == '$40,230,320'

def test_yearly_cash_int(contract_year):
    assert contract_year.yearly_cash_int == 40230320

def test_guaranteed_money(contract_year):
    assert contract_year.guaranteed_money == '$40,230,320'

def test_guaranteed_money_int(contract_year):
    assert contract_year.guaranteed_money_int == 40230320

