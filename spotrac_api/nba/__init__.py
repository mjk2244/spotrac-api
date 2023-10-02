import sys

import spotrac_api.nba.contract_year as contract_year
sys.modules['contract_year'] = contract_year

import spotrac_api.nba.contract as contract
sys.modules['contract'] = contract

import spotrac_api.nba.constants as constants
sys.modules['constants'] = constants

import spotrac_api.transaction as transaction
sys.modules['transaction'] = transaction

import spotrac_api.nba.player as player
sys.modules['player'] = player
