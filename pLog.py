#!/usr/bin/env python
# coding: utf-8

import shelve, pyperclip

shell = shelve.open('words-p')

def save(a):
    shel = shelve.open('words-p')
    shel['pass'] = a
    shel.close()

print("Welcome to Password Manger\n\n".center(100))

try:
    a = shell['pass']
except:
    a = {}
    print("I guess you are new over here. So lets add a new Domain. ")

    domain = input("Enter the Domain Name: ")
    user_id = input("Enter the Email Address: ")
    pas = input("Enter the password: ")

    a[domain] = {user_id : pas}
    save(a)

while True:

    print("""
    1. To get password
    2. To Update Password
    3. To Insert New Password
             """)

    choice = input("Choice?? ")
    if choice == '1':
        print("Select your account")
        print('\t', ", ".join(list(a.keys())))

        acc = input('Domain Name?? ')

        if acc in a.keys():
            temp = list(a[acc].keys())
            for i in range(len(temp)):
                print(f"{i+1}. {temp[i]}")
            
            try:
                eAdd = int(input("Select??.. "))
            except:
                exit()
                
            x = temp[eAdd-1]
            
            if x in temp:
                pyperclip.copy(a[acc][x])
                print('Your Password has been copied.')
        else:
            pass
        
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
                pas = input("Enter the new password (q/b --> Go Back) : ")
                if pas in ['q','']:
                    continue
                else:
                    print(a[acc][x])
                    a[acc][x] = pas
                    print(a[acc][x])
                    print('Your Password has been reset.')
                    save(a)
        else:
            pass
        
    elif choice == '3':
        anoCe = input("Do you want to Add a Domain(ad) or add into existing domain(ed): ")
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


