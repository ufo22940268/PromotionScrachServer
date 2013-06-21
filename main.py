#coding=utf-8
import urllib
import json
import re
from bank import Bank
from bs4 import BeautifulSoup
import db
import util
import sys
import traceback

import scratch.cmb
import scratch.ceb
import scratch.hxb
import scratch.ccb
import scratch.cmbc
import scratch.abc
import scratch.spdb
import scratch.cib
import scratch.boc
import scratch.ecitic
import scratch.icbc
import scratch.comm
import scratch.psbc
import scratch.pingan
import scratch.nbcb
import scratch.icbc

TEST_BANKS = {
        #scratch.cmb,
        scratch.ceb,
        #scratch.abc,
        }


ALL_BANKS = [
        #----------1----------
        scratch.cmb,
        scratch.ceb,
        scratch.hxb,
        scratch.ccb,
        scratch.cmbc,
        scratch.abc,
        scratch.spdb,
        scratch.cib,
        scratch.boc,
        scratch.ecitic,
        scratch.icbc,

        #----------2----------
        scratch.comm,
        scratch.psbc,
        scratch.pingan,
        scratch.nbcb,
        scratch.icbc,
        ]


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
            print traceback.print_exc();
            print "bank %s error" % (name,);

def updateProms(bankEntities):
    for bankEntity in bankEntities:
        getter = bankEntity.BanksGetter();
        name = getter.getName();
        try: 
            banks = getter.fetchBankList();
            if not db.hasBankName(name):
                print "%s bank not found" % name;
                break;

            for b in banks:
                b.name = name;
                db.updateBank(b);
        except:
            print traceback.print_exc();
            print "bank %s error" % (name,);

def help():
    print '''
            ussage:
                python main.py [normal|test|update-test]'''


if __name__ == '__main__':
    if len(sys.argv) < 2:
        help();
        exit(-1);

    if sys.argv[1] == "normal":
        fetchProms(ALL_BANKS);
    elif sys.argv[1] == "test": 
        db.createDb();
        fetchProms(TEST_BANKS);
    elif sys.argv[1] == "update-test": 
        updateProms(TEST_BANKS);
    else:
        help();
        exit(-1);
