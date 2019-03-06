import ib_insync as insync
import numpy as np
import datetime


def main(symbol, client):
	ib = insync.IB()
	ib.connect('127.0.0.1', 7497, clientId=client)
	# Connects to the IB TWS/GW under the client ID specified

	contract = insync.Stock(symbol, "SMART", "USD")
	ib.qualifyContracts(contract)
	# qualifyContracts fills in missing, required information

	ib.reqMktData(contract, "", False, False) 
	# reqMktData starts the data stream

	my_tick = ib.ticker(contract)
	ib.sleep(1)
	# Waits a bit to ensure stream has begun

	file_name = symbol + ".npy"
	dataSet = []
	t = datetime.datetime.now()

	while ib.waitUntil(t):
		t = t + datetime.timedelta(seconds=1)
		# Executes the loop once per second. Not the same as waiting
		# for a second between loops. Accounts for the time it takes
		# the code to execute during loop. Will never start early. 
		# Could get behind of the code takes longer than a second
		# to execute.
		
		dataPoint = {"midpoint" : my_tick.midpoint(), \
					"bid" : my_tick.bid, \
					"ask" : my_tick.ask }
		
		dataSet.insert(0, dataPoint)
		
		while len(dataSet) > 1800:
			del dataSet[-1]
			
		if len(dataSet) == 1800:
			np.save(symbol + ".npy", dataSet)
			
		# ~ print(dataSet[0])
		print("STREAMING {} - CLIENT {} - DATASET {} - MIDPOINT {}".format(symbol, client, len(dataSet), dataPoint["midpoint"]))

if __name__ == "__main__":
	print("This program will collect second-data from Interactive Brokers.")
	print("It will be saved into a file, ready for a decision program to read.")
	print("-------------------------------------------------------------------")
	symbol = input("Symbol:  ").upper()
	client = int(input("Client ID:  "))
	main(symbol, client)
