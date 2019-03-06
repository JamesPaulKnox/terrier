from multiprocessing import Process
import feed, algo
import glob, time, copy

waitTime = 1800

def buildList():
	
	print("Built the list.")
	
	returnList = []
	with open("stocks", "r") as f:
		for i in f:
			returnList.append(i.rstrip())
	return returnList
	
def main():
	
	print("Starting feed programs")
	
	stocks = copy.copy(buildList())
	print(stocks)
	
	for stock in stocks:
		print(stock)
		client = stocks.index(stock) + 10
		print(client)
		print("Starting feed for {}".format(stock))
		p = Process(target=feed.main, args=(stock, client))
		p.start()
		print("Feed started. Client {}".format(client))
		
	print("Feed programs started")
	
if __name__ == '__main__':
	
	main()
