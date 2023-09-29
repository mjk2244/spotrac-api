from spotrac_api.nba.contract import Contract
from bs4 import BeautifulSoup
import pytest

@pytest.fixture
def zion_contract():
    with open('zion_williamson.html', 'r') as f:
        return Contract(BeautifulSoup(f.read(), 'html.parser'))

def test_parse_contract_years(zion_contract):
    contract_years = zion_contract.parse_contract_years(zion_contract._raw_data)
    assert len(contract_years) == 5
    assert contract_years[0].current_year == True
    assert contract_years[0].base_salary == '$34,005,250'
    assert contract_years[0].likely_incentives == '$0'

def test_parse_summary(zion_contract):
    assert zion_contract.parse_summary(zion_contract._raw_data) == ('Zion Williamson signed a 5 year / '
    '$197,230,450 contract with the New Orleans Pelicans, including  $197,230,450 guaranteed, and an annual '
    'average salary of $39,446,090. In 2023-24, Williamson will earn a base salary of $34,005,250, while '
    'carrying a cap hit of $34,005,250 and a dead cap value of $34,005,250.')

def test_parse_terms(zion_contract):
    assert zion_contract.parse_terms(zion_contract._raw_data) == '5 yr(s) / $197,230,450'

def test_parse_aav(zion_contract):
    assert zion_contract.parse_aav(zion_contract._raw_data) == '$39,446,090'

def test_parse_gtd_at_sign(zion_contract):
    assert zion_contract.parse_gtd_at_sign(zion_contract._raw_data) == '$197,230,450'

def test_parse_signed_using(zion_contract):
    assert zion_contract.parse_signed_using(zion_contract._raw_data) == 'Designated Rookie Extension/Bird'

def test_parse_free_agent(zion_contract):
    assert zion_contract.parse_free_agent(zion_contract._raw_data) == '2028 / UFA'

def test_parse_notes(zion_contract):
    notes = zion_contract.parse_notes(zion_contract._raw_data)
    assert notes[0] == 'No All-NBA: $193M (25%)'
    assert notes[1] == 'All-NBA: $231M (30%)'
    print(notes[2])
    assert notes[2] == 'Protections TBDWeight must be less than 295 lbs; body fat monitored (@cclark_13)'

def test_contract_years(zion_contract):
    assert len(zion_contract.contract_years) == 5
    assert zion_contract.contract_years[4].base_salary_int == 44886930

def test_summary(zion_contract):
    assert zion_contract.summary == ('Zion Williamson signed a 5 year / '
    '$197,230,450 contract with the New Orleans Pelicans, including  $197,230,450 guaranteed, and an annual '
    'average salary of $39,446,090. In 2023-24, Williamson will earn a base salary of $34,005,250, while '
    'carrying a cap hit of $34,005,250 and a dead cap value of $34,005,250.')

def test_terms(zion_contract):
    assert zion_contract.terms == '5 yr(s) / $197,230,450'

def test_length(zion_contract):
    assert zion_contract.length == 5

def test_years_remaining(zion_contract):
    assert zion_contract.years_remaining == 5

def test_avg_salary(zion_contract):
    assert zion_contract.avg_salary == '$39,446,090'

def test_avg_salary_int(zion_contract):
    assert zion_contract.avg_salary_int == 39446090

def test_gtd_at_sign(zion_contract):
    assert zion_contract.gtd_at_sign == '$197,230,450'

def test_gtd_at_sign_int(zion_contract):
    assert zion_contract.gtd_at_sign_int == 197230450

def test_signed_using(zion_contract):
    assert zion_contract.signed_using == 'Designated Rookie Extension/Bird'

def test_free_agent(zion_contract):
    assert zion_contract.free_agent == '2028 / UFA'

def test_free_agent_tuple(zion_contract):
    assert zion_contract.free_agent_tuple == (2028, 'UFA')

def test_notes(zion_contract):
    assert len(zion_contract.notes) == 4
    assert zion_contract.notes[0] == 'No All-NBA: $193M (25%)'

def test_dollars_to_int(zion_contract, amount = '$5,000,000'):
    assert zion_contract.dollars_to_int(amount)
    