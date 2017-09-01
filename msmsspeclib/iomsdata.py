'''
@package iomsdata.py

iomsdata.py was writen by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>
and is distributed under LGPL version 3

Geneve August 2017
'''

class Compound(object):
    def __init__(self, name, smiles, precmz, prectype, ionmode, tr, inst, insttype, collenergy, biosource, links, spectra):
        self.name = name
        self.smiles = smiles
        self.precmz = precmz.replace(",", ".")
        self.prectype = prectype
        self.inst = inst
        self.insttype = insttype
        self.collenergy = collenergy
        self.spectra = spectra
        self.tr = tr
        self.ionmode = ionmode
        self.links = links
        self.biosource = biosource

    def debug(self):
        print("Name: %s" % (self.name))
        print("SMILES: %s" % (self.smiles))
        print("INCHIKEY: %s" % (self.inchiKey))
        print("Precursor m/z: %s" % (self.precmz))
        print("Retention time: %s" % (self.tr))
        print("Precursor type: %s" % (self.prectype))
        print("Collision energy: %s" % (self.collenergy))
        print("Spectra:")
        self.spectra.debug()

class MSMSspectra(object):
    """ MSMSSpectra data structure """
    def __init__(self):
        """ init the class """
        self.mass = []
        self.intensity = []

    def debug(self):
        """ debug the signal to standard out """
        for i in range(len(self.mass)):
            print("%.4f  %.4f" % (self.mass[i], self.intensity[i]))

    def sortMZ(self):
        """ sort m/z and intensity by mass """
        l = []
        for i in range(len(self.mass)):
            l.append([self.mass[i], i])
        l.sort(key=lambda x: x[0])
        intensity_ = []
        for i in range(len(l)):
            self.mass[i] = l[i][0]
            intensity_.append(self.intensity[l[i][1]])
        del self.intensity[:]
        self.intensity = intensity_

    def totxt(self):
        """ return spectra to a txt variable"""
        txt = ""
        for i in range(len(self.mass)):
            txt += "%.4f\t%.4f\n" % (self.mass[i], self.intensity[i])
        return txt

    def getMZIntensityMax(self):
        """ get the maximum intensity """
        return self.mass[self.intensity.index(max(self.intensity))]

    def getIntensityMax(self):
        """ get the maximum intensity """
        return float(max(self.intensity))

    def signal_size(self):
        """ return the size of the ms/ms spectra """
        return len(self.mass)

    def clear(self):
        """ remove all element from the mass and intensity vectors """
        del self.mass[:]
        del self.intensity[:]

def drange(start, stop, step):
    """Create a range of double numbers from start to stop according to a step"""
    r = start
    while r < stop:
        yield r
        r += step

def nsplit(s, delim=None):
    """Split string according a delimiter and removing empty fields"""
    if delim == None:
        import re
        return [x for x in re.split(u'\s|\u200b', s) if x]
    else:
        return [x for x in s.split(delim) if x]

def spectraconvert(spectra, ival=0.15):
    """ spectralconvert method
        - Convert the spectra to relative intensity scale
        - Filter the intensity according a ival value
    """
    rint = []
    maxint = float(spectra.getIntensityMax())
    for i in range(spectra.signal_size()):
        rint.append(float(spectra.intensity[i]/maxint))

    new_spectra = MSMSspectra()
    for i in range(spectra.signal_size()):
        if rint[i] >= ival:
            new_spectra.mass.append(spectra.mass[i])
            new_spectra.intensity.append(rint[i])
        else:
            continue
    """
    def spectraconvert(spectra, mzmin=50.0, mzmax=400.0, mzstep=0.05, kind_="cubic", ival=0.15):
    - Interpolate the spectra ???
    - Convert the signals in a same scale for dot products
    new_spectra = MSMSspectra()
    from scipy.interpolate import interp1d
    f = interp1d(spectra.mass, rint)
    for mz in drange(mzmin, mzmax, mzstep):
        new_spectra.mass.append(mz)
        intensity = f(mz)
        new_spectra.intensity.append(intensity)
        if intensity >= ival:
            new_spectra.intensity.append(intensity)
        else:
            new_spectra.intensity.append(0.)
    """
    return new_spectra

