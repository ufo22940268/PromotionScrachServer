#coding=utf-8
import sqlite3
import hashlib
from bank import Bank

class BankTable():
    COL_ID = "_id";
    COL_TITLE = "title";
    COL_FETCH_TIME = "fetch_time";
    COL_NAME = "name";
    COL_ACCEPTED = "accepted";
    COL_URL = "url";

    TABLE_NAME = "bank";

def getConnection():
    conn = sqlite3.connect("content.db");
    conn.row_factory = sqlite3.Row;
    return conn;

def createDb():
    conn = getConnection();
    c = conn.cursor();
    c.execute("DROP TABLE IF EXISTS bank");
    c.execute("CREATE TABLE bank(" 
                + BankTable.COL_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, "
                + BankTable.COL_TITLE + " TEXT, " 
                + BankTable.COL_FETCH_TIME + " TEXT, " 
                + BankTable.COL_NAME + " TEXT, " 
                + BankTable.COL_ACCEPTED + " INTEGER DEFAULT 0, " 
                + BankTable.COL_URL + " TEXT" 
                + ")");
    conn.commit();
    c.close();

def insertBank(bank):
    conn = getConnection();
    c = conn.cursor();

    c.execute("INSERT INTO bank(" + BankTable.COL_TITLE + "," + BankTable.COL_FETCH_TIME  + "," + BankTable.COL_NAME + "," + BankTable.COL_URL + ") values(?, ?, ?, ?)",
            (bank.title.decode("utf-8"), bank.fetchTime, bank.name.decode("utf-8"), bank.url.decode("utf-8")));
    conn.commit();
    c.close();
    return True;

def getBankList(name=None):
    conn = getConnection();
    c = conn.cursor();
    if name == None:
        c.execute("select * from " + BankTable.TABLE_NAME);
    else:
        c.execute("select * from " + BankTable.TABLE_NAME + " where name = '" + name + "'");

    conn.commit();

    banks = [];
    for row in c.fetchall():
	bank = Bank();
	bank.name = row[BankTable.COL_NAME];
	bank.title = row[BankTable.COL_TITLE];
	bank.fetchTime = row[BankTable.COL_FETCH_TIME];
	bank.accepted = row[BankTable.COL_ACCEPTED];
	bank.url = row[BankTable.COL_URL];
	banks.append(bank);
    return banks;

def getAvailableBanks():
    return ["招商银行", "中信银行"];

if __name__ == '__main__':
    createDb();
