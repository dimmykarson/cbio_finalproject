import os, csv
import matplotlib.pyplot as plt
script_dir = os.path.dirname(__file__)


def clear():
    plt.clf()
    plt.cla()
    plt.close()
    plt.yscale('log')


clear()

rel_path = "better_config_ag.txt"
abs_file_path = os.path.join(script_dir, rel_path)
file = open(abs_file_path, "r")
reader = csv.reader(file, delimiter=";")
plt.yscale('log')
times_ag = []
for i in reader:
    v_ant_x = []
    v_ant_y = []
    sl = i[1:]
    for x in range(len(sl)):
        try:
            if x%2==0:
                v_ant_x.append(int(sl[x]))
            else:
                v_ant_y.append(float(sl[x]))
        except:
            continue
    times_ag.append(float(i[0]))
    l2, = plt.plot(v_ant_x, v_ant_y, 'r', label='GA', alpha=0.5)




rel_path = "better_config_ant.txt"
abs_file_path = os.path.join(script_dir, rel_path)
file = open(abs_file_path, "r")
reader = csv.reader(file, delimiter=";")
times_ant = []
for i in reader:
    v_ant_x = []
    v_ant_y = []
    sl = i[1:]
    for x in range(len(sl)):
        try:
            if x%2==0:
                v_ant_x.append(int(sl[x]))
            else:
                v_ant_y.append(float(sl[x]))
        except:
            continue
    times_ant.append(float(i[0]))
    l1, = plt.plot(v_ant_x, v_ant_y, 'b', label='ANT')


plt.legend(handles=[l1, l2])
plt.savefig("comparation.png")
plt.show()



clear()

l1, plt.plot(times_ant, label="ANT")
l2, = plt.plot(times_ag, label="AG")
plt.show()




