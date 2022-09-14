import requests
req = requests.get("http://localhost:5000/",allow_redirects=False)
if req.status_code < 300 and req.status_code > 199:
    exit(0)
else:
    exit(-1)
    