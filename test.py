from scratch.citic import CiticGetter
from scratch.cmb import CmbGetter
bl = CmbGetter().fetchBankList();
for b in bl:
    print b
