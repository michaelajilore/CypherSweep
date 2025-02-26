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
flagwords = {"Exposed directory" :"Index of /", "Exposed directory" : "Directory listing for", "Exposed directory" :"Parent Directory", "Exposed directory" :".htaccess",
            "Exposed directory" : "server-status", "(Linux password file)" : "root:x:0:0:", " (Windows boot file)" : "boot.ini" ,
            "(Environment configuration file)" : ".env", "(Possible DB credentials)": "config.php", "(Exposed version control meta data)" : ".git",
            "(Java app server config)" : "WEB-INF/web.xml", "(ASP.NET configuration)" : "appsettings.json", "(Django settings file)" : "local_settings.py",
            "(Exposed admin endpoint)" : "/admin", "(Exposed admin endpoint)" : "/phpmyadmin", "(Exposed admin endpoint)" : "/wp-admin", "(Exposed debug endpoint)" : "/debug",
            "(Exposed debug endpoint)" : "/dev", "(Exposed debug endpoint)" : "/config", "(Exposed debug endpoint)" : "/logs"}
fuzztried = set()
lock = threading.Lock()



def flagcatch(r,b):
    for key, value in flagwords.items():  
        if value.encode() in r.content:  
            with lock:
                b[key] = r.url + " | " + value
                

def Vulnsearch():
    flagscaught = {}
    target = input("ENTER A DOMAIN: ")
    inputval = "https://" + target
    try:
        iv = requests.get(inputval, proxies=proxies[0])
    except requests.exceptions.RequestException as e:
        print(f"could not resolve domain try again")
        Vulnsearch()
    threadcount = multiprocessing.cpu_count()
    def task(target,flagscaught):
        reqcount = 0
        rm = random.randint(50,70)
        rp = random.randint(0, len(proxies)-1)
        rh = random.randint(0, len(headers)-1)
        for i in range(len(dorks)):
            if dorks[i] not in tried:
                with lock:
                    tried.add(dorks[i])
                    
                URL = "https://" + dorks[i][0] + target + dorks[i][1]
                try:            
                    s = requests.get(URL, proxies=proxies[rp], headers=headers[rh])
                    reqcount += 1
                    if s.status_code in [202,200,302]:
                        with lock:
                                vulnerable.append("https://" + dorks[i][0] + target + dorks[i][1])
                        flagcatch(s,flagscaught)
                    elif s.status_code == 403:
                        try:
                            for i in range(len(fuzz)):
                                bypassatt = "https://" + dorks[i][0] + target + dorks[i][1] + fuzz[i]
                                ss = requests.get(bypassatt, proxies=proxies[rp], headers=headers[rh])
                                reqcount += 1
                                if ss.status_code in [202,200,302]:
                                    with lock:
                                        vulnerable.append("https://" + dorks[i][0] + target + dorks[i][1] + fuzz[i])
                                    flagcatch(ss,flagscaught)
                        except requests.exceptions.RequestException as e:
                            print(f"403 fuzz Request failed: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed for {URL}: {e}")
                if reqcount >= rm:
                    reqcount = 0
                    rp = random.randint(0, len(proxies)-1)
                    rh = random.randint(0, len(headers)-1)
                    rm = random.randint(50,70)


    for i in range(threadcount):
        thread = threading.Thread(target=task, args=(target,flagscaught))
        thread.start()
        with lock:
            threadsmain.append(thread)

    for thread in threadsmain:
        thread.join()

 

    print(f"Vulnerable URL's: {vulnerable}")
    print(f"Other flagged Vulns: {flagscaught}")




def bypass():
    flagscaught = {}
    target = input("ENTER 403 DOMAIN: ")
    inputval = "https://" + target
    try:
        iv = requests.get(inputval, proxies=proxies[0])
    except requests.exceptions.RequestException as e:
        print(f"could not resolve domain try again")
        bypass()
    
    threadcount = multiprocessing.cpu_count()
    def task2(target,flagscaught):
        reqcount = 0
        rp = random.randint(0, len(proxies)-1)
        rh = random.randint(0, len(headers)-1)
        rm = random.randint(50, 70)
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
                        flagcatch(ff,flagscaught)
                except requests.exceptions.RequestException as e:
                    print(f"403 fuzz attempt failed: {e}")
                if reqcount >= rm:
                    reqcount = 0
                    rp = random.randint(0, len(proxies)-1)
                    rh = random.randint(0, len(headers)-1)
                    rm = random.randint(50, 70)
    for i in range(threadcount):
        thread = threading.Thread(target=task2, args=(target,flagscaught))
        thread.start()
        with lock:
            threadsfuzz.append(thread)

    for thread in threadsfuzz:
        thread.join()
    

    print(f"Vulnerable URL's: {vulnerable}")
    print(f"Other flagged Vulns: {flagscaught}")


def responseanalyze():
    flagscaught = {}
    target = input("ENTER 403 DOMAIN: ")
    inputval = "https://" + target
    try:
        iv = requests.get(inputval, proxies=proxies[0])
    except requests.exceptions.RequestException as e:
        print(f"could not resolve domain try again")
        responseanalyze()
    for key, value in flagwords.items():  
        if value.encode() in iv.content:  
                flagscaught[key] = iv.url + " | " + value

    print(f"Flagged vulnerabilities: {flagscaught}")

def helpmenu():
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("                                                                                                                                               By Michael Ajilore")
    ascii_art = figlet_format("CypherSweep", font="slant")
    print(colored(ascii_art, "yellow"))
    print("Option 1 to start Vulnerability search")
    print("Option 2 to start 403 Bypass")
    print("Option 3 to analyze HTTP response")
    print("Option 4 for help menu")
    print(" ")
    x = int(input("choose any number to return to main menu: "))
    if x >= 0:
        mainmenu()

def mainmenu():
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("                                                                                                                                               By Michael Ajilore")
    ascii_art = figlet_format("CypherSweep", font="slant")
    print(colored(ascii_art, "yellow"))
    print("(1) Vulnerability search                                                                                        This war's a people's war against a system that's")
    print("(2) 403 Bypass                                                                                                  spiralled outta our control                      ")
    print("(3) Scan HTTP response")
    print("(4) Help menu")
    user = int(input())

    if user == 1:
        Vulnsearch()
    elif user == 2:
        bypass()
    elif user == 3:
        responseanalyze()
    elif user == 4:
        helpmenu()
    else:
        mainmenu()

mainmenu()
