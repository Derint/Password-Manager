#!/usr/bin/env python

from requests import get
from sql_cmds import timeDB, updatePasswd, openDB
from os import remove, get_terminal_size, path
from time import sleep


def savefile(url):
    req = connect(url)
    file = path.basename(url.replace('%2F', '/'))
    with open(".pwd/tmp"+file, 'wb') as f:
        for chunk in req.iter_content(chunk_size=250):
            f.write(chunk)
            
def getRecords(dwndata, account):
    params = []
    for usr, (t, psk) in dwndata[account].items():
        params.append((t, account, usr, psk))
    return params

def insertRecords(tableName, params):
    ins_query = "INSERT INTO Pwords values (?, ?, ?, ?)"
    openDB(tableName, query=ins_query, values=params, commit=True, exeMany=True)

def backspace():
    print(f"\r {' '*get_terminal_size()[0]}", end='')
    
def printmsg(text, sym):
    backspace()
    print(f"\r  [{sym}]  {text}", end="")
    
def connect(url, n=1):
    print("\r  *Requesting Content....", end='')
    while True:
        try:  
            req = get(url)
            return req
        except:
            print(f"\r  !!! Start the server to update passwords {'.'*n}", end='')
            n+=1; sleep(0.4)
            if n%7==0:
                n = 1
                backspace()
            if n>25:
                print("\n  [!]  Connection Time-out, pls check your server/computer Ntw....")
                exit()
        

url = '' #Server URL for .db file
FILENAME = '.pwd/pwds.db'
savefile(url)

printmsg("Updating Passwords...", "*")
thisdata, dwndata = timeDB('.pwd/pwds.db'), timeDB('.pwd/tmppwds.db')

thisKey, dwndKey = thisdata.keys(), dwndata.keys()
uniqKeys = set(thisKey).union(dwndKey)
count = {'account':0, 'update_psk':0, 'usrname':0}

for account in uniqKeys:
    addUsrList = []

    if account in thisKey and account in dwndKey:
        for username in dwndata[account]:
            time2_, psk2 = dwndata[account][username]
            
            if username in thisdata[account]: # check if paswd change is req.
                time1_, psk1 = thisdata[account][username]
                if time1_ < time2_:
                    updatePasswd(FILENAME, time2_, account, username, psk2)
                    count['update_psk'] += 1
        
            else: # i.e if username not in current db
                count['usrname'] += 1
                addUsrList.append((time2_, account, username, psk2))

    elif account in dwndKey: # Add this new account in current database
        records = getRecords(dwndata, account)
        insertRecords(FILENAME, records)
        count['account'] += 1

    if addUsrList:
        insertRecords(FILENAME, addUsrList)

remove('.pwd/tmppwds.db')
is_updated = sum([count[x] for x in count])

if count['update_psk']:
    printmsg(f"Updated {count['update_psk']} Password(s)\n", '+')

if count['account']:
    printmsg(f"Added {count['account']} Account(s) \n", '+')

if count['usrname']:
    printmsg(f"Added {count['usrname']} username(s) \n", '+')
    
msg = "Passwords Updated Successfully" if is_updated else "All Passwords are already up-to-date."

print(f"\r  [+]  {msg}....")