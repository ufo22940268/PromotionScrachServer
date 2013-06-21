#coding=utf-8
import sys
import sqlite3
import hashlib
from bank import Bank
import settings
from settings import *
import util
from datetime import datetime

class BankTable():
    COL_ID = "_id";
    COL_TITLE = "title";
    COL_FETCH_TIME = "fetch_time";
    COL_NAME = "name";
    COL_ACCEPTED = "accepted";
    COL_URL = "url";
    COL_HASH = "hash";
    COL_CITY_ID = "city_id";

    TABLE_NAME = "bank";

    FLAG_UNACCEPTED = 0;
    FLAG_ACCEPTED = 1;
    FLAG_POSTPONED = 2;

class NameTable():
    COL_ID = "_id";
    COL_NAME = "name";

    TABLE_NAME = "name";

class CityTable():
    COL_ID = "_id";
    COL_NAME = "name";

    TABLE_NAME = "city";
    DEFAULT_ID = -1;

def getConnection():
    dbName = settings.getDbName();
    conn = sqlite3.connect(dbName);
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
                + BankTable.COL_ACCEPTED + " INTEGER DEFAULT " + str(BankTable.FLAG_POSTPONED) + ", " 
                + BankTable.COL_URL + " TEXT," 
                + BankTable.COL_HASH + " INTEGER," 
                + BankTable.COL_CITY_ID + " INTEGER,"
                + "FOREIGN KEY (" + BankTable.COL_CITY_ID + ") REFERENCES " + CityTable.TABLE_NAME + "(" + CityTable.COL_ID + ")"
                + ")");

    c.execute("DROP TABLE IF EXISTS " + NameTable.TABLE_NAME);
    c.execute("CREATE TABLE " + NameTable.TABLE_NAME + "(" 
                + NameTable.COL_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, "
                + NameTable.COL_NAME + " TEXT " 
                + ")");

    c.execute("DROP TABLE IF EXISTS %s" % CityTable.TABLE_NAME);
    c.execute("CREATE TABLE %(table)s(%(id)s INTEGER PRIMARY KEY AUTOINCREMENT, %(name)s TEXT)" % \
	    {"table":CityTable.TABLE_NAME, "id":CityTable.COL_ID, "name":CityTable.COL_NAME});

    conn.commit();
    c.close();

def insertBank(bank):
    conn = getConnection();
    c = conn.cursor();

    now = datetime.now().strftime('%Y-%m-%d');
    cityId = getCityId(bank.city);
    hashCode = bank.hashCode();
    if not hasInDb(hashCode) and not bank.isExpired():
        c.execute("INSERT INTO bank(" 
		+ BankTable.COL_TITLE + "," 
		+ BankTable.COL_FETCH_TIME  + "," 
		+ BankTable.COL_NAME + "," 
		+ BankTable.COL_URL + "," 
		+ BankTable.COL_HASH + "," 
		+ BankTable.COL_CITY_ID + ")" 
		+ " values(?, ?, ?, ?, ?, ?)",
                (bank.title.decode("utf-8"), now, bank.name.decode("utf-8"), bank.url.decode("utf-8"), hashCode, cityId,));
        conn.commit();

    c.close();
    return True;

def removeBank(bank):
    conn = getConnection();
    c = conn.cursor();
    c.execute("delete from %s where %s = ?" % (BankTable.TABLE_NAME, BankTable.COL_HASH) ,(bank.hashcode(),));
    conn.commit();
    c.close();

def removeBankByName(name):
    conn = getConnection();
    c = conn.cursor();
    c.execute("delete from " + BankTable.TABLE_NAME
            + " where " + BankTable.COL_NAME + " = ?", (name.decode("utf-8"),));
    conn.commit();
    c.close();
    

