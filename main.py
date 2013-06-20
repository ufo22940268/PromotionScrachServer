#coding=utf-8
import urllib
import json
import re
from bank import Bank
from bs4 import BeautifulSoup
import db
import util
import sys

import scratch.abc
import scratch.boc
import scratch.ccb
import scratch.cib
import scratch.cmb
import scratch.ecitic
import scratch.icbc
import scratch.spdb


ALL_BANKS = [
        scratch.ecitic,
        scratch.cmb,
        scratch.abc,
        scratch.boc,
        scratch.ccb,
        scratch.cib,
        scratch.icbc,
        scratch.spdb,
        ]

TEST_BANKS = {
        scratch.ccb,
        scratch.boc,
        }

def real(index):
    return index*2;

def fetchProms(bankEntities):
    for bankEntity in bankEntities:
        getter = bankEntity.BanksGetter();
        name = getter.getName();
        try: 
            banks = getter.fetchBankList();
            db.insertBankName(name);
            for b in banks:
                b.name = name;
                db.insertBank(b);
        except:
            print "bank %s error" % (name,);

def help():
    print '''
            ussage:
                python main.py [normal|test]'''


if __name__ == '__main__':
    if len(sys.argv) < 2:
        help();
        exit(-1);

    if sys.argv[1] == "normal":
        fetchProms(ALL_BANKS);
    elif sys.argv[1] == "test": 
        fetchProms(TEST_BANKS);
    else:
        help();
        exit(-1);
