from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

from ib_insync import *

import datetime
import time
import pandas as pd
import os



def ib__data_request(
	dict__proc,
	dict__conn,
	dict__log
):

	dict__configuration = {
		# 'ib__api_connection': {'i__success':False, 'i__skip':False},
		'ib__historical_bars_request': {'i__success':False, 'i__skip':False},
		'ib__current_mkt_price': {'i__success':False, 'i__skip':False},
		# 'ib__api_disconnect': {'i__success':False, 'i__skip':False},
	}

	if dict__proc['input_args']['request_type']['value'] != 'historical_bars':
		for config_key in dict__configuration.keys():
			if config_key in ['ib__historical_bars_request']:
				dict__configuration[config_key]['i__skip'] = True
				print('Skipping %s | request type set to %s' %(
					config_key,
					dict__proc['input_args']['request_type']['value']
					))

	if dict__proc['input_args']['request_type']['value'] != 'current_mkt_price':
		for config_key in dict__configuration.keys():
			if config_key in ['ib__current_mkt_price']:
				dict__configuration[config_key]['i__skip'] = True
				print('Skipping %s | request type set to %s' %(
					config_key,
					dict__proc['input_args']['request_type']['value']
					))


	# ib__historical_bars_request
	s__configuration_step = 'ib__historical_bars_request'

	if not dict__configuration[s__configuration_step]['i__skip']:
		
		if not dict__proc['I__flag']:

			
			dict__proc, dict__conn, dict__log = ib__historical_bars_request(
				dict__proc=dict__proc,
				dict__conn=dict__conn,
				dict__log=dict__log
				)

			time.sleep(5)

	# ib__current_mkt_price
	s__configuration_step = 'ib__current_mkt_price'

	if not dict__configuration[s__configuration_step]['i__skip']:
		
		if not dict__proc['I__flag']:
			
			dict__proc, dict__conn, dict__log = ib__current_mkt_price(
				dict__proc=dict__proc,
				dict__conn=dict__conn,
				dict__log=dict__log
				)

			time.sleep(5)

	return dict__proc, dict__conn, dict__log






def _ticker(
	symbol,
	sec_type="STK",
	currency="USD",
	exchange="SMART"
):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    
    return contract 



# Request historical bars
def ib__historical_bars_request(
	dict__proc,
	dict__conn,
	dict__log
):
	dict__proc['I__flag'] = False

	# Ticker
	# contract = _ticker(
	# 	symbol=dict__proc['input_args']['ticker']['value'],
	# 	)
	contract = Stock(
		dict__proc['input_args']['ticker']['value'],
		'SMART',
		'USD'
		)

	# print(dict__conn['app'].isConnected())

	# queryTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	# queryTime = time.strftime('%Y%m%d %H:%M:%S')
	try:
		bars = dict__conn['app'].reqHistoricalData(
		        contract=contract,
		        endDateTime='',
		        durationStr=dict__proc['input_args']['historical_bars__duration']['value'],
		        barSizeSetting=dict__proc['input_args']['historical_bars__barSize']['value'],
		        whatToShow=dict__proc['input_args']['historical_bars__whatToShow']['value'],
		        useRTH=True,
		        # formatDate=1,
		        # keepUpToDate=False,
		        # chartOptions=[]
			)

		dict__proc['dat']['result'] = util.df(bars)

		# print(dict__proc['dat']['result'].head())
		dict__proc, dict__log = _outupt_data(
			dict__proc=dict__proc,
			dict__log=dict__log,
			)

	except Exception as e:
		print('Unable to gather historical bars')
		print(str(e))



	return dict__proc, dict__conn, dict__log




def _outupt_data(
	dict__proc,
	dict__log
	):
	

	s__duration = '_'.join(dict__proc['input_args']['historical_bars__duration']['value'].split(' '))
	s__bars = '_'.join(dict__proc['input_args']['historical_bars__barSize']['value'].split(' '))
	s__time = datetime.datetime.now().strftime('%Y%m%d')

	fn__output = dict__proc['project_name'] + '__' + \
		dict__proc['input_args']['request_type']['value'] + '_' + \
		s__duration + '_by_' + s__bars + '_bars__' + s__time + '.csv'



	if 'result' in dict__proc['dat'].keys():
		try:
			dict__proc['dat']['result'].to_csv(
				os.path.join(
					dict__proc['cfg']['dir__dat'],
					fn__output),
				index=False,
				)
		except Exception as e:
			print(str(e))
	else:
		dict__proc['I__flag'] = True
		print('results not avail.')

	return dict__proc, dict__log



def ib__current_mkt_price(
	dict__proc,
	dict__conn,
	dict__log
):
	dict__proc['I__flag'] = False

	# contract = _ticker(
	# 	symbol=dict__proc['input_args']['ticker']['value'],
	# 	)

	contract = Stock(
		dict__proc['input_args']['ticker']['value'],
		'SMART',
		'USD'
		)
	#Request Market Data
	dict__conn['app'].reqMktData(
		reqId = 1, # TickerId
		contract = contract, 
		genericTickList= '',
		snapshot=False,
		regulatorySnapshot=False,
		mktDataOptions = []
		)
	
	dict__conn['app'].run()

	# print(dir(dict__conn['app'].reqMktData))

	# print(dict__conn['app'].reqMktData)

	return dict__proc, dict__conn, dict__log