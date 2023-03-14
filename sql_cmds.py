import sqlite3
from collections import defaultdict


def openDB(tableName, query, values=(), commit=False, exeMany=False):
    conn = sqlite3.connect(tableName)
    c = conn.cursor()

    if values: 
        if exeMany:
            c.executemany(query, values)
        else:
            c.execute(query, values)

    else: 
        c.execute(query)

    if commit:
        conn.commit()
    else:
        a = c.fetchall()
        
    c.close()
    conn.close()
    
    if not commit:return a

def createDB(tableName):
    query = """
    CREATE TABLE IF NOT EXISTS Pwords (
        time      bigint,
        account   varchar2(50),
        username  varchar2(50),
        passwd    varchar2(50)
    )
    """
    openDB(tableName, query, commit=True)
    
    
def readDB(tableName):
    query = """
    SELECT account, username, passwd FROM Pwords
    """
    result = openDB(tableName, query)

    data = defaultdict(dict)
    for accnt, uname, pwd in result:
        data[accnt][uname] = pwd
    return data


def timeDB(tableName):
    #time, account, username
    query = """
    SELECT * FROM Pwords
    """
    result = openDB(tableName, query)

    data = defaultdict(dict)
    for _time, accnt, uname, pwd in result:
        data[accnt][uname] = [_time, pwd]
    return data


def insertRecord(tableName, time_, account, uname, pwd):
    query = """
    INSERT INTO Pwords (time, account, username, passwd) values (?, ?, ?, ?)
    """
    openDB(tableName, query, (time_, account, uname, pwd), commit=True)
    

def updatePasswd(tableName, time_, acct, uname, newPasswd):
    query = f"""
    UPDATE Pwords 
    SET 
        passwd ='{newPasswd}',
        time = '{time_}'
    WHERE 
        account='{acct}' and username='{uname}'
    """
    openDB(tableName, query, commit=True)
    
    
def deleteAccount(tableName, account):
    query = """
    DELETE FROM Pwords
    WHERE
        account=?
    """
    openDB(tableName, query, values=(account,), commit=True)

    
def deleteUsername(tableName, account, username):
    query = """
    DELETE FROM Pwords
    WHERE
        account=? and username=?
    """
    openDB(tableName, query, values=(account, username), commit=True)