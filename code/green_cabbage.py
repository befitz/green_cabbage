import os
import re
import time
import datetime

from connection import ib__api_connection as conn
from data_request import data_request as req


def _input_args():

	dict__input_args = {
		'request_type': {
			'arg_name': 'request_type',
			'allowed_values': [
				'historical_bars',
				'current_mkt_price'
				],
			'default_value':'historical_bars'
			# 'default_value': 'test'
		},
		'ticker': {
			'arg_name': 'ticker',
			# 'allowed_values': ['PLTR'],
			'default_value':'PLTR'
		},
		'historical_bars__duration': {
			'arg_name': 'historical_bars__duration',
			'allowed_values': 'integer (S|D|W|M|Y)',
			'default_value':'1 M'
		},
		'historical_bars__barSize': {
			'arg_name': 'historical_bars__barSize',
			'allowed_values': [
				'1 min', '2 mins', '3 mins', '5 mins', '10 mins', '15 mins',
				'20 mins', '30 mins', '1 hour', '2 hours', '3 hours', '4 hours',
				'8 hours', '1 day', '1W', '1M'
				],
			'default_value':'1 day'
		},
		'historical_bars__whatToShow': {
			'arg_name': 'historical_bars__whatToShow',
			'allowed_values': [
				'TRADES', 'MIDPOINT', 'BID', 'ASK', 'BID_ASK',
				'ADJUSTED_LAST', 'HISTORICAL_VOLATILITY', 'OPTION_IMPLIED_VOLATILITY',
				'REBATE_RATE', 'FEE_RATE', 'YIELD_BID', 'YIELD_ASK', 'YIELD_BID_ASK', 'YIELD_LAST'
				],
			'default_value':'MIDPOINT'
		},
	}

	return dict__input_args









# Project structure | Directories


def _process_run_find_working_directories(
	dict__proc,
):

	dict__proc['I__flag'] = False

	# Get the current working directory
	cwd = os.getcwd()

	if re.search(r'(.+)/code', cwd):
		dict__proc['cfg']['dir__root'] = re.search(r'(.+)/code', cwd).group(1)

		dict__proc['cfg']['dir__code'] = os.path.join(dict__proc['cfg']['dir__root'], 'code')
		dict__proc['cfg']['dir__dat'] = os.path.join(dict__proc['cfg']['dir__root'], 'data')

		print('Process Run Configuration | Identify working directories\n\troot:\n\t\t%s\n\tcode:\n\t\t%s\n\tdata:\n\t\t%s' %(
				dict__proc['cfg']['dir__root'],
				dict__proc['cfg']['dir__code'],
				dict__proc['cfg']['dir__dat']
			))
	else:
		print('Unable to identify root directory')


	return dict__proc







def process__run_configuration(
):
	
	# Initiate process dictionary
	dict__proc = {
		'cfg': {
			'dir__root': '',
			'dir__code': '',
			'dir__dat': '',
		},
		'project_name': 'green_cabbage',
		'input_args': {},
		'I__flag':False,
		'dat': {},

	}

	# Arg parse
	dict__input_args = _input_args()

	for arg_name in dict__input_args.keys():
		if 'value' not in dict__input_args[arg_name].keys():
			dict__proc['input_args'][arg_name]={
				'value': dict__input_args[arg_name]['default_value']
			}
		else:
			dict__proc['input_args'][arg_name]={
				'value': dict__input_args[arg_name]['value']
			}


	# Find code and data directories
	dict__proc = _process_run_find_working_directories(
		dict__proc=dict__proc
	)

	
	# Initiate connection dictionary
	dict__conn = {
		'cfg': {
			'host': '127.0.0.1',
			'port': 7497,
			'client_id': 1,
		},
		'status': 'disconnected', 
	}

	# Initiate logging
	dict__log = {}
	
	return dict__proc, dict__conn, dict__log




# Initiate process start time and input args


# Initiate connection and connection handles






if __name__ == '__main__':


	# Process run configuration
	dict__proc, dict__conn, dict__log = process__run_configuration(
		)


	# dict__proc['I__flag'] = False

    # Establish connection handle
	if not dict__proc['I__flag']:
		dict__proc, dict__conn, dict__log = conn.ibapi__connect(
			dict__proc=dict__proc,
			dict__conn=dict__conn,
			dict__log=dict__log
			)

    # Historical bars request
	if not dict__proc['I__flag']:
		dict__proc, dict__conn, dict__log = req.ib__data_request(
			dict__proc=dict__proc,
			dict__conn=dict__conn,
			dict__log=dict__log
			)


    # Close connection handle
	dict__proc, dict__conn, dict__log = conn.ibapi__disconnect(
		dict__proc=dict__proc,
		dict__conn=dict__conn,
		dict__log=dict__log
		)

# Close process with end time and save log data