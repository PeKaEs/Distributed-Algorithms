import threading
from time import sleep

class Bakery:

    def __init__(self, NumberOfThreads):
        self.choosenThread = []
        self.nbr = []
        self.NumberOfThreads = NumberOfThreads

        for i in range(self.NumberOfThreads + 1):
            self.choosenThread.append(0)
            self.nbr.append(0)

    def criticial_section(self, ID):
        print "\n Thread : " +str(ID) + "\t\t\tin Critical Section",
        sleep(2)

    def enter_procedure(self, ID, criticial_section):
        self.choosenThread[ID] = 1
        self.nbr[ID] = 1 + max(self.nbr)
        maxValue = self.nbr[ID]

        print "\n Thread : " + str(ID) + "\tToken: " + str(maxValue) + " assigned",
        self.choosenThread[ID] = 0

        for i in range (self.NumberOfThreads):
            if i != ID:
                while self.choosenThread[i] != 0:
                    pass
                while (self.nbr[i] != 0 and (self.nbr[ID] > self.nbr[i] or (self.nbr[i] == self.nbr[ID] and ID > i))):
                    pass

        print "\n Thread : " + str(ID) + "\t\tentering Critical Section Token: " + str(self.nbr[ID]),
        self.criticial_section(ID)
        print "\n Thread : " + str(ID) + "\t\texiting Critical Section Token: " + str(self.nbr[ID]),
        self.nbr[ID] = 0

    def thread_request(self, ID, criticial_section):
        while True:
            print "\n Thread : " + str(ID) + " requesting Critical Section",
            self.enter_procedure(ID, criticial_section)

NumberOfThreads = 10
bakery = Bakery(NumberOfThreads)
criticial_section = 0

try:
    for count in range(NumberOfThreads):
        newThread = threading.Thread(target=bakery.thread_request, args=[count, criticial_section])
        newThread.start()
except:
   print "\nCan not start the thread",
