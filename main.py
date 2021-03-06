import threading
import station
import time
import random

"""
this is the actual implementation of the network
"""



#the probability for a station to send his package
SENT_PROB = 0.5


#initialize all the workstations

stations = [ station.station(5,i) for i in range(8)]


def auxiliary():
    """
    function that does nothing,to be passed to the timer
    """
    pass

def packagecreation(stations,probability,slot):
    """
    function that handles the creation of the packages at each time slot
    """
    for station in stations :
        station.createpack(probability,slot) 

def packageshipment(stations,probability,slot):
    """
    function that handles the package shipment
    from each station with collision detection
    """
    #figure out which stations will compete for the medium
    for station in stations :
        n = random.random()
        if n < probability :
            station.WANT_TO_SENT=True

    #check for collisions and send the packages
    for i in range(0,7,2) :
        if  stations[i].WANT_TO_SENT and stations[i+1].WANT_TO_SENT : 
            stations[i].WANT_TO_SENT = False
            stations[i+1].WANT_TO_SENT = False
        else:
            if stations[i].WANT_TO_SENT : 
                stations[i].sendpack(slot)
                stations[i].WANT_TO_SENT = False
            elif stations[i+1].WANT_TO_SENT : 
                stations[i+1].sendpack(slot)
                stations[i+1].WANT_TO_SENT = False


#the main function of the program
def main(SIM_TIME,CREATION_CHANCE,TIME_SLOT=0.1):
    #mark the start of the simulation 
    for station in stations :
        station.buffer=[]
        station.delay['delay']=0
        station.delay['packages']=0
    start = time.time()
    slot=0
    #start the simulation itself
    while time.time() - start < float(SIM_TIME) :
        timer = threading.Timer(TIME_SLOT,auxiliary) 
        slot += 1
        timer.start()
        packageshipment(stations,SENT_PROB,slot)
        packagecreation(stations,CREATION_CHANCE,slot)
        timer.join()
    
    #calculate the network total delay for the packages
    totaldelay = 0
    for station in stations:
        if not station.delay['packages']:
            continue
        totaldelay += station.delay['delay']/station.delay['packages']
    network_total_delay = totaldelay/8
    
    #calculate the total number of packages that the network sent
    total_packages=0
    for station in stations:
        total_packages += station.delay['packages']
    #calculate the thoughput of the network
    throughput = total_packages/(slot)

    return (network_total_delay,throughput)
