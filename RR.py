class Process:

	def __init__(self, ID,ArrivalTime,ServiceTime):
		self.id = ID
		self.arrival_time = ArrivalTime
		self.serviceTime = ServiceTime
		self.waitTime = 0
		self.turnAroundTime = 0
		self.notRun = True 	#Bool to check first use

	#Allows for printing Process Object as string
	def __str__(self):
		return	str(self.id) + " " + str(self.arrival_time) + " " +  str(self.waitTime) + " " + str(self.turnAroundTime)

class RoundRobin:

	def __init__(self,Processes=None):
		self.Processes = Processes
		self.QuantumList = [50,100,250,500]	#List of Time Quantimes
		self.dispatchTimes = [0,5,10,15,20,25]	#List of dispatch overhead times

	@staticmethod
	def execute(ProcessesList,TimeQuantum,DispatchOverheadTime):
		# Nessesary Variables
		waitTime = 0
		serviceTime = 0
		timeQuantum = TimeQuantum
		dispatch_overhead_time = DispatchOverheadTime
		Processes = ProcessesList #Grab the list of processes to be analyzed
		pQueue = list()	#queue to hold processes still in use
		finishedProcesses = list() #processes once done go in here for safe keeping

		#Lets grab the first process from the List and drop it into the queue
		print(TimeQuantum,DispatchOverheadTime)
		pQueue.append(Processes.pop(0))

		while(len(pQueue) > 0):	#as long as there is an item in the queue, lets process it
			
			current_process = pQueue.pop(0)
			serviceTime = current_process.serviceTime

			if(serviceTime < timeQuantum):
				#check if it has ever been run, so we can set the wait time
				if(current_process.notRun):
					current_process.waitTime = waitTime
					current_process.notRun = False
				#update the wait time with process service time
				waitTime += serviceTime
				#since the service time was less than the time quantum,
				#we won't use the entire time, lets only use what is needed
				current_process.serviceTime = 0
				#since this process is done, lets set the turnaround time to the time
				#difference between when the process arrived and the current wait time
				current_process.turnAroundTime = waitTime - current_process.arrival_time
				#sleep(serviceTime) #we can sleep if we want a full simulation with time
				#this process is finished so we can stash it in the finished processes list
				finishedProcesses.append(current_process)
			else:
				#here we will take the entire time quantum
				#check if it has ever been run, so we can set the wait time
				if(current_process.notRun):
					current_process.notRun = False
					current_process.waitTime = waitTime
				#update the wait time with process service time
				waitTime += serviceTime
				# deduct the time quantum from the process service time so we know how much is left
				current_process.serviceTime -= timeQuantum
				#since this process isn't finished, lets add it to the queue, so we can continue
				#processing it once it's turn comes around again
				pQueue.append(current_process)

			#lets check if there are any processes left in the original list
			if(len(Processes) > 0):
				#if there are, lets check the arrival time
				#if the next process came in before our current wait time
				#add it to the queue so we can start servicing it when it comes to its turn
				if(Processes[0].arrival_time <= waitTime):
					pQueue.append(Processes.pop(0))
				else:
					#if the next process hasn't arrived yet, lets wait for it
					#updating the wait time once it arrives
					#and lets add it now to the queue
					waitTime += (Processes[0].arrival_time - waitTime)
					pQueue.append(Processes.pop(0))

			#We are now changing processes, so lets drop in to the wait time
			#the Dispatch Overhead Time it takes to switch processes
			waitTime += dispatch_overhead_time

		#Once we have finished, lets return the finishedProcesses list
		return finishedProcesses

	def analasys(self):
		#lets make a list to store all the finishedprocesses list
		#for each changed timeQuantum
		TQ_Processes = list()
		for TimeQuantum in self.QuantumList:
			for DispatchOverheadTime in self.dispatchTimes:
				TQ_Processes.append(RoundRobin.execute(self.Processes,TimeQuantum,DispatchOverheadTime))

		

## Lets import the processes ##
Prs = list()
with open('p.txt','r') as p:
	i=1
	for line in p:
		line = line.strip('\n').split(' ')
		if(len(line) > 1):
			Prs.append( Process(i, float(line[0]), float(line[2])) )
		i += 1

### START ###
RR = RoundRobin(Prs)
#Prs = RR.execute(Prs,50,10)

Prs = RR.analasys()