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

def next_sibling(node, count):
    i = 0;
    for n in node.next_elements:
        i += 1;
        if i == count*2:
            return n;

def getFetchedTime():
    return os.path.getmtime("./content.db");
