#!/usr/bin/env python
# coding: utf-8

import shelve, pyperclip
import androidhelper 

droid = androidhelper.Android () 

shell = shelve.open('words-p')

def save(a):
    shell = shelve.open('words-p')
    shell['pass'] = a
    shell.close()

print("\n\n\t\tWelcome to Password Manger\n\n")

try:
    a = shell['pass']
except:
    a = {}
    shell['pass'] = a
    shell.close()
    print("I guess you are new over here. So lets add a new Domain. ")

    domain = input("Enter the Domain Name ")
    user_id = input("Enter the Email Address: :\n")
    pas = input("Enter the password: :\n")

    a[domain] = {user_id : pas}
    save(a)
    print ('Your Data has been saved') 

shell.close()

while True:

    print("""
    1. To get password
    2. To Update Password
    3. To Insert New Password
             """)

    choice = input("Choice??   ")
    if choice == '1':
        d = list(a.keys())

        if len(d) > 1:
            print("Select your account")
            print('\t', ", ".join(d))

            acc = input('Domain Name?? ')

            if acc in a.keys():
                temp = list(a[acc].keys())

                if len(temp) > 1:
                    for i in range(len(temp)):
                        print(f"{i+1}. {temp[i]}")
                    
                    try:
                        eAdd = int(input("Select??.. "))
                    except:
                        exit()
                        
                    x = temp[eAdd-1]
                    
                    if x in temp:
                        droid.setClipboard(a[acc][x])
                        print('Your password has been copied') 
                else:
                    droid.setClipboard(list(a[acc].values())[0])
                    print('Your Password has been copied.')

            else:
                print('No such domain exist !!!')
        else:
            droid.setClipboard(list(list(a.values())[0].values())[0])
            print(f'Your password for {temp} with user_id has been copied')
            
    elif choice == '2':
        print("Select your account")
        print('\t', ", ".join(list(a.keys())))

        acc = input('Domain Name?? ')
        
        if acc in a.keys():
            for i in range(len(list(a[acc].keys()))):
                print(f"{i+1}. {list(a[acc].keys())[i]}")
            
            try:
                eAdd = int(input("Select??.. "))
            except:
                exit()
                
            x = list(a[acc].keys())[eAdd-1]
            
            if x in a[acc].keys():
                pas = input("Enter the new password (q/b --> Go Back) : \n")
                if pas in ['q','']:
                    continue
                else:
                    print(a[acc][x])
                    a[acc][x] = pas
                    print('Your Password has been reset.')
                    save(a)
        else:
            pass
        
    elif choice == '3':
        anoCe = input("Do you want to Add a Domain(ad) or \nadd into existing domain(ed): ")
        o = ['q','','b']

        if anoCe == 'ad':
            print("To Go back enter (q/b,uk)")
            domain = input("Enter the Domain Name: ")
            user_id = input("Enter the Email Address: ")
            pas = input("Enter the password: ")
            
            if domain in o or user_id in o or pas in o:
                continue

            a[domain] = {user_id : pas}
            save(a)
            
        elif anoCe == 'ed':
            print("Select your account")
            print('\t', ", ".join(list(a.keys())))

            acc = input('Domain Name?? ')

            if acc in a.keys():
                user_id = input('Enter the User Id: ')
                pas = input("Enter the password: ")

                if pas in o or user_id in o:
                    continue

                a[acc][user_id] = pas
                save(a)
                
    elif choice in ['q','e','']:
        exit()
        
    print('\n')

