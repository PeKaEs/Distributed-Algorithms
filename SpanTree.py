from time import sleep
from threading import Thread as Machine
from Queue import Queue as connTunel

class Node(Machine):
    def __init__( self, uID ):
        Machine.__init__(self)
        self.cTunnel = connTunel()

        self.uID = uID
        self.nParent = None
        self.nNeighbours = []
        self.nChildrens = []
        self.killSwitch = False
        self.bWannaInactive = False

    def get_uid( self ):
        return self.uID

    def kill( self ):
        self.killSwitch = True

    def set_neighbours( self, neighbours ):
        self.nNeighbours = neighbours
        self.iNeighboursCounter = 0
        self.iNeighboursCount = len( neighbours )

    def get_childrens( self ):
        return [tmp.get_uid() for tmp in self.nChildrens]

    def get_parrent( self ):
        return self.nParent.get_uid()

    def send_message( self, *tMessage ):
        self.cTunnel.put( tMessage )

    def run(self):
        while not self.killSwitch:
            while not self.cTunnel.empty():
                sFunc, sParam = self.cTunnel.get()
                self.__getattribute__( sFunc )( sParam )


    def parrent_request( self, nPossibleParent ):
        if self.nParent is None:
            self.nParent = nPossibleParent

            for nNeighbour in self.nNeighbours:
                nNeighbour.send_message( "parrent_request", self )
                sleep(1)

            self.nParent.send_message( "parrent_request_aproved", self )
        else:
            nPossibleParent.send_message( "parrent_request_refused", None)

    def parrent_request_aproved( self, childrenNode ):
        self.nChildrens.append( childrenNode )
        self.autodeath_counter()

    def parrent_request_refused( self, *args):
        self.autodeath_counter()

    def autodeath_counter(self):
        self.iNeighboursCounter += 1
        if self.iNeighboursCounter >= self.iNeighboursCount:
            self.bWannaInactive = True

def main():
    G = {
        0: [2, 3],
        1: [0, 4],
        2: [0, 3, 4],
        3: [0,2],
        4: [0, 1, 2, 3]
    }

    nMachines = [ Node( uid ) for uid in G ]
    for node in nMachines:
        node.set_neighbours ( [ tmpNode for tmpNode in nMachines if tmpNode.uID in G[ node.get_uid() ] ] )

    for node in nMachines:
        node.start()

    nMachines[0].send_message( "parrent_request", nMachines[0] )

    loopSwitch = True
    while loopSwitch:
        sizeOfGraph = len ( nMachines )
        inactiveCounter = 0
        for node in nMachines:
            if node.bWannaInactive:
                inactiveCounter += 1

        if inactiveCounter == sizeOfGraph:
            loopSwitch = False
            for node in nMachines:
                node.kill()

    for node in nMachines:
        print( "Node uid: {}||\t Parent uid:{}\tChildrens uids: {}".format( node.get_uid(), node.get_parrent(), node.get_childrens() ) )


if __name__ == "__main__":
    main()
