import csv, glob, re
import matplotlib.pyplot as plt
import numpy as np

devre = re.compile(r'\[(.*)\(')

# Read in data
devices = ["Al_%.1f_%d" % (t1, t2) for t1 in np.arange(0.5, 2.5, 0.5) for t2 in np.arange(5, 15, 5)]
devices += ["Al2O3_%.1f_%d" % (t1, t2) for t1 in np.arange(0.5, 2.5, 0.5) for t2 in np.arange(5, 15, 5)]
for dev in ['Al', 'Al2O3']:
    for t2 in np.arange(5, 15, 5):
        for t1 in np.arange(0, 2.5, 0.5):
            caps = []
            for f in glob.glob('data/C-V Sweep [%s_%.1f_%d*.csv' % (dev, t1, t2)):
                data = csv.reader(open(f))
                cv = map(lambda entry: (float(entry[1]), float(entry[2])), filter(lambda entry: entry[0] == 'DataValue', data))
                vs, cs = zip(*cv)
                vs = [list(vs[i:i+101]) for i in range(0, len(vs), 202)]
                cs = [list(cs[i:i+101]) for i in range(0, len(cs), 202)]
                freqs = [1e3, 1e4, 1e5, 1e6, 5e6]

                for v, c in zip(vs[0], cs[0]):
                    if round(v*10000) == 10000. and c < 1e-9:
                        caps.append(c)
                
            if caps != []:
                print dev, t1, t2
                print len(caps)
                print np.mean(caps)
                print np.std(caps)
                print caps