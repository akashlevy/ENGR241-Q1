import csv, glob, re
import matplotlib.pyplot as plt
import numpy as np
from intersection import intersection

devre = re.compile(r'\[(.*)\(')

# Read in data
devices = ["Al_%.1f_%d" % (t1, t2) for t1 in np.arange(0.5, 2.5, 0.5) for t2 in np.arange(5, 15, 5)]
devices += ["Al2O3_%.1f_%d" % (t1, t2) for t1 in np.arange(0.5, 2.5, 0.5) for t2 in np.arange(5, 15, 5)]
for dev in ['Al', 'Al2O3']:
    for t2 in np.arange(5, 15, 5):
        for t1 in np.arange(0, 2.5, 0.5):
            for plotter in [plt.plot, plt.semilogy]:
                bvs = []
                for f in glob.glob('data/Breakdown [%s_%.1f_%d*.csv' % (dev, t1, t2)):
                    # Read data
                    data = csv.reader(open(f))
                    iv = map(lambda entry: (float(entry[1]), float(entry[2])), filter(lambda entry: entry[0] == 'DataValue', data))
                    vvals, ivals = zip(*iv)

                    # Compute breakdown voltage based on 1mA threshold
                    bv = intersection(np.array(vvals), np.array(ivals), np.array([0, 50]), np.array([1e-3, 1e-3]))
                    bvs.append(bv[0][0])

                    # Set the font dictionaries (for plot title and axis titles)
                    title_font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'bold', 'verticalalignment':'bottom'}
                    axis_font = {'fontname':'Arial', 'size':'12'}

                    # Plot data
                    plt.title('MOSCAP Breakdown I-V %s_%.1f_%d' % (dev, t1, t2))
                    plt.xlabel('$V_{G}$ (V)', **axis_font)
                    plt.ylabel('$I_{GB}$ (A)', **axis_font)
                    plotter(vvals, ivals)
                plt.savefig('imgs/%s_%.1f_%d_breakdown_%s.pdf' % (dev, t1, t2, plotter.__name__), format='pdf')
                plt.close()

                if bvs != [] and plotter == plt.plot:
                    print dev, t1, t2
                    print len(bvs)
                    print np.mean(bvs)
                    print np.std(bvs)
                    print bvs


