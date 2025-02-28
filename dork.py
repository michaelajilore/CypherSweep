import requests
import threading
import random
import multiprocessing
import re
import time
from pyfiglet import figlet_format
from termcolor import colored


dorks = [] # will be filled with dorks stored as tuples with the prefix first then the postfix being second in the pair dorks that dont have a post fix will have " " as the second pair 
proxies = [] # will be filled with proxies 
fuzz = ["/admin/?","//admin//","///admin///","/./admin/./","/admin?","/admin??","/admin/?/","/admin/??","/admin/??/","/admin/..","/admin/../",
        "/admin/./","/admin/.","/admin/.//","/admin/*","/admin//*","/admin/%2f","/admin/%2f/","/admin/%20","/admin/%20/","/admin/%09","/admin/%09/",
        "/admin/%0a","/admin/%0a/","/admin/%0d","/admin/%0d/","/admin/%25","/admin/%25/","/admin/%23","/admin/%23","/admin/%26","/admin/%3f","/admin/%3f/",
        "/admin/%26/","/admin/#","/admin/#/","/admin/#/./","/./admin","/./admin/","/..;/admin","/..;/admin/","/.;/admin","/.;/admin/","/;/admin",
        "/;/admin/","//;//admin","//;//admin/","/admin/./","/%2e/admin","/%2e/admin/","/%20/admin/%20","/%20/admin/%20/","/admin/..;/","/admin.json",
        "/admin/.json","/admin..;/","/admin;/","/admin%00","/admin.css","/admin.html","/admin?id=1","/admin~","/admin/~","/admin/°/","/admin/&",
        "/admin/-","/admin\\/\\/","/admin/..%3B/","/admin/;%2f..%2f..%2f","/ADMIN","/ADMIN/","/admin/..\\;/","/*/admin","/*/admin/","/ADM+IN","/ADM+IN/"]
headers = [{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/110.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; U; Android 12; en-us; SM-A715F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:110.0) Gecko/20100101 Firefox/110.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:110.0) Gecko/20100101 Firefox/110.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G930F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/109.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; Nexus 5X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-J730F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.4 Mobile/15E148 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/109.0.0.0 Safari/537.36"}] #will be filled with user agents 
vulnerable = []
tried = set()
threadsmain = []
fuzzvuln = []
threadsfuzz = []
stop_event = threading.Event()
flagwords = {"(Exposed directory)" :"Index of /", "(Exposed directory)" : "Directory listing for", "(Exposed directory)" :"Parent Directory", "(Exposed directory)" :".htaccess",
            "(Exposed directory)" : "server-status", "(Linux password file)" : "root:x:0:0:", " (Windows boot file)" : "boot.ini" ,
            "(Environment configuration file)" : ".env", "(Possible DB credentials)": "config.php", "(Exposed version control meta data)" : ".git",
            "(Java app server config)" : "WEB-INF/web.xml", "(ASP.NET configuration)" : "appsettings.json", "(Django settings file)" : "local_settings.py",
            "(Exposed admin endpoint)" : "/admin", "(Exposed admin endpoint)" : "/phpmyadmin", "(Exposed admin endpoint)" : "/wp-admin", "(Exposed debug endpoint)" : "/debug",
            "(Exposed debug endpoint)" : "/dev", "(Exposed debug endpoint)" : "/config", "(Exposed debug endpoint)" : "/logs"}
fuzztried = set()
pattern = r"^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,10}$"
lock = threading.Lock()

def checkproxy(proxy):
     test = "https://www.google.com"
     check = requests.get(test, proxies=proxy)
     if check.status_code in [200,202,302]:
         return True
     
     return False

def displayprogress(tried, pool, threads_list):
    while any(thread.is_alive() for thread in threads_list):
        if len(pool) > 0:
            progress = (len(tried) / len(pool)) * 100
            print(f"Task progress {progress:.2f}% ")
        else:
            print("Waiting for tasks...")
        time.sleep(5)
    print("All threads completed!")

def flagcatch(r,b):
    for key, value in flagwords.items():  
        if value.encode() in r.content:  
            with lock:
                b[key] = r.url + " | " + value
                

