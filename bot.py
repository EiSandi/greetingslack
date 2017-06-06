import websocket
import json
import requests
import urllib
import os
 

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
        MESSAGE ="Hi, I'm Office Uncle and I am here to help you understand what insurance you have, your coverage and to answer FAQs.I respond to keywords (for example MRI, physiotherapy, reimbursement), however to get you started -here's some suggested keywords for you to try:\nGP; Specialist; Surgery; Pregnancy; Dentist"
        TOKEN = "xoxb-192115241664-GwLVUSLTCWStYLg3X7aOtCmo"
        UNFURL = os.environ['UNFURL-LINKS']
except:
        MESSAGE = "Hi, I'm Office Uncle and I am here to help you understand what insurance you have, your coverage and to answer FAQs.I respond to keywords (for example MRI, physiotherapy, reimbursement), however to get you started -here's some suggested keywords for you to try:\nGP; Specialist; Surgery; Pregnancy;Dentist"
        TOKEN ="xoxb-192115241664-GwLVUSLTCWStYLg3X7aOtCmo"
        UNFURL = 'FALSE'
###############################################################

def parse_join(message):
    m = json.loads(message)
    if (m['type'] == "team_join"):
        x = requests.get("https://slack.com/api/im.open?token="+TOKEN+"&user="+m["user"]["id"])
        x = x.json()

        result=requests.get("https://slack.com/api/users.profile.get?token="+TOKEN)
        result=result.json()
        # print result["profile"]["email"]
        print result

        x = x["channel"]["id"]
        if (UNFURL.lower() == "false"):
          xx = requests.post("https://slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+x+"&text="+urllib.quote(MESSAGE)+"&parse=full&as_user=true&unfurl_links=false")
        else:
          xx = requests.post("https://slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+x+"&text="+urllib.quote(MESSAGE)+"&parse=full&as_user=true")
        #DEBUG
        #print '\033[91m' + "HELLO SENT" + m["user"]["id"] + '\033[0m'
        #

#Connects to Slacks and initiates socket handshake
def start_rtm():
    r = requests.get("https://slack.com/api/rtm.start?token="+TOKEN, verify=False)
    r = r.json()
    r = r["url"]
    return r

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    print "SOME ERROR HAS HAPPENED", error

def on_close(ws):
    print '\033[91m'+"Connection Closed"+'\033[0m'

def on_open(ws):
    print "Connection Started - Auto Greeting new joiners to the network"


if __name__ == "__main__":
    r = start_rtm()
    ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
    #ws.on_open
    ws.run_forever()