def readOrbitrapSpectra(fname):
    """Read orbitrap output ms/ms csv"""
    name = "None"
    smiles = "None"
    precmz = "None"
    prectype = "None"
    insttype = "None"
    collenergy = "None"
    spectra = MSMSspectra()
    getspectra = False
    fi = open(fname, "r")
    for line in fi:
        if "SPECTRUM" in line:
            name_ = nsplit(line.strip(), ";")[-1]
            if "SPECTRUM" not in name_:
                name = name_
            else:
                name = "None"
        elif "Mass" in line:
            getspectra = True
        else:
            if getspectra == True:
                v = nsplit(line.strip(), ";")
                if len(v) == 2:
                    spectra.mass.append(float(v[0].replace(",",".")))
                    spectra.intensity.append(float(v[1].replace(",",".")))
                else:
                    continue
            else:
                continue

    fi.close()
    return Compound(name, "None", "None", "None", "None", "None", "None", "None", "None", "None", "None", spectra)

def readMoNaCSV(fname):
        """Read MoNa csv database extracted with MoNaJSON2CSV.py"""
        compounds = []
        name = "None"
        smiles = "None"
        precmz = "None"
        prectype = "None"
        insttype = "None"
        collenergy = "None"
        spectra = MSMSspectra()

        fi = open(fname, "r")
        for line in fi:
            v = nsplit(line.strip(), ";")
            name = v[0]
            precmz = v[1]
            prectype = v[2]
            smiles = v[4]
            insttype = v[5]
            collenergy = v[9]
            signals = nsplit(v[10], " ")
            for sig in signals:
                a = nsplit(sig, ":")
                spectra.mass.append(float(a[0].replace(",",".")))
                spectra.intensity.append(float(a[1].replace(",",".")))
            compounds.append(Compound(name, smiles, precmz, prectype, "None", "None", "None", insttype, collenergy, "None", "None", spectra))
        fi.close()

        return compounds

def readMSP(fname):
        """Read MSP file type """
        compounds = []
        name = "N/A"
        smiles = "N/A"
        precmz = "N/A"
        prectype = "N/A"
        ionmode = "N/A"
        insttype = "N/A"
        inst = "N/A"
        collenergy = "N/A"
        tr = "N/A"
        biosource = "N/A"
        links = "N/A"
        spectra = MSMSspectra()
        getspectra = False
        fi = open(fname, "r")
        for line in fi:
            if "name" in line.lower():
                if getspectra == True:
                    compounds.append(Compound(name, smiles, precmz, prectype, ionmode, tr, inst, insttype, collenergy, biosource, links, spectra))
                    spectra = MSMSspectra()
                    getspectra = False
                name = nsplit(line.strip(), ":")[-1].strip()
            elif "precursormz" in line.lower():
                precmz = nsplit(line.strip(), ":")[-1].strip()
            elif "precursortype" in line.lower():
                prectype = nsplit(line.strip(), ":")[-1].strip()
            elif "instrumenttype" in line.lower():
                insttype = nsplit(line.strip(), ":")[-1].strip()
            elif "instrument" in line.lower():
                inst = nsplit(line.strip(), ":")[-1].strip()
            elif "smiles" in line.lower():
                smiles = nsplit(line.strip(), ":")[-1].strip()
            elif "collisionenergy" in line.lower():
                collenergy = nsplit(line.strip(), ":")[-1].strip()
            elif "retentiontime" in line.lower():
                tr = nsplit(line.strip(), ":")[-1].strip()
            elif "ionmode" in line.lower():
                ionmode = nsplit(line.strip(), ":")[-1].strip()
            elif "ionmode" in line.lower():
                ionmode = nsplit(line.strip(), ":")[-1].strip()
            elif "links" in line.lower():
                links = nsplit(line.strip(), ":")[-1].strip()
            elif "num peaks" in line.lower():
                getspectra = True
            else:
                if getspectra == True:
                    a = nsplit(line.strip(), "\t")
                    if len(a) == 2:
                        spectra.mass.append(float(a[0].replace(",",".")))
                        spectra.intensity.append(float(a[1].replace(",",".")))
                    else:
                        continue
                else:
                    continue
        compounds.append(Compound(name, smiles, precmz, ionmode, tr, prectype, inst, insttype, collenergy, biosource, links, spectra))
        fi.close()
        return compounds