def Vulnsearch():
    global threadsmain
    stop_event.clear() # Reset the flag at the start
    threadsmain = []
    tried = set()
    flagscaught = {}
    target = input("ENTER A DOMAIN: ")
    if bool(re.match(pattern, target)):
        inputval = "https://" + target
        proxy_index = random.randint(0, len(proxies)-1)

        try:
            requests.get(inputval, proxies=proxies[proxy_index])

        except requests.exceptions.RequestException as e:
            print(f"could not resolve domain try again")
            Vulnsearch()
        threadcount = multiprocessing.cpu_count()
    else:
        print("Invalid domain please try again")
        Vulnsearch()
    def task(target,flagscaught,tried):
        global stop_event
        reqcount = 0
        rm = random.randint(50,70)
        rp = random.randint(0, len(proxies)-1)
        rh = random.randint(0, len(headers)-1)
        for i in range(len(dorks)):
            if stop_event.is_set():
                return
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
                            for k in range(len(fuzz)):
                                if dorks[i][1] == " ":
                                    nopostfix = "https://" + dorks[i][0] + target + fuzz[k]
                                    np = requests.get(nopostfix, proxies=proxies[rp], headers=headers[rh])
                                    reqcount += 1
                                    if np.status_code in [202,200,302]:
                                        with lock:
                                            vulnerable.append("https://" + dorks[i][0] + target + fuzz[k])
                                        flagcatch(np,flagscaught)
                                else:
                                    bypassatt = "https://" + dorks[i][0] + target + dorks[i][1] + fuzz[k]
                                    ss = requests.get(bypassatt, proxies=proxies[rp], headers=headers[rh])
                                    reqcount += 1
                                    if ss.status_code in [202,200,302]:
                                        with lock:
                                            vulnerable.append("https://" + dorks[i][0] + target + dorks[i][1] + fuzz[k])
                                        flagcatch(ss,flagscaught)
                        except requests.exceptions.RequestException as e:
                            print(f"403 fuzz Request Connection error: {e}")
                            stop_event.set()
                            mainmenu()
                except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
                    print(f"Request failed or interrupted for {URL}: {e}")
                    stop_event.set()
                    mainmenu()
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

    progress_thread = threading.Thread(target=displayprogress, args=(tried, dorks, threadsmain))
    progress_thread.daemon = True
    progress_thread.start()

    for thread in threadsmain:
        thread.join()

 

    print(f"Vulnerable URL's: {vulnerable}")
    print(f"Other flagged Vulns: {flagscaught}")




def bypass():
    global threadsfuzz
    stop_event.clear()
    flagscaught = {}
    threadsfuzz = []
    fuzztried = []
    target = input("ENTER 403 DOMAIN: ")
    if bool(re.match(pattern, target)):
        inputval = "https://" + target
        try:
            iv = requests.get(inputval, proxies=proxies[0])
        except requests.exceptions.RequestException as e:
            print(f"could not resolve domain try again")
            bypass()
        
        threadcount = multiprocessing.cpu_count()
    else:
        print("Invalid domain please try again")
        bypass()
    def task2(target,flagscaught):
        global stop_event
        reqcount = 0
        rp = random.randint(0, len(proxies)-1)
        rh = random.randint(0, len(headers)-1)
        rm = random.randint(50, 70)
        for i in range(len(fuzz)):
            if stop_event.is_set():
                return
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
                except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
                    print(f"403 fuzz attempt failed: {e}")
                    stop_event.set()
                    mainmenu()
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

    progress_thread = threading.Thread(target=displayprogress, args=(fuzztried, fuzz, threadsfuzz))
    progress_thread.daemon = True
    progress_thread.start()

    for thread in threadsfuzz:
        thread.join()
    

    print(f"Vulnerable URL's: {vulnerable}")
    print(f"Other flagged Vulns: {flagscaught}")


def responseanalyze():
    flagscaught = {}
    target = input("ENTER DOMAIN: ")
    count = 0
    if bool(re.match(pattern, target)):
        inputval = "https://" + target
        try:
            iv = requests.get(inputval, proxies=proxies[0])
        except requests.exceptions.RequestException as e:
            print(f"could not resolve domain try again")
            responseanalyze()
    else:
        print("Invalid domain please try again")
        responseanalyze()
    try:
        for key, value in flagwords.items():
            count +=1  
            if value.encode() in iv.content:  
                    progress = (count // len(flagwords)) * 100
                    if count % 5 == 0:
                        print(f"Scan progress {progress}%")

                    flagscaught[key] = iv.url + " | " + value
    except(KeyboardInterrupt, requests.exceptions.RequestException):
        print("Keyboard interrupt returning to menu")
        mainmenu


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
    print("Use Crtl + C to back out of any scan")
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
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
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
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

for i in range(len(proxies)):
    if checkproxy(proxies[i]):
        continue
    else:
       proxies.pop(i)
    if len(proxies) == 0:
        print("WARNING proxy list needs attention before scanning")
mainmenu()