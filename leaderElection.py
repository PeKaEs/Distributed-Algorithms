#####################################################################
## Simple disturbed algorithm for leader election in ring topology ##
## Time complexity O(n)                                            ##
## Exhanged messages O(n^2)                                        ##
#####################################################################

from time import sleep
from threading import Thread as Machine
from Queue import Queue as connTunel

class Node(Machine):
    def __init__( self, uID ):
        Machine.__init__(self)
        self.cTunnel = connTunel()

        self.uID = uID

        self.neighbour = None
        self.state = ""
        self.leaderUID = None

        self.everyone = []

        self.killSwitch = False
        self.bWannaInactive = False

    def get_uid( self ):
        return self.uID

    def kill( self ):
        self.killSwitch = True

    def set_neighbour( self, neighbour ):
        self.neighbour = neighbour

    def set_everyone(self, everyone):
        self.everyone = everyone

    def send_message( self, *tMessage ):
        self.cTunnel.put( tMessage )

    def run(self):
        while not self.killSwitch:
            while not self.cTunnel.empty():
                sFunc, sParam = self.cTunnel.get()
                self.__getattribute__( sFunc )( sParam )


    def request( self, receivedUID ):

        if receivedUID > self.uID:
            self.state = "NotLeader"
            self.neighbour.send_message( "request", receivedUID )
            return

        if receivedUID == self.uID:
            self.state = "Leader"
            for node in self.everyone:
                node.send_message("leader_elected", self)
            self.leaderUID = self.uID
            self.killSwitch = True
            self.bWannaInactive = True

        if receivedUID < self.uID and self.state != "NotLeader":
            self.neighbour.send_message( "request", self.uID )

    def leader_elected( self, theLeader):
        self.leaderUID = theLeader.get_uid()
        self.killSwitch = True
        self.bWannaInactive = True

    def get_leader( self ):
        return self.leaderUID

    def get_state( self ):
        return self.state

def get_node_with_uid(nodes, uid):
    for node in nodes:
        if node.get_uid() == uid:
            return node
    return None

def main():
    G = {
        0: 1,
        1: 2,
        2: 3,
        3: 4,
        4: 5,
        5: 0
    }

    ringSize = len(G)

    nMachines = [ Node( uid ) for uid in G ]
    for node in nMachines:
        node.set_neighbour( get_node_with_uid(nMachines, (node.get_uid()+1) % ringSize ))
        node.set_everyone( [ tmpNode for tmpNode in nMachines if tmpNode.get_uid() != node.get_uid()] )

    for node in nMachines:
        node.start()

    for node in nMachines:
        node.send_message( "request", -1 )

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
        print( "Node uid: {}||\tNode leader UID: {}\tNode state: {}".format( node.get_uid(), node.get_leader(), node.get_state() ) )


if __name__ == "__main__":
    main()
