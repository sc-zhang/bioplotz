import bioplotz as bp
import random
import matplotlib.pyplot as plt



plt.figure(figsize=(20, 20), dpi=100)

# DEMO for manhattan plot
data = {'Chr%02d'%(_+1):[[random.randint(int(0), int(2e6)) for _ in range(int(1e4))], [random.random() for _ in range(int(1e4))]] for _ in range(16)}
plt.subplot(221)
mh = bp.manhattan(data, threshold=[0.01, 0.05], threshold_line_color=['red', 'blue'], log_base=10, reverse=True)
plt.xticks(rotation=-45)

# DEMO for gene cluster
gene_list = []
offset = 0
for _ in range(20):
    gn = "Gene%0d"%(_+1)
    sp = offset+random.randint(int(1e3), int(5e4))
    ep = sp + random.randint(int(5e3), int(5e4))
    direct = '+' if random.random()>=0.5 else '-'
    color = 'green' if direct=='+' else 'orange'
    gene_list.append([gn, sp, ep, direct, color])
    offset = ep
plt.subplot(222)
gcp = bp.genecluster(gene_list)

# DEMO for chromosome plot
chr_len_db = {'Chr%02d'%(_+1): random.randint(int(1.6e6), int(2e6)) for _ in range(16)}
centro_db = {'Chr%02d'%(_+1): random.randint(int(6e5), int(1e6)) for _ in range(16)}
bed_list = []
for i in range(1000):
    chrn = "Chr%02d"%(random.randint(1, 16))
    sp = random.randint(0, int(chr_len_db[chrn]))
    ep = sp + random.randint(int(1e3), int(1e4))
    if ep >= chr_len_db[chrn]-1e3:
        continue
    if centro_db[chrn]-1e3 <= sp <= centro_db[chrn]+1e3 or centro_db[chrn]-1e3 <= ep <= centro_db[chrn]+1e3 or sp <= centro_db[chrn] <= ep:
        continue
    bed_list.append([chrn, sp, ep, random.random()])

plt.subplot(223)
bp.chromosome(chr_len_db, bed_data=bed_list, centro_db=centro_db, orientation='horizontal', cmap='Blues')
plt.subplot(224)
bp.chromosome(chr_len_db, bed_data=bed_list, centro_db=centro_db, orientation='vertical', cmap='Greens')

plt.show()

