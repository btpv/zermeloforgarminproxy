version = "V14.9.22.20.03"
updating = False

import json
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask ,request
def update():
    global updating
    if updating:
        return
    rq = requests.get("https://raw.githubusercontent.com/btpv/zermeloforgarminproxy/master/files/run.py")
    newest = rq.text.split("\n")[0].replace("version = ","").replace("\"","")
    print(f"old{version} - new{newest}")
    if version != newest:
        print("updating")
        updating = True
        with open(__file__,"w") as f:
            f.write(rq.text)
        app.do_teardown_appcontext()
    else:
        print("uptodate")
    

sched = BackgroundScheduler(daemon=True)
sched.add_job(update,'interval',minutes=0.1)
sched.start()
app = Flask(__name__)
@app.teardown_request
def teardown(exception):
    os._exit(0)
@app.after_request
def treat_as_plain_text(response):
    # print(response.url)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

@app.route("/",methods=['POST'])
def main():
    data = json.loads(request.get_data())
    try:
        rq = requests.post(f"https://{data['domain']}.zportal.nl/api/v3/oauth", data={'username': data['username'], 'password': data['password'], 'client_id': 'OAuthPage', 'redirect_uri': '/main/',
            'scope': '', 'state': '4E252A', 'response_type': 'code', 'tenant': data['domain']})
        token = rq.text[rq.text.find("code=")+5:rq.text.find("&",rq.text.find("code=")+5)]
        return {"token":token}
    except:
        return {"error":"missing info"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000,debug=False)
