import os
import time
import random

MASTER_IP = "10.0.0.1"
PASSIVE_EP_1 = "10.0.0.20"

WHO                     = os.getenv("WHO", "¯\\_(ツ)_/¯")
SEED                    = int(os.getenv("SEED", 69))
MIN_ONLINE_TIME        = int(os.getenv("MIN_ONLINE_TIME", 3))
MAX_ONLINE_TIME        = int(os.getenv("MAX_ONLINE_TIME", 15))
MIN_OFFLINE_TIME    = int(os.getenv("MIN_OFFLINE_TIME", 3))
MAX_OFFLINE_TIME    = int(os.getenv("MAX_OFFLINE_TIME", 10))

random.seed(SEED, version=2)

def master() :
    print("I am master.", flush=True)
    os.system("tail -f /dev/null")


def active_endpoint() :
    while True :
        online_time:int = random.randint(MIN_ONLINE_TIME, MAX_ONLINE_TIME)
        offline_time:int = random.randint(MIN_OFFLINE_TIME, MAX_OFFLINE_TIME)
        
        print(f"Now ONLINE for {online_time}s.", flush=True)
        os.system(f"ping {MASTER_IP} -c {online_time} -i 1 > /dev/null")
        
        print(f"Now OFFLINE for {offline_time}s.", flush=True)
        time.sleep(offline_time)

def passive_endpoint() :
    while True :
        online_time:int = random.randint(MIN_ONLINE_TIME, MAX_ONLINE_TIME)
        offline_time:int = random.randint(MIN_OFFLINE_TIME, MAX_OFFLINE_TIME)
        
        print(f"Now OFFLINE for {offline_time}s.", flush=True)
        os.system("iptables -A INPUT -p icmp --icmp-type echo-request -j DROP")
        time.sleep(offline_time)

        print(f"Now ONLINE for {online_time}s.", flush=True)
        os.system("iptables -D INPUT -p icmp --icmp-type echo-request -j DROP")
        time.sleep(online_time)


if __name__ == "__main__" :
    match WHO :
        case "master" :
            master()
            
        case "active-ep-1" :
            active_endpoint()

        case "passive-ep-1" :
            passive_endpoint()

        case _ :
            print("UNKNOWN !!")


