#coding=utf-8
from scratch.base import BaseGetter 
from bs4 import BeautifulSoup
from bank import Bank
import city_parser
import re

class BanksGetter(BaseGetter):

    def getName(self):
        return "兴业银行";

    def fetchBankList(self):
        banks = [];

        #Country promotion.
        mainUrl = "http://creditcard.cib.com.cn/card/PromoteActivity/nationalPromotion/";
        banks += self.fetchBankListByUrl(mainUrl);

        #City promotion.
        cityUrl = "http://creditcard.cib.com.cn/card/PromoteActivity/areaPromotion/index.html";
        banks += self.fetchBankListByUrl(cityUrl);
        banks += self.getBankListIterate(cityUrl, lambda page:917596317 - page);
        banks += self.getBankListIterate(cityUrl, lambda page:1619285262 + page);
        #hk macao prmotions.
        hkUrl = "http://creditcard.cib.com.cn/card/PromoteActivity/gangaotaiyouhuizhuanqu/"
        banks += self.fetchBankListByUrl(hkUrl);
        banks += self.fetchBankListByUrl("http://creditcard.cib.com.cn/card/PromoteActivity/gangaotaiyouhuizhuanqu/index.html_917596317.html");

        #Foreign promotions.
        foreignUrl = "http://creditcard.cib.com.cn/card/PromoteActivity/jingwaiyouhuizhuanqu/jingwaicuxiao/"
        banks += self.fetchBankListByUrl(foreignUrl);
        banks += self.getBankListIterate(foreignUrl, lambda page:917596317 - page);
        foreignUrl = "http://creditcard.cib.com.cn/card/PromoteActivity/jingwaiyouhuizhuanqu/jingwaifuwu/"
        banks += self.fetchBankListByUrl(foreignUrl);

        #Hotel airplane ticket promotions.
        banks += self.fetchBankListByUrl("http://creditcard.cib.com.cn/card/PromoteActivity/jingwaiPromotion/jipiaojiudian/");

        return banks;

    def fetchBankListByUrl(self, url):
        banks = [];

        f = self.openUrl(url);
        if f == None:
            return;

        soup = BeautifulSoup(f);
        lis = soup.find_all("li", class_="link");
        for l in lis:
            b = Bank();
            a = l.find("a");
            href = a["href"].encode("utf-8")
            if href.startswith("http:"): 
                b.url = href;
            else:
		b.url = "http://creditcard.cib.com.cn" + href;

            title = a.string.strip().encode("utf-8");
	    b.city = city_parser.parseBracketStyle(title);
	    if b.city in ["兴悦会", "机票随兴订",]:
		b.city = None;
	    b.title = re.sub(r"\[.*?\](.*)", r"\1", title);
            banks.append(b);
        return banks;

    def fetchAllUrls(self):
        mainUrl = "http://creditcard.cib.com.cn/card/PromoteActivity/nationalPromotion/";

        urls = [];
        urls.append(mainUrl);
        f = self.openUrl(mainUrl);
        soup = BeautifulSoup(f);
        for span in soup.find("div", class_="leftmenu").find_all("span"):
            urls.append("http://creditcard.cib.com.cn" + span.contents[0]["href"].encode("utf-8"));
        return urls;

    def getBankListIterate(self, rawUrl, func):
        banks = [];
	for page in range(0, self.getPageRange()):
            url = rawUrl + "_" + str(func(page)) + ".html";
            bs =  self.fetchBankListByUrl(url);
            if bs == None:
                break;
            else:
                banks += bs;
        return banks;
