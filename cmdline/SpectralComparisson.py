#!/usr/bin/env python

import sys
import string
import math
import multiprocessing

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from msmsspeclib.iomsdata import *
from msmsspeclib.MSMSVectorSpace import *


"""
babel_bin="/usr/local/bin/babel"
obminimize_bin="/usr/local/bin/obminimize"

def GetNCPU():
    return multiprocessing.cpu_count()

def babel(cmd):
    os.system(babel_bin+" "+cmd)

def MultiThread(mollst, options, input_type, output_type):
    listcmd = []
    for i in range(len(mollst)):
        outname = mollst[i]
        inp_sufx = input_type.replace("-i", "")
        out_sufx = output_type.replace("-o", "")
        if options == "NONE":
            cmd = ("%s \"%s\" %s \"%s\"" % (input_type, mollst[i], output_type, outname.replace((".%s" % (inp_sufx)) ,(".%s" % (out_sufx)))))
        elif "gen3d" in options.lower():
            #Fist conversion in 2D sdf
            cmd = ("--gen2D -h %s \"%s\" %s \"%s\"" % (input_type, mollst[i], "-osdf", outname.replace((".%s" % (inp_sufx)) ,(".%s" % ("sdf")))))
            #Then minimization to 3D using the GAFF (Generic Amber Forcefield)
            #obminimize -ff GAFF -o mol2 "NP-000023.mol2"  > ciao.mol2
            cmd += (";%s -ff GAFF %s \"%s\" > \"%s\"" % (obminimize_bin, output_type, mollst[i].replace(inp_sufx, "sdf"), outname.replace((".%s" % (inp_sufx)) ,(".%s" % (out_sufx)))))
            #Remove the previous sdf file
            cmd += (";rm -f  \"%s\"" % (mollst[i].replace(inp_sufx, "sdf")))
        else:
            cmd = ("%s %s \"%s\" %s \"%s\"" % (options, input_type, mollst[i], output_type, outname.replace((".%s" % (inp_sufx)) ,(".%s" % (out_sufx)))))
            print cmd
        listcmd.append(cmd)
    pool = multiprocessing.Pool(GetNCPU())
    pool.map(babel, listcmd
"""

def main():
    if len(sys.argv) >= 3:
        dbmol = []
        for i in range(1, len(sys.argv)-1):
            mol = readOrbitrapSpectra(sys.argv[i])
            mol.spectra = spectraconvert(mol.spectra, ival=0.01)
            dbmol.append(mol)
            #mol.debug()

        msmscmp = MSMSVectorSpace(5.0)

        vfp = []
        for i in range(len(dbmol)):
            msmscmp.FPMassVector(vfp, dbmol[i].spectra)
        vfp.sort()

        dmx = [[0. for i in range(len(dbmol))] for i in range(len(dbmol))]
        for i in range(len(dbmol)):
            dmx[i][i] = 1.
            for j in range(i+1, len(dbmol)):
                fp1 = msmscmp.genGlobalMSMSFingerprint(vfp, dbmol[i].spectra)
                fp2 = msmscmp.genGlobalMSMSFingerprint(vfp, dbmol[j].spectra)
                #fp1, fp2 = msmscmp.genBinaryMSMSfingerprint(dbmol[i].spectra, dbmol[j].spectra)
                dmx[i][j] = dmx[j][i] = msmscmp.cosine_similarity(fp1, fp2)
                print("Processing %d and %d" % (i, j))

        fo = open(sys.argv[-1], "w")
        fo.write("Objects\t")
        for i in range(len(dbmol)-1):
            fo.write("%s\t" % (dbmol[i].name))
        fo.write("%s\n" % (dbmol[-1].name))
        for i in range(len(dmx)):
            fo.write("%s\t" % (dbmol[i].name))
            for j in range(len(dmx[i])-1):
                fo.write("%.4f\t" % (dmx[i][j]))
            fo.write("%.4f\n" % (dmx[i][-1]))
        fo.close()

    else:
        print("Usage %s file1.csv file2.csv ... fileN.csv output.txt" % (sys.argv[0]))

if __name__ == '__main__':
    main()
