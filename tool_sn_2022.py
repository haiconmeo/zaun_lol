import requests
import requests, os, re, subprocess, ctypes, sys, traceback
from random import shuffle
 
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin
import json
def getToken():
    #League Client command line query
    command = "WMIC PROCESS WHERE name='LeagueClient.exe' GET commandline"
    #Get WMIC output
    output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.read().decode('utf-8')
    #Parse landing token
    return re.findall(r'--landing-token=(.*?)\s\-?\-?', output)[0]
def run_scrip(invitation_code,accountToken):
    url = "https://findmymap.lol.garena.vn/api/bind"

    payload = json.dumps({
    "invitation_code": invitation_code,
    "confirm": True
    })

    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'content-length': '52',
    'content-type': 'application/json',
    'origin': 'https://findmymap.lol.garena.vn',
    'referer': f'https://findmymap.lol.garena.vn/?token={accountToken}',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'token': accountToken,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


if __name__ == '__main__':
    print("LOL code tool hp 2022 - Hai Con Meo.")
    if not isAdmin():
        print('Please run as admin!')
        sys.exit(0)
    codes = open('haiconmeo.txt', encoding='utf-8').readlines()
    shuffle(codes)

    token = getToken()
    print('Your token: ', token)
    for code in codes:
        try:
            print(code)
            
            res = run_scrip(code.strip(), token)
            print(res)
            if   'error' in res and res['error'] =="ERROR__INVITEE_LIMIT" :
                print('INVITEE_LIMIT')
                break


        except Exception as e:
            print(traceback.format_exc())
