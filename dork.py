import requests
import threading
import random

dorks = []
proxies = []
fuzz = []
headers = [{}]
tried = set()
vulnerable = []
fuzzvuln = []
fuzztried = set()
lock = threading.Lock()

print("(1) Vulnerability search")
print("(2) 403 Bypass")
print(" ")

user = int(input())


def Vulnsearch():
    target = input("ENTER A DOMAIN")
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




    thread1 = threading.Thread(target=task, args=(target))
    thread2 = threading.Thread(target=task, args=(target))
    thread3 = threading.Thread(target=task, args=(target))
    thread4 = threading.Thread(target=task, args=(target))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    print(vulnerable)

def bypass():
    target = input("ENTER 403 DOMAIN")
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

    thread1 = threading.Thread(target=task2, args=(target))
    thread2 = threading.Thread(target=task2, args=(target))
    thread3 = threading.Thread(target=task2, args=(target))
    thread4 = threading.Thread(target=task2, args=(target))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    print(vulnerable)


if user == 1:
    Vulnsearch()
elif user == 2:
    bypass()
