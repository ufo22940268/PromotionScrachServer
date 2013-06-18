#coding=utf-8
import urllib
import json
import re
from bank import Bank
from bs4 import BeautifulSoup
import db
import util

import scratch.abc
import scratch.boc
import scratch.ccb
import scratch.cib
import scratch.cmb
import scratch.ecitic
import scratch.icbc
import scratch.spdb


ALL_BANKS = [
        scratch.abc,
        scratch.boc,
        scratch.ccb,
        scratch.cib,
        scratch.cmb,
        scratch.ecitic,
        scratch.icbc,
        scratch.spdb,
        ]

TEST_BANKS = {
        scratch.abc,
        scratch.spdb,
        }

def real(index):
    return index*2;

def main():
    #for bankEntity in ALL_BANKS:
    for bankEntity in TEST_BANKS:
        getter = bankEntity.BanksGetter();
        name = getter.getName();
        banks = getter.fetchBankList();
        db.insertBankName(name);
        for b in banks:
            b.name = name;
            db.insertBank(b);

if __name__ == '__main__':
    main();
    #util.clearBankTable();

    #banks = [];
    #banks = banks  + fetchCmbBanks();
    #banks = banks  + fetchCiticBanks();
    #for b in banks:
        #db.insertBank(b);    

    #util.printBankTable();
