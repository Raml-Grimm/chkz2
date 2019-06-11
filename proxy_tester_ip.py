import requests
import threading
import json


def main(proxy):
    try:
        req = requests.get('https://api.ipify.org?format=json', proxies={"https": proxy}, timeout=4)
        d = json.loads(req.text)
        print("[LIVE PROXY] IP  =>  " + d['ip'])
    except:
        print("[DEAD] PROXY => " + proxy)

with open("https_live.txt", "r") as plist:
	proxies = plist.read()

	threads = []

	for proxy in proxies.split('\n'):
		t = threading.Thread(target=main, args=(proxy,))
		threads.append(t)

	for x in threads:
		x.start()
		x.join()