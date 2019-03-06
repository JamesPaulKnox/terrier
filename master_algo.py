from multiprocessing import Process
import algo
import glob, time, copy

def buildList():
	
	print("Built the list.")
	
	returnList = []
	with open("stocks", "r") as f:
		for i in f:
			returnList.append(i.rstrip())
	return returnList
	
def main():
	
	print("Starting algo programs")
	
	for i in buildList():
		print("Starting algo for {}".format(i))
		p = Process(target=algo.main, args=(i,))
		p.start()
		print("Algo started.")
		
	print("Algo programs started.")
	
if __name__ == '__main__':
	
	main()
