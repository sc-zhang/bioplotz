import bioplotz as bp
import random
import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10), dpi=100)

# DEMO for manhattan plot
data = {
    "Chr%02d"
    % (_ + 1): [
        [random.randint(int(0), int(2e6)) for _ in range(int(1e4))],
        [random.random() for _ in range(int(1e4))],
    ]
    for _ in range(16)
}
plt.subplot(231)
mh = bp.manhattan(
    data,
    threshold=[0.01, 0.05],
    threshold_line_color=["red", "blue"],
    log_base=10,
    reverse=True,
)
plt.xticks(rotation=-45, fontsize=15)
plt.ylabel("-log10(p)", fontsize=15)

# DEMO for gene cluster
gene_list = []
offset = 0
for _ in range(20):
    gn = "Gene%0d" % (_ + 1)
    sp = offset + random.randint(int(1e3), int(5e4))
    ep = sp + random.randint(int(5e3), int(5e4))
    direct = "+" if random.random() >= 0.5 else "-"
    color = "green" if direct == "+" else "orange"
    gene_list.append([gn, sp, ep, direct, color])
    offset = ep
plt.subplot(232)
gcp = bp.genecluster(gene_list)
plt.xticks(fontsize=15)

# DEMO for chromosome plot
chr_len_db = {
    "Chr%02d" % (_ + 1): random.randint(int(1.6e6), int(2e6)) for _ in range(16)
}
centro_db = {"Chr%02d" % (_ + 1): random.randint(int(6e5), int(1e6)) for _ in range(16)}
inner_data = []
outer_data = []
outer_data2 = []
for i in range(1000):
    chrn = "Chr%02d" % (random.randint(1, 16))
    sp = random.randint(0, int(chr_len_db[chrn]))
    ep = sp + random.randint(int(1e3), int(1e4))
    if ep >= chr_len_db[chrn] - 1e3:
        continue
    if (
            centro_db[chrn] - 1e3 <= sp <= centro_db[chrn] + 1e3
            or centro_db[chrn] - 1e3 <= ep <= centro_db[chrn] + 1e3
            or sp <= centro_db[chrn] <= ep
    ):
        continue
    inner_data.append([chrn, sp, ep, random.random()])
    outer_data2.append([chrn, sp, ep, "*", "red"])

for i in range(10000):
    chrn = "Chr%02d" % (random.randint(1, 16))
    sp = random.randint(0, int(chr_len_db[chrn]))
    ep = sp + random.randint(int(1e3), int(1e4))
    if ep >= chr_len_db[chrn] - 1e3:
        continue
    if (
            centro_db[chrn] - 1e3 <= sp <= centro_db[chrn] + 1e3
            or centro_db[chrn] - 1e3 <= ep <= centro_db[chrn] + 1e3
            or sp <= centro_db[chrn] <= ep
    ):
        continue
    outer_data.append([chrn, sp, ep, random.random()])

plt.subplot(233)
bp.chromosome(
    chr_len_db,
    inner_data=inner_data,
    outer_data=outer_data2,
    outer_value_type="marker",
    centro_db=centro_db,
    orientation="horizontal",
    cmap="Blues",
    outer_size=20,
)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.subplot(234)
bp.chromosome(
    chr_len_db,
    inner_data=inner_data,
    outer_data=outer_data,
    centro_db=centro_db,
    orientation="vertical",
    outer_line_color="orange",
    cmap="Greens",
    outer_line_style="-",
    outer_size=1,
)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.subplot(235)
base = ["A", "T", "G", "C", "-"]
base_seq = ""
for i in range(100):
    base_seq += base[random.randint(0, 3)]

aln_db = {}
for i in range(3):
    gid = "Gene%02d" % (i + 1)
    cur_seq = list(base_seq)
    for j in range(random.randint(0, 20)):
        cur_seq[random.randint(0, 99)] = base[random.randint(0, 4)]
    aln_db[gid] = "".join(cur_seq)

plt.rcParams['font.sans-serif'] = 'Courier New'
bp.multialign(aln_db)

plt.show()
