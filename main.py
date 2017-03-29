from time import time

class Process:

	def __init__(self,ID = 0, ArrivalTime = 0, ServiceTime = 0):
		self.id = ID
		self.arrival_time = float(ArrivalTime)
		self.serviceTime = float(ServiceTime)
		self.waitTime = 0
		self.turnAroundTime = 0
		self.notRun = True

	def __str__(self):
		return str(self.id) + " " + str(self.arrival_time) + " " +  str(self.waitTime) + " " + str(self.turnAroundTime)

class RoundRobin:

	def __init__(self,Processes=None):
		self.Processes = Processes
		self.Queue = list()
		self.timeQuantum  = 50
		self.QuantumList = [50,100,250.500]
		self.dispatch_overhead_time = 0
		self.dotList = [0,5,10,15,20,25]
		self.finishedProcesses = list()

	def Start(self):
		waitTime = 0;
		serviceTime = 0

		self.Queue.append(self.Processes.pop(0))

		while(len(self.Queue) > 0):

			
			current_process = self.Queue.pop(0)

			serviceTime = current_process.serviceTime
			#check if service time is less than quantum time
			if(serviceTime < self.timeQuantum):
				if(current_process.notRun):
					current_process.notRun = False
					current_process.waitTime = waitTime
				waitTime += serviceTime
				current_process.serviceTime = 0
				current_process.turnAroundTime = waitTime - current_process.arrival_time
				self.finishedProcesses.append(current_process)

				#sleep(serviceTime) #Wait for process to end
			else:
				if(current_process.notRun):
					current_process.notRun = False
					current_process.waitTime = waitTime
				waitTime += serviceTime
				current_process.serviceTime -= self.timeQuantum
				self.Queue.append(current_process)
				#sleep(self.timeQuantum)

			if(len(self.Processes) > 0):
				if(self.Processes[0].arrival_time <= waitTime):
					self.Queue.append(self.Processes.pop(0))
				else:
					waitTime += (self.Processes[0].arrival_time - waitTime)
					self.Queue.append(self.Processes.pop(0))

		for p in self.finishedProcesses:
			print(p)

	#def changingQuantumTime(self):

	#def changingOverheadTime(self):

# PROGRAM START HERE #

#	Import the list of processes and arrival times
Processes = list()
with open('p.txt','r') as p:
	i=1
	for line in p:
		line = line.strip('\n').split(' ')
		if(len(line) > 1):
			Processes.append( Process( i, float(line[0]), float(line[2]) ) )
		i += 1

#Start the roundrobin
RR = RoundRobin(Processes)
RR.Start()