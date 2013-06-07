import os
import sys
#from db import BankTable
import db

def printBankTable():
    os.system("make print-db");

def clearBankTable():
    os.system("make clear-db");

def log(str):
    sys.stderr.write(str + "\n")

def getAcceptedFlag(op):
    if op == "accept":
        return db.BankTable.FLAG_ACCEPTED;
    elif op == "unaccept":
        return db.BankTable.FLAG_UNACCEPTED;
    else:
        return db.BankTable.FLAG_POSTPONED;
