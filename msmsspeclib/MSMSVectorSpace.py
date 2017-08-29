'''
@package MSMSVectorSpace.py

MSMSVectorSpace.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve August 2017
'''


import math

class MSMSVectorSpace(object):
    def __init__(self, ppm):
        self.ppm = ppm

    def DaltonError(self, mass):
        return mass/((1/self.ppm) * 1000000);

    def FPMassVector(self, vfp, spectre):
        if len(vfp) == 0:
            vfp.extend(spectre.mass)
        else:
            vspec = []
            for i in range(spectre.signal_size()):
                mserror = self.DaltonError(spectre.mass[i])
                getvspec = True
                for j in range(len(vfp)):
                    if math.fabs(spectre.mass[i] - vfp[j]) <= mserror:
                        getvspec = False
                        break
                    else:
                        continue
                if getvspec == True:
                    vspec.append(spectre.mass[i])
                else:
                    continue
            vfp.extend(vspec)

    def genGlobalMSMSFingerprint(self, vfp, spectre):
        fp = [0. for i in range(len(vfp))]
        for j in range(len(vfp)):
            mserror = self.DaltonError(vfp[j])
            fpint = 0.
            nint = 0
            for i in range(spectre.signal_size()):
                if math.fabs(spectre.mass[i] - vfp[j]) <= mserror:
                     fpint += spectre.intensity[i]
                     nint += 1
                     #print("%d %d %f %f %f" % (j,i, vfp[j], spectre1.mass[i], spectre1.intensity[i]))
                else:
                    continue
            if nint > 0:
                fp[j] = fpint/float(nint)
            else:
                fp[j] = 0.
        #print "-"*10
        #for i in range(len(vfp)):
        #    print("%f %f" % (vfp[i], fp[i]))
        #print "-"*10
        return fp

    def genBinaryMSMSfingerprint(self, spectre1, spectre2):
        vfp = []
        self.FPMassVector(vfp, spectre1)
        self.FPMassVector(vfp, spectre2)
        vfp.sort()

        #build the fingerprint 1 and the fingerprint 2
        fp1 = [0. for i in range(len(vfp))]
        for j in range(len(vfp)):
            mserror = self.DaltonError(vfp[j])
            fpint = 0.
            nint = 0
            for i in range(spectre1.signal_size()):
                if math.fabs(spectre1.mass[i] - vfp[j]) <= mserror:
                     fpint += spectre1.intensity[i]
                     nint += 1
                     #print("%d %d %f %f %f" % (j,i, vfp[j], spectre1.mass[i], spectre1.intensity[i]))
                else:
                    continue
            if nint > 0:
                fp1[j] = fpint/float(nint)
            else:
                fp1[j] = 0.
            #print "-"*8
        fp2 = [0. for i in range(len(vfp))]
        for j in range(len(vfp)):
            mserror = self.DaltonError(vfp[j])
            fpint = 0.
            nint = 0
            for i in range(spectre2.signal_size()):
                if math.fabs(spectre2.mass[i] - vfp[j]) <= mserror:
                     fpint += spectre2.intensity[i]
                     nint += 1
                else:
                    continue
            if nint > 0:
                fp2[j] = fpint/float(nint)
            else:
                fp2[j] = 0.

        return fp1, fp2

    def cosine_similarity(self, fp1, fp2):
        "compute cosine similarity of fp1 to fp2: (fp1 dot fp2)/{||fp1||*||fp2||)"
        if len(fp1) == len(fp2):
            sumxx, sumxy, sumyy = 0, 0, 0
            for i in range(len(fp1)):
                x = fp1[i]
                y = fp2[i]
                sumxx += x*x
                sumyy += y*y
                sumxy += x*y
            return sumxy/math.sqrt(sumxx*sumyy)
        else:
            return 0.