def writeMSP(fname, compound):
    fo = open(fname, "a")
    fo.write("NAME: %s\n" % (compound.name))
    fo.write("PRECURSORMZ: %s\n" % (compound.precmz))
    fo.write("PRECURSORTYPE: %s\n" % (compound.prectype))
    fo.write("INSTRUMENTTYPE: %s\n" % (compound.insttype))
    fo.write("INSTRUMENT: %s\n" % (compound.inst))
    fo.write("COLLISIONENERGY: %s\n" % (compound.collenergy))
    fo.write("SMILES: %s\n" % (compound.smiles))
    fo.write("RETENTIONTIME: %s\n" % (compound.tr))
    fo.write("IONMODE: %s\n" % (compound.ionmode))
    fo.write("BIOLOGICALSOURCE: %s\n" % (compound.biosource))
    fo.write("Links: %s\n" % (compound.links))
    fo.write("Num Peaks: %d\n" % (compound.spectra.signal_size()))
    for j in range(compound.spectra.signal_size()):
        fo.write("%.4f\t%.4f\n" % (compound.spectra.mass[j], compound.spectra.intensity[j]))
    fo.write("\n")
    fo.close()

def readMGF(fname):
        """Read MGF file type """
        compounds = []
        name = "N/A"
        smiles = "N/A"
        precmz = "N/A"
        prectype = "N/A"
        ionmode = "N/A"
        insttype = "N/A"
        inst = "N/A"
        collenergy = "N/A"
        tr = "N/A"
        biosource = "N/A"
        links = "N/A"
        spectra = None
        fi = open(fname, "r")
        for line in fi:
            if "end ions" == line.lower().strip():
                compounds.append(Compound(name, smiles, precmz, prectype, ionmode, tr, inst, insttype, collenergy, biosource, links, spectra))
            elif "begin ions" in line.lower().strip():
                name = "N/A"
                smiles = "N/A"
                precmz = "N/A"
                prectype = "N/A"
                ionmode = "N/A"
                insttype = "N/A"
                inst = "N/A"
                collenergy = "N/A"
                tr = "N/A"
                biosource = "N/A"
                links = "N/A"
                spectra = MSMSspectra()
            elif "=" in line:
                a = nsplit(line.strip(), "=")
                if "name" == a[0].lower().strip():
                    name = a[-1].strip()
                elif "precursormz" == a[0].lower().strip():
                    precmz = a[-1].strip()
                elif "precursortype" == a[0].lower().strip():
                    prectype = a[-1].strip()
                elif "instrumenttype" == a[0].lower().strip():
                    insttype = a[-1].strip()
                elif "instrument" == a[0].lower().strip():
                    inst = a[-1].strip()
                elif "smiles" == a[0].lower().strip():
                    smiles = a[-1].strip()
                elif "collisionenergy" == a[0].lower().strip():
                    collenergy = a[-1].strip()
                elif "retentiontime" == a[0].lower().strip():
                    tr = a[-1].strip()
                elif "ionmode" == a[0].lower().strip():
                    ionmode = a[-1].strip()
                elif "ionmode" == a[0].lower().strip():
                    ionmode = a[-1].strip()
                elif "links" == a[0].lower().strip():
                    links = a[-1].strip()
            else:
                a = nsplit(line.strip(), " ")
                if len(a) == 2:
                    spectra.mass.append(float(a[0].replace(",",".")))
                    spectra.intensity.append(float(a[1].replace(",",".")))
                else:
                    continue
        fi.close()

        return compounds

def writeMGF(fname, compound):
    fo = open(fname, "a")
    fo.write("BEGIN IONS\n")
    fo.write("NAME=%s\n" % (compound.name))
    fo.write("PRECURSORMZ=%s\n" % (compound.precmz))
    fo.write("PRECURSORTYPE=%s\n" % (compound.prectype))
    fo.write("INSTRUMENTTYPE=%s\n" % (compound.insttype))
    fo.write("INSTRUMENT=%s\n" % (compound.inst))
    fo.write("COLLISIONENERGY=%s\n" % (compound.collenergy))
    fo.write("SMILES=%s\n" % (compound.smiles))
    fo.write("RETENTIONTIME=%s\n" % (compound.tr))
    fo.write("IONMODE=%s\n" % (compound.ionmode))
    fo.write("BIOLOGICALSOURCE=%s\n" % (compound.biosource))
    fo.write("LINKS=%s\n" % (compound.links))
    for j in range(compound.spectra.signal_size()):
        fo.write("%.4f %.4f\n" % (compound.spectra.mass[j], compound.spectra.intensity[j]))
    fo.write("END IONS\n")
    fo.close()
