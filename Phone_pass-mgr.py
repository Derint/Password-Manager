#!/usr/bin/env python
# coding: utf-8


from androidhelper import Android
from time import sleep, time
from os import system, name, get_terminal_size, mkdir, path
from sql_cmds import *

def clearConsole():
    system( 'cls' if name in ('nt', 'dos') else  'clear')


def heading_1(text):
    print(f"\n\n{text.center(w)}"+'\n\n')
    
def heading_2(text):
    print(f"\n{text.center(w-int(w*0.5))}")

def getKeys(shell):
    return [i for i in (list(shell.keys()))]
   

def printDetails(shell, shownum=False):
    s, t, width, space = 0, 8, w, ' '
    n = len(getKeys(shell))
    print('\n',space*t, end='')
    for idx, key in enumerate(getKeys(shell)):
        s += len(key) + 5
        if s>width:
            s=0
            print(f'\n{space*(t+1)}', end='')
        el = ', ' if idx+1 != n else ''
        print(f"{str(idx+1)+'. ' if shownum else ''}{key}", end=el)
    print()
  

def copy_to_clipboard(text):
    droid.setClipboard(text)

def make_toast(text, n=1):
    for _ in range(n):
        droid.makeToast(text)

def get_input(text, nl=False, el=False):
    t, t2 = "\n" if nl else "",  "\n" if el else ""
    return input( f"{t}  [>]   {text} :  {t2}")
    
def prt_to_scn(text, sym, end='\n'):
    print(f"  [{sym}]   {text}", end=end)

def getTime():
    return round(time())

droid = Android()

path_ = '.pwd'
if not path.isdir(path_):
    mkdir(path_)

slash = '\\' if name in ['nt', 'dos'] else '/'
w = get_terminal_size()[0]

fileName = path_+slash+'pwds.db'


shell = readDB(fileName)

if not path.isfile(fileName) or len(shell)==0 :
    clearConsole()
    heading_1("Initial Setup")

    accnt  = get_input("Account")
    uname = get_input("Username")
    passwd = get_input("Password")

    createDB(fileName)
    insertRecord(fileName, getTime(), accnt, uname, passwd)



while True:
    clearConsole()
    print("""
    	
                            Password Manager
    	                          
    
        1. Get Passwd
        2. Update Passwd
        3. Insert New Acct/Uname
        4. Delete Acct/Uname
            """)

    try:
        choice = get_input("Select ?? ").lower()
    except:
        clearConsole();
        exit();
    
    if choice in ['q', 'b', '', 'exit', 'q()']:
        prt_to_scn("Exiting.........   ", "~")
        sleep(1)
        break

    clearConsole()
    
    if choice == '1':    
        heading_1("Get Password")
        heading_2("Choose your Account ")
        
        printDetails(shell)
        accdet = getKeys(shell)
        account = get_input("Account Name ", nl=True)

        if account in accdet:
            unames = getKeys(shell[account])
          
            if len(unames)==1: uchoice= 0
                
            else:
                printDetails(shell[account], True)
                try: 
                    uchoice = int(get_input("Select ", nl=True)) -1
                    if not (-1 < uchoice < len(unames)):
                        print("  [!]  Invalid Input")
                       
                except: 
                    prt_to_scn("Invalid Input", "!"); continue
                   
            copy_to_clipboard(shell[account][unames[uchoice]])
            make_toast(f"Passwd Copied for {unames[uchoice]}")
                  
    elif choice == '2':
        heading_1("Updating Password")
        heading_2("Choose your Account")
        
        printDetails(shell)
        accdet = getKeys(shell)
        account = get_input("Account Name: ", nl=True)

        if account in accdet:
            unames = getKeys(shell[account])
            try:

                if len(unames)==1:
                    uchoice= 0
                    prt_to_scn(f"Changing Passwd for {unames[uchoice]}", "~")
                    
                else:
                    printDetails(shell[account], True)

                    uchoice = int(get_input("Select Acct", nl=True)) -1
                    if not (-1 < uchoice < len(unames)):continue

                prt_to_scn("Enter Your New Passwd : ", ">", end="")
                passwd = input()
                if passwd:
                    updatePasswd(fileName, getTime(), account, unames[uchoice],  passwd)
                    shell = readDB(fileName)

                    msg = "Password Changed Successfully"
                    
                else:
                    msg = "Password Cannot be Blank"
                make_toast(msg)

            except:
                make_toast("Something went wrong", "+");sleep(0.5)

    elif choice == '3':
        heading_1("New Account/Username")
        prt_to_scn("Add New <Account(na) | Username(nu)>", '~')
        uchoice2 = input("  [>]   ")

        if uchoice2 == 'na':
            account =  get_input("Account Name ", nl=True)
            if not account: prt_to_scn("Empty Input", "!"); continue;
            
            if account not in getKeys(shell):
                username = get_input("Username")
                passwd = get_input("Passwd")
                
                if not (username or passwd) : prt_to_scn("Empty Input", "!"); continue;
                insertRecord(fileName, getTime(), account, username, passwd)
                make_toast("Account added successfully")
            else:
                make_toast(f'Account: {account} is already created'); sleep(1)
                
        elif uchoice2 == 'nu':
            heading_2("Choose your Account")
            printDetails(shell)
            accdet = getKeys(shell)
            account = get_input("Enter Account Name ", nl=True)

            if account in accdet:
                username = get_input("New User-name: ")

                if username not in shell[account].keys():
                    passwd = get_input("Passwd for Username: ")
                    if not (username or passwd) : prt_to_scn("Empty Input", "!"); continue;
                    insertRecord(fileName, getTime(), account, username, passwd)
                    msg = "User added successfully"
                else:
                    msg = "User-name Already Exists"

                make_toast(msg)

        if uchoice2 in ['na', 'nu']: 
            shell = readDB(fileName)


    elif choice == '4':
        heading_1("Delete Account/Username")
       
        uchoice3 = get_input('Delete Account(a) or Username(u) ', nl=True).lower()

        if uchoice3 in ['a', 'u']:
            heading_2("Choose your Account")
            printDetails(shell)
            accdet = getKeys(shell)
            account = get_input("Enter Account Name: ", nl=True)

        if uchoice3 == 'a':
            if account in accdet:
                deleteAccount(fileName, account)
                make_toast(f'Account : {account} deleted')
                

        elif uchoice3 == 'u':

            if account in accdet:
                unames = getKeys(shell[account])
                if len(unames)==1:  uchoice= 0
                else:
                    printDetails(shell[account], True)
                    uchoice = int(get_input("Select ", nl=True)) -1
                    if not(-1 < uchoice < len(unames)):continue

                deleteUsername(fileName, account, unames[uchoice])
                make_toast(f'Username {unames[uchoice]} Deleted')

        
        if uchoice3 in ['a', 'u'] and account in accdet:
            shell = readDB(fileName)
        
            # If there are no keys
            if len(shell[account]) == 0 and uchoice3 =='u':
                make_toast(f'Account: {account} has no username, deleting it')
                deleteAccount(fileName, account)
                make_toast(f'Account : {account} deleted')
                sleep(2)

    
    if choice in [str(i) for i in range (1, 5)]:
        sleep(1)
    else:
        prt_to_scn("invalid Input  ", "!")

    shell = readDB(fileName)
    if len(shell)==0:break
    
clearConsole()
        



