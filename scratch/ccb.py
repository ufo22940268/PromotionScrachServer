#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log

class BanksGetter(BaseGetter):
    def getName(self):
        return "建设银行";

    def fetchBankList(self):
        banks = [];
	return banks;
