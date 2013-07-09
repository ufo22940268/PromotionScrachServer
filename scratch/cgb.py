#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import urllib
from time import gmtime, strftime
from util import log
from datetime import datetime
import re

class BanksGetter(BaseGetter):

    def getName(self):
        return "广发银行";

    def fetchBankList(self):

        banks = [];
        baseUrls = ["http://card.cgbchina.com.cn/Channel/11820301?currentChannelPage=%d", "http://card.cgbchina.com.cn/Channel/11820220?currentChannelPage=%d", "http://card.cgbchina.com.cn/Channel/11820139?currentChannelPage=%d"];
        for baseUrl in baseUrls:
            for page in range(1, self.getPageRange()): 
                url = baseUrl % page;
                soup = self.getSoup(url);
                if not soup: 
                    break;

                youhuiContent = soup.find("div", class_="youhui_content");
                if len(youhuiContent.contents) <= 1:
                    break;

                for a in youhuiContent.find_all("a"):
                    bank = Bank();
                    title = a.string.encode("utf-8");
                    m = re.match(r"【(.*)】(.*)", title);
                    if not m:
                        bank.title = title;
                    else:
                        bank.city = m.group(1);
                        bank.title = m.group(2);

                    url =  a["href"].encode("utf-8");
                    if url.find("http") != -1:
                        bank.url = url;
                    else:
                        bank.url = "http://card.cgbchina.com.cn" + url;

                    dateStr = a.parent.find_next_sibling("p").string
                    if dateStr:
                        dateStr = dateStr.encode("utf-8").split("-")[-1].strip();
                        try:
                            bank.endDate =  datetime.strptime(dateStr, "%Y.%m.%d");
                        except ValueError:
                            pass;

                    banks.append(bank);

        return banks;
