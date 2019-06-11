import threading
import requests
import json


def iplookup(proxy):
	try:
		ip = requests.get('https://www.wepayapi.com/v2/credit_card/create', proxies={"https": proxy}, timeout=1)
		print("HTTPS LIVE  =>  " + proxy + "\t[LIVE ON GATEWAY]")
		with open('https_live.txt', 'a+') as lives:
			lives.write(proxy + '\n')
			lives.close()
	except:
		print("DEAD PROXY  =>  " + proxy)

with open("HTTP1.txt", "r") as plist:
	proxies = plist.read()

	threads = []

	for proxy in proxies.split('\n'):
		t = threading.Thread(target=iplookup, args=(proxy,))
		threads.append(t)

	for x in threads:
		x.start()
		x.join()

	# for x in threads:
	# 	x.join()
