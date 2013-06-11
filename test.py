from scratch.citic import CiticGetter
from scratch.cmb import CmbGetter
from scratch.cgb import CgbGetter
from scratch import ccb
from scratch import ceb
from scratch import cmbc
from scratch import abc
bl = abc.BanksGetter().fetchBankList();
if bl != None:
    for b in bl:
        print b
