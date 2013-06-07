#coding=utf-8
import sqlite3
import hashlib
from bank import Bank
from util import log

class BankTable():
    COL_ID = "_id";
    COL_TITLE = "title";
    COL_FETCH_TIME = "fetch_time";
    COL_NAME = "name";
    COL_ACCEPTED = "accepted";
    COL_URL = "url";

    TABLE_NAME = "bank";

    FLAG_UNACCEPTED = 0;
    FLAG_ACCEPTED = 1;
    FLAG_POSTPONED = 2;

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

def buildWhereClause(d):
    if len(d) == 0:
        return "";

    where = "where ";
    keys = list(d.viewkeys());
    for i in range(len(keys)):
        key = keys[i];
        where = where + key + " = ? ";
        if i != len(keys) - 1:
            where += "and ";
    return where;
    

def getBankList(whereDict):
    conn = getConnection();
    c = conn.cursor();
    where = buildWhereClause(whereDict);
    c.execute("select * from " + BankTable.TABLE_NAME + " " + where, list(whereDict.viewvalues()));

    conn.commit();

    banks = [];
    for row in c.fetchall():
	bank = Bank();
	bank.name = row[BankTable.COL_NAME];
	bank.title = row[BankTable.COL_TITLE];
	bank.fetchTime = row[BankTable.COL_FETCH_TIME];
	bank.accepted = row[BankTable.COL_ACCEPTED];
	bank.url = row[BankTable.COL_URL];
        bank.id = row[BankTable.COL_ID];
	banks.append(bank);
    return banks;

def getAvailableBanks():
    return ["招商银行", "中信银行"];

def checkProm(id, opFlag):
    conn = getConnection();
    c = conn.cursor();
    c.execute("update " + BankTable.TABLE_NAME + " set " + BankTable.COL_ACCEPTED + " = ? " +
            " where " + BankTable.COL_ID + " = ?", (opFlag, id,));
    conn.commit();
    c.close();

def updateItemStates(ids, acFlag):
    conn = getConnection();
    c = conn.cursor();
    for id in ids:
        c.execute("update " + BankTable.TABLE_NAME + " set " + BankTable.COL_ACCEPTED + " = ? " +
                " where " + BankTable.COL_ID + " = ?", (acFlag, id,));
    conn.commit();
    c.close();


if __name__ == '__main__':
    createDb();
