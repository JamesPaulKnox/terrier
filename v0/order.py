# Find all files ending in "_decision.npy" and save in a list.
# Iterate through the files, storing the contents of each in a master-list.
#     It will be a list of dicts.
#     {"symbol":symbol, "decision":decision, "buySize":buySize}
# 
# call IB positions() and save it to a list of dicts, formatted as such
#     {symbol, posSize}
#
# If decision is a 1 AND posSize < 1, send a market buy of buySize.
#      Then, posSize = posSize + buySize
# If decision is a -1 AND posSize > 0, send a market sell of posSize
#      Then, posSize = 0

import ib_insync as insync
import numpy as np
import glob, time, copy, datetime, random

ib = insync.IB()



def updatePositions():
	
	global positionList
	positionList = [] # empty positions list
	
	global symbolList
	symbolList = []
	
	for i in ib.positions():
		posSize = i[2]
		symbol = i[1].symbol # i[1] returns a symbol object.
		
		positionList.append({"symbol":symbol, "posSize":posSize})
		symbolList.append(symbol)



def updateDecisions():
	
	global decisionList
	decisionList = [] # empty decisions list
	
	files = glob.glob("*_decision.npy")
	
	for i in files:
		try:
			content = np.load(i)
		except:
			waitTime = copy.copy(random.random())
			print("File in use. Waiting {} seconds.".format(waitTime))
			time.sleep(waitTime)
			content = np.load(i)
			
		decisionList.append(content)

def marketOrder(action, size, symbol):
	print("CONTRACT")
	contract = insync.Stock(symbol, 'SMART', 'USD')
	print("ORDER")
	order = insync.MarketOrder(action, size)
	print("QUALIFY")
	ib.qualifyContracts(contract)
	print("PLACE")
	ib.placeOrder(contract, order)



def testDecisions():
	updatePositions()
	updateDecisions()
	
	# ~ print(symbolList)
	
	print("{} - Positions & Decisions updated!".format(datetime.datetime.now()))
	
	for i in decisionList:
		
		# ~ print("Start for loop")
		
		symbol = i.item()["symbol"]
		decision = int(i.item()["decision"])
		buySize = int(i.item()["buySize"])
		
		# ~ print("Assigned {} variables".format(symbol))
		
		# ~ print("TESTING: {}, {}, {}".format(symbol, decision, buySize))
		
		# ~ print(decision)
		# ~ print(type(decision))
		
		if decision == 1:
			# ~ print("Buy")
			if symbol in symbolList:
				# ~ print("Cancel. Already owned.")
				pass
			else:
				# ~ print("BUY")
				marketOrder("BUY", buySize, symbol)
				print("BUY {} of {}".format(buySize, symbol))
			
		elif decision <= 0:
			# ~ print("Sell")
			if symbol in symbolList:
				# ~ print("SEARCH")
				for entry in positionList:
					if entry["symbol"] == symbol:
						sellSize = entry["posSize"]
				# ~ print("SELL")
				marketOrder("SELL", sellSize, symbol)
				print("SELL {} of {}".format(sellSize, symbol))



def is_time_between(begin_time, end_time, check_time):
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def blockUnfilled():
	global t
	
	while ib.openOrders() != [] and ib.waitUntil(t):
		print("There are outstanding orders. [recheck in 5]")
		t = t + datetime.timedelta(seconds=5)


def main():
	ib.connect('127.0.0.1', 7497, clientId=1000, timeout=30)	
	
	counter = 0
	t = datetime.datetime.now()
	
	
	while ib.waitUntil(t): # See 1_terrier for details on ib.waitUntil(t)
		 # See 1_terrier for details
		 
		print("Starting loop. t = {}".format(t))
		
		if is_time_between(datetime.time(9, 35), datetime.time(15,55), datetime.datetime.now().time()):
			t = t + datetime.timedelta(seconds=1)
			testDecisions()
		elif is_time_between(datetime.time(16,1), datetime.time(9,29), datetime.datetime.now().time()):
			t = t + datetime.timedelta(seconds=60)
			if ib.isConnected():
				ib.reqGlobalCancel()
				ib.disconnect()
			print("It is outside of specified trading time. Waiting 60 seconds.")
		else:
			t = t + datetime.timedelta(seconds=15)
			if not ib.isConnected():
				ib.connect('127.0.0.1', 7497, clientId=1000)
			print("Waiting 15 seconds for time margins to pass.")

		print("Finished loop. Next loop: {}".format(t))
if __name__ == "__main__":
    main()
