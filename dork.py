import requests
import threading
import random
import multiprocessing
from pyfiglet import figlet_format
from termcolor import colored


dorks = []
proxies = []
fuzz = []
headers = [{}]
tried = set()
vulnerable = []
fuzzvuln = []
threadsfuzz = []
threadsmain = []
fuzztried = set()
lock = threading.Lock()
4


def Vulnsearch():
    target = input("ENTER A DOMAIN")
    threadcount = multiprocessing.cpu_count()
    def task(target):
        reqcount = 0
        rp = random.randint(0, len(proxies)-1)
        rh = random.randint(0, len(headers)-1)
        for i in range(len(dorks)):
            if dorks[i] not in tried:
                with lock:
                    tried.add(dorks[i])
                    
                URL = "https://" + dorks[i] + target
                try:            
                    s = requests.get(URL, proxies=proxies[rp], headers=headers[rh])
                    reqcount += 1
                    if s.status_code in [202,200,302]:
                        with lock:
                                vulnerable.append("https://" + dorks[i] + target)
                    elif s.status_code == 403:
                        try:
                            for i in range(len(fuzz)):
                                bypassatt = "https://" + dorks[i] + target + fuzz[i]
                                ss = requests.get(bypassatt, proxies=proxies[rp], headers=headers[rh])
                                reqcount += 1
                                if ss.status_code in [202,200,302]:
                                    with lock:
                                        vulnerable.append("https://" + dorks[i] + target + fuzz[i])
                        except requests.exceptions.RequestException as e:
                            print(f"403 fuzz Request failed: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed for {URL}: {e}")
                if reqcount >= 60:
                    reqcount = 0
                    rp = random.randint(0, len(proxies)-1)
                    rh = random.randint(0, len(headers)-1)


    for i in range(threadcount):
        thread = threading.Thread(target=task, args=(target,))
        thread.start()
        with lock:
            threadsmain.append(thread)

    for thread in threadsmain:
        thread.join()

 

    print(vulnerable)

def bypass():
    target = input("ENTER 403 DOMAIN")
    threadcount = multiprocessing.cpu_count()
    def task2(target):
        reqcount = 0
        rp = random.randint(0, len(proxies)-1)
        rh = random.randint(0, len(headers)-1)
        for i in range(len(fuzz)):
            if fuzz[i] not in fuzztried:
                with lock:
                    fuzztried.add(fuzz[i])
                    fuzzatt = "https://" + target + fuzz[i]
                try:
                    ff = requests.get(fuzzatt, proxies=proxies[rp], headers=headers[rh])
                    reqcount +=1 
                    if ff.status_code in [202,200,302]:
                        with lock:
                            vulnerable.append("https://" + target + fuzz[i])
                except requests.exceptions.RequestException as e:
                    print(f"403 fuzz attempt failed: {e}")
                if reqcount >= 60:
                    reqcount = 0
                    rp = random.randint(0, len(proxies)-1)
                    rh = random.randint(0, len(headers)-1)
    for i in range(threadcount):
        thread = threading.Thread(target=task2, args=(target,))
        thread.start()
        with lock:
            threadsfuzz.append(thread)

    for thread in threadsfuzz:
        thread.join()
    

    print(vulnerable)

def helpmenu():
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("                                                                                                                                               By Michael Ajilore")
    ascii_art = figlet_format("CypherSweep", font="slant")
    print(colored(ascii_art, "yellow"))
    print("Press 1 to start Vulnerability search")
    print("press 2 to start 403 Bypass")
    print("Press 3 for Help menu ")
    print("Press any other number to go back to the  main menu")
    x = int(input("choose any number to return to main menu"))
    if x >= 0:
        mainmenu()

def mainmenu():
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("                                                                                                                                               By Michael Ajilore")
    ascii_art = figlet_format("CypherSweep", font="slant")
    print(colored(ascii_art, "yellow"))
    print("(1) Vulnerability search                                                                                        This war's a people's war against a system that's")
    print("(2) 403 Bypass                                                                                                  spiralled outta our control                      ")
    print("(3) Help menu")
    user = int(input())

    if user == 1:
        Vulnsearch()
    elif user == 2:
        bypass()
    elif user == 3:
        helpmenu()
    else:
        mainmenu()

mainmenu()
