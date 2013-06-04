#coding=utf-8
import urllib
import json
import re
from bank import Bank
from time import gmtime, strftime
import db
import util

def main():
    #f = urllib.urlopen("http://cc.cmbchina.com/SvrAjax/PromotionChange.ashx?city=0411&type=specialsale");
    f = open("cache.js");
    raw = f.readlines();
    strs = raw[:];
    if strs != None:
        i = strs[0].find("(");
        new = strs[0][:i] + strs[0][i + 1:];
        i = new.rfind(")");
        new = new[:i] + new[i + 1:];

    new = re.sub(r"(\w+):", r'"\1":', new);
    new = re.sub(r"\"http\"", r'http', new);
    blJo = json.loads(new)["list"];
    banks = [];
    for bJo in blJo:
        b = inflateBank(bJo);
        banks.append(b);

    for b in banks:
        db.insertBank(b);    

def inflateBank(jo):
    b = Bank();
    url = jo["LinkUrl"].encode("utf-8");
    if url.find("http:") == -1:
	b.url = "http://cc.cmbchina.com" + url;
    else:
	b.url = url;

    b.title = jo["Title"].encode("utf-8");
    b.name = "招商银行";
    b.fetchTime = strftime("%Y-%m-%d %H:%M:%S", gmtime());
    return b;

def temp():
    f = urllib.urlopen("http://cc.cmbchina.com/SvrAjax/PromotionChange.ashx?city=0411&type=specialsale");
    open("cache.js", "w").write(f.readline());

if __name__ == '__main__':
    util.clearBankTable();
    main()
    util.printBankTable();
