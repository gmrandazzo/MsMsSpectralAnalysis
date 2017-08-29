#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from msmsspeclib.iomsdata import *
from msmsspeclib.MSMSVectorSpace import *

def main():
    if len(sys.argv) == 4:
        mol1 = None
        mol2 = None
        if sys.argv[3].lower() == "mona":
            mol1 = readMoNaCSV(sys.argv[1])[0]
            mol2 = readMoNaCSV(sys.argv[2])[1]
        elif sys.argv[3].lower() == "orbitrap":
            mol1 = readOrbitrapSpectra(sys.argv[1])
            mol2 = readOrbitrapSpectra(sys.argv[2])
        else:
            return

        print(mol1.insttype, mol2.insttype)
        mol1.spectra = spectraconvert(mol1.spectra, 0.01)
        mol2.spectra = spectraconvert(mol2.spectra, 0.01)

        msmscmp = MSMSVectorSpace(5.0)

        vfp = []
        msmscmp.FPMassVector(vfp, mol1.spectra)
        msmscmp.FPMassVector(vfp, mol2.spectra)
        vfp.sort()

        fp1 = msmscmp.genGlobalMSMSFingerprint(vfp, mol1.spectra)
        fp2 = msmscmp.genGlobalMSMSFingerprint(vfp, mol2.spectra)

        similarity = msmscmp.cosine_similarity(fp1, fp2)

        print("Spectral similarity: %.2f" % (similarity))

        width = 0.30       # the width of the bars

        fig = plt.figure()
        ax = fig.add_subplot(111)

        rects1 = ax.bar(mol1.spectra.mass, mol1.spectra.intensity, width, color='r')
        for i in range(mol2.spectra.signal_size()):
            mol2.spectra.intensity[i] *= -1

        rects2 = ax.bar(mol2.spectra.mass, mol2.spectra.intensity, width, color='g')
        ax.set_ylabel('intensity')
        #ax.legend( (rects1[0], rects2[0], rects3[0]), ('y', 'z', 'k') )

        def autolabel(rects):
            for rect in rects:
                h = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                        ha='center', va='bottom')

        #autolabel(rects1)
        #autolabel(rects2)

        plt.show()
    else:
        print("Usage: %s [spectra 1] [spectra 2] [\"mona\" or \"orbitrap\"]" % (sys.argv[0]))

if __name__ == '__main__':
    main()
