import requests
import threading
import random

dorks = []
proxies = []
fuzz = []
headers = [{}]
tried = set()
target = input("ENTER A DOMAIN")
vulnerable = [1,2,3]
lock = threading.Lock()


def task():
    reqcount = 0
    rp = random.randint(0, len(proxies)-1)
    rh = random.randint(0, len(headers)-1)
    try:
        for i in range(len(dorks)):
            if dorks[i] not in tried:

                tried.add(dorks[i])
                URL = "https://" + dorks[i] + target
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

                if reqcount >= 60:
                    reqcount = 0
                    rp = random.randint(0, len(proxies)-1)
                    rh = random.randint(0, len(headers)-1)

    except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


thread1 = threading.Thread(target=task)
thread2 = threading.Thread(target=task)
thread3 = threading.Thread(target=task)
thread4 = threading.Thread(target=task)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

print(vulnerable)

