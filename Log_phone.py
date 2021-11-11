#!/usr/bin/env python
# coding: utf-8

# In[6]:


import shelve, androidhelper


# In[7]:


def save(shell,fname):
    shel = shelve.open(fname)
    shel['pass'] = shell
    shel.close()
    
    newS = shelve.open(fname)
    return newS['pass']

def getKeys(shell):
    return [i for i in (list(shell.keys()))]

def getInfo():
    account = input("Enter Acct Name: ")
    username = input("Enter Uname: ")
    passwd = input("Enter Passwd: ")
    
    return account, username, passwd

def printDetails(shell, prt=False, shownum=False):
    temp = getKeys(shell)
    if prt:
        if shownum: print("\n".join([f'\t{i+1}. {temp[i]}' for i in range(len(temp))]))  
        else: print('\t' + ", ".join(temp))


# In[8]:


fileName = 'words-p1'
droid = androidhelper.Android()
try:
    shell = shelve.open(fileName)['pass']
except:
    print("Initial Setup".center(50))
    d = getInfo()
    temp = {d[0]: {d[1]:d[2]}}
    shell = save(temp, fileName)


# In[9]:


if len(shell)==0:
    print("")
    d = getInfo()
    temp = {d[0]: {d[1]:d[2]}}
    shell = save(temp, fileName)


# In[10]:


while True:
    print("""
    1. Get Passwd
    2. Update Passwd
    3. Insert New Acct/Uname
    4. Delete Acct/Uname
            """)

    choice = input("Select?? ")

    if choice == '1':
        print("Get Password\n".center(40))
        print("Choose your Account")
        printDetails(shell, True)
        accdet = getKeys(shell)
        account = input("Enter Account Name: ")

        if account in accdet:
            unames = getKeys(shell[account])

            if len(unames)==1:
                t = "".join(shell[account].keys())
                droid.setClipboard(shell[account][unames[0]])
                print(f"\nPasswd Copied!({t})")

            else:
                printDetails(shell[account], True, True)
                try: 
                    uchoice = int(input("\t Select: ")) - 1
                    if -1 < uchoice < len(unames):
                        droid.setClipboard(shell[account][unames[uchoice]])
                        print(f"\nPasswd Copied!")

                except: exit()

    elif choice == '2':
        print("Updating Password\n".center(30))
        print("\nChoose your Account")
        printDetails(shell, True)
        accdet = getKeys(shell)
        account = input("Enter Account Name: ")

        if account in accdet:
            unames = getKeys(shell[account])
            printDetails(shell[account], True, True)

            try: 
                uchoice = int(input("   Select: ")) - 1
                if -1 < uchoice < len(unames):
                    passwd = input("Enter Your New Passwd: ")
                    shell[account][unames[uchoice]] = passwd
                    shell = save(shell, fileName)

            except: exit()

    elif choice == '3':
        print("Adding New Account/Username\n".center(30))

        uchoice2 = input('Add New Account(na) or New Username(nu): ')

        if uchoice2 == 'na':
            account = input("Enter Account Name: ")
            
            if account not in getKeys(shell):
                username = input("Enter Username: ")
                passwd = input("Enter Passwd: ")
                shell[account] = {username:passwd}
            else:
                print(f'Account: {account} is already created')
                
        elif uchoice2 == 'nu':
            print("Choose your Account")
            printDetails(shell, True)
            accdet = getKeys(shell)
            account = input("Enter Account Name: ")

            if account in accdet:
                username = input("Enter Username: ")
                passwd = input("Enter Passwd: ")
                shell[account][username] = passwd

        if uchoice2 in ['na', 'nu']: shell = save(shell, fileName)


    elif choice == '4':
        print('Deleting Account/Username\n'.center(30))
        uchoice3 = input('Delete Account(a) or Username(u): ')

        if uchoice3 == 'a':
            print("Choose your Account")
            printDetails(shell, True)
            accdet = getKeys(shell)
            account = input("Enter Account Name: ")

            if account in accdet:
                del shell[account]
                print(f'Account : {account} was deleted')
                shell = save(shell, fileName)

        elif uchoice3 == 'u':
            print("Choose your Account")
            printDetails(shell, True)
            accdet = getKeys(shell)
            account = input("Enter Account Name: ")

            if account in accdet:
                unames = getKeys(shell[account])
                printDetails(shell[account], True, True)
                try: 
                    uchoice = int(input("\t Select: ")) - 1
                    if -1 < uchoice < len(unames):
                        del shell[account][unames[uchoice]]
                        shell = save(shell, fileName)
                        print(f'\nUsername {unames[uchoice]} in Account({account}) was Deleted.')
                        
                        if len(shell[account]) == 0:
                            print(f'Account: {account} has no username, so deleting it now.')
                            del shell[account]
                            print(f'Account : {account} was deleted')
                            shell = save(shell, fileName)
                        
                except: exit()
            
    elif choice in ['q', 'b', '']:
        print("\n\n\tExiting.........")
        break
    
    if len(shell)==0:break
        
    print('----'*10)


# In[ ]:


len(shell)


# In[ ]:




