import ib_insync as insync
import numpy as np
import datetime as dt
import copy

########################################################################
# Function: reqMktData #################################################
# This will pull live market data, for as long as it is running ########
########################################################################

def reqMktData(tickerList, client, waitTime):
	ib = insync.IB()
	contractList = []
	ib.connect('127.0.0.1', 7497, clientId=client)
	
	for ticker in tickerList:
		ticker = ticker.rstrip().upper()
		contract = insync.Stock(ticker, "SMART", "USD")
		ib.qualifyContracts(contract)
		ib.reqMktData(contract, "", False, False)
		contractList.append({"ticker":ticker, "contract":contract})

	ib.sleep(5)

	while True:
		t = copy.copy(dt.datetime.now())
		tWait = copy.copy(t + dt.timedelta(seconds=waitTime))
		
		for contract in contractList:
			fileName = "{}_mkt.npy".format(contract["ticker"])
			print("{} - STREAMING {}".format(dt.datetime.now(), contract["ticker"]))
			np.save(fileName, ib.ticker(contract["contract"]))
		
		t = copy.copy(dt.datetime.now())
		sleepTime = (tWait - t).total_seconds()
		ib.sleep(sleepTime)

########################################################################
# Function: reqHistoricalData ##########################################
# Pulls bar data from over the past period, until now. #################
########################################################################

def reqHistoricalData(tickerList, client, waitTime,
					duration, barSize, whatToShow):
	ib = insync.IB()
	contractList = []
	ib.connect('127.0.0.1', 7497, clientId=client)
	
	for ticker in tickerList:
		ticker = ticker.rstrip().upper()
		contract = insync.Stock(ticker, "SMART", "USD")
		ib.qualifyContracts(contract)
		contractList.append({"ticker":ticker, "contract":contract})

	ib.sleep(5)

	while True:
		t = copy.copy(dt.datetime.now())
		tWait = copy.copy(t + dt.timedelta(seconds=waitTime))
		
		for contract in contractList:
			fileName = "{}_bar.npy".format(contract["ticker"])
			print("{} - STREAMING {}".format(dt.datetime.now(), contract["ticker"]))
			
			bars = ib.reqHistoricalData(
					contract["contract"],
					endDateTime="",
					durationStr=duration,
					barSizeSetting=barSize,
					whatToShow=whatToShow,
					useRTH=True,
					formatDate=1)
			
			np.save(fileName, bars)
		
		t = copy.copy(dt.datetime.now())
		sleepTime = (tWait - t).total_seconds()
		ib.sleep(sleepTime)

########################################################################
# END OF FUNCTIONS #####################################################
########################################################################

if __name__ == "__main__":
	reqHistoricalData(["aapl", "tsla", "xom"], 1, 5, "10 D", "15 mins", "MIDPOINT")
