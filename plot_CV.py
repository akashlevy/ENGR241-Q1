import csv, glob, re
import matplotlib.pyplot as plt
import numpy as np

devre = re.compile(r'\[(.*)\(')

# Read in data
for f in glob.glob('data/C-V*.csv'):
    device = devre.search(f).group(1)
    data = csv.reader(open(f))
    cv = map(lambda entry: (float(entry[1]), float(entry[2])), filter(lambda entry: entry[0] == 'DataValue', data))
    vs, cs = zip(*cv)
    vs = [list(vs[i:i+101]) for i in range(0, len(vs), 202)]
    cs = [list(cs[i:i+101]) for i in range(0, len(cs), 202)]
    freqs = [1e3, 1e4, 1e5, 1e6, 5e6]

    # Set the font dictionaries (for plot title and axis titles)
    title_font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'bold', 'verticalalignment':'bottom'}
    axis_font = {'fontname':'Arial', 'size':'12'}

    # Plot data
    plt.title('MOSCAP C-V %s' % device)
    plt.xlabel('$V_{G}$ (V)', **axis_font)
    plt.ylabel('$C_{GB}$ (F)', **axis_font)
    lines = []
    for v, c in zip(vs, cs):
        line, = plt.semilogy(v, c)
        lines.append(line)
    plt.legend(lines, ['$V_{G}$=%s Hz' % int(freq) for freq in freqs])
    plt.show()