def updateBank(bank):
    conn = getConnection();
    c = conn.cursor();

    if bank.isExpired():
        removeBank(bank);
        return;

    if not hasInDb(bank.hashCode()):
        insertBank(bank);
    else:
        now = datetime.now().strftime('%Y-%m-%d');
        cityId = getCityId(bank.city);
        print "update:", bank;
        c.execute("UPDATE " + BankTable.TABLE_NAME + " SET " 
                + BankTable.COL_TITLE + " = ?," 
                + BankTable.COL_FETCH_TIME  + " = ?," 
                + BankTable.COL_NAME + " = ?," 
                + BankTable.COL_URL + " = ?," 
                + BankTable.COL_CITY_ID + " = ?" +
                " where " + BankTable.COL_HASH + " = ?",
                (bank.title.decode("utf-8"), now, bank.name.decode("utf-8"), bank.url.decode("utf-8"), cityId, bank.hashCode()));
        conn.commit();

    c.close();
    return True;

def hasInDb(hashCode):
    conn = getConnection();
    c = conn.cursor();
    c.execute("SELECT * FROM %(table)s WHERE %(c_hash)s = ?" % {"table":BankTable.TABLE_NAME, "c_hash":BankTable.COL_HASH},
            (hashCode,));
    conn.commit();
    cnt = len(c.fetchall());
    c.close();
    return cnt != 0;


def insertBankName(name):
    name = name.decode("utf-8");
    conn = getConnection();
    c = conn.cursor();

    if not hasBankNameInDb(name):
        c.execute("INSERT INTO " + NameTable.TABLE_NAME + "(" + NameTable.COL_NAME + ") values(?)",
                (name,));
        conn.commit();
    c.close();
    return True;

def hasBankNameInDb(name):
    conn = getConnection();
    c = conn.cursor();
    c.execute("SELECT * FROM %(table)s WHERE %(name)s = ?" % {"table":NameTable.TABLE_NAME, "name":NameTable.COL_NAME},
            (name,));
    conn.commit();
    cnt = len(c.fetchall());
    c.close();
    return cnt != 0;

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

def hasBankName(name):
    conn = getConnection();
    c = conn.cursor();
    c.execute("select * from %s where %s = ?" % (NameTable.TABLE_NAME, NameTable.COL_NAME), (name.decode("utf-8"),));
    cnt = len(c.fetchall());
    conn.commit();
    c.close();
    return cnt != 0;
    

def getBankList(whereDict, city="all"):
    conn = getConnection();
    c = conn.cursor();
    where = buildWhereClause(whereDict);
    if city and city != "all":
	where += " and ct_name = '%s'" % city;

    c.execute("SELECT * FROM " + BankTable.TABLE_NAME 
	    + " LEFT OUTER JOIN " 
            + " (SELECT _id AS ct_id, name AS ct_name FROM city) "  
            + " ON ct_id == " + BankTable.COL_CITY_ID + " "
	    + where, list(whereDict.viewvalues()));

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
	city = row["ct_name"];
	if city:
	    bank.city = city;
	banks.append(bank);
    return banks;

def getAvailableBanks():
    conn = getConnection();
    c = conn.cursor();
    c.execute("SELECT " + NameTable.COL_NAME + " from " + NameTable.TABLE_NAME);
    conn.commit();

    names = [];
    for row in c.fetchall():
        names.append(row[NameTable.COL_NAME]);
    return names;

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

def getCityId(name):
    if not name:
	return CityTable.DEFAULT_ID;

    conn = getConnection();
    c = conn.cursor();
    c.execute("select * from %(table)s where %(name)s = ?" % {"table":CityTable.TABLE_NAME, "name":CityTable.COL_NAME,}, (name.decode("utf-8"),)) ;
    conn.commit();
    rows = c.fetchall();
    id = None;
    if len(rows) > 0:
	id = rows[0][CityTable.COL_ID];
    else:
	id = insertNewCity(name);
    return id;

def insertNewCity(city):
    conn = getConnection();
    c = conn.cursor();
    c.execute("insert into %s(%s) values(?)" % (CityTable.TABLE_NAME, CityTable.COL_NAME), (city.decode("utf-8"),));
    conn.commit();
    id =  c.lastrowid;
    c.close();
    return id;

def help():
    print ''' usage:
                python db.py create-db''';

if __name__ == '__main__':
    if len(sys.argv) < 2:
        help();
        exit(-1);

    if sys.argv[1] == "create-db":
        createDb();
    else:
        help();
        exit(-1);
