from scratch.citic import CiticGetter
from scratch.cmb import CmbGetter
from scratch.cgb import CgbGetter
from scratch import ccb
bl = ccb.BanksGetter().fetchBankList();
if bl != None:
    for b in bl:
        print b
