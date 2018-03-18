import requests
url = 'http://makeohio2018.kevinbartchlett.com/collectData.php'
payload = {'key1': 'boobs','key2': 'whitsSmallDick'}
r = requests.post(url,data=payload)
r.text
r.status_code
