'''
Created on 21 nov. 2018

@author: Vyacheslav.Sviridov
'''

from moenm import MoENM


def main():
    with MoENM("", "", "") as moe:

        fdn = "SubNetwork=ONRM_ROOT_MO,SubNetwork=RNC1,MeContext=RNC1,ManagedElement=1,RncFunction=1,UtranCell="

        print moe.get("{0}Cell1;{0}Cell4".format(fdn), "administrativeState,userLabel", "-t")
        print moe.set("{0}Cell1;{0}Cell4".format(fdn), "--preview", userLabel="test", administrativeState="UNLOCKED")

        print moe.get("{0}Cell1;{0}Cell4".format(fdn), "administrativeState,userLabel", "-t")
        print moe.set("{0}Cell1;{0}Cell4".format(fdn), "--preview", administrativeState="LOCKED")

        print moe.get("{0}Cell1;{0}Cell4".format(fdn), "administrativeState,userLabel", "-t")

        fdn = "SubNetwork=ONRM_ROOT_MO,SubNetwork=Subn1,MeContext=Rbs1,ManagedElement=1,ENodeBFunction=1,EUtranCellFDD=ECell1"

        print moe.get(fdn, "earfcndl,earfcnul", "-t")
        print moe.action(fdn, "changeFrequency", "--preview", earfcn="3456")


if __name__ == '__main__':
    main()
