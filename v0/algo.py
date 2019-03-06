import numpy as np
import copy, time, random


sma_big = []
sma_mid = []
sma_now = []

smoothing = 10

def sma(data, period):
	
	data = copy.copy(data[0:period])

	dataSum = 0
	for i in data:
		dataSum = dataSum + i["midpoint"]
	
	mean = dataSum / len(data)	
	return mean

def avg(data):
	mean = sum(data) / len(data)	
	return mean
	
def decider(sma_now, sma_mid, sma_big):
	
	if sma_now >= sma_mid >= sma_big:
		return 1
	
	elif sma_now <= sma_mid <= sma_big:
		return -1
		
	else:
		return 0
	
def main(symbol):
	while True:
		try:
			try:
				counter = counter + 1
			except:
				counter = 0
			
			time.sleep(1)
			
			try:
				dataSet = copy.copy(np.load(symbol + ".npy"))
			except:
				time.sleep(random.random())
				dataSet = copy.copy(np.load(symbol + ".npy"))

			sma_big.insert(0, sma(dataSet, 1800))
			sma_mid.insert(0, sma(dataSet, 450))
			sma_now.insert(0, sma(dataSet, 225))
				
			while len(sma_big) > smoothing:
				del sma_big[-1]
			while len(sma_mid) > smoothing:
				del sma_mid[-1]
			while len(sma_now) > smoothing:
				del sma_now[-1]
			
			midpoint = dataSet[0]["midpoint"]

			if counter > (smoothing * 1.5):

				decision = decider(avg(sma_now[0:smoothing - 1]), avg(sma_mid[0:smoothing - 1]), avg(sma_big[0:smoothing - 1]))

				print("DECISION: {} {}".format(decision, symbol))
				
				# ~ budget = 1000
				
				# ~ buySize = budget / dataSet[0]["ask"]
				# ~ buySize = round(buySize)
				
				buySize = 100
				
				# ~ print(buySize)
				
				output = {"symbol":symbol, "decision":decision, "buySize":buySize}
				
				try:
					np.save(symbol + "_decision.npy", output)
				except:
					time.sleep(random.random())
					np.save(symbol + "_decision.npy", output)
					
		except Exception as e: print(e)
if __name__ == "__main__":
	print("This program will interpret the data provided from the previous.")
	print("It will make a decision and output that to a file, to be ordered.")
	print("-------------------------------------------------------------------")
	symbol = input("Symbol:  ").upper()
	main(symbol)
