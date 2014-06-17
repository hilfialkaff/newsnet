import numpy as np
import sys

drill_down = []
roll_up = []
similarity = []
fname = sys.argv[1]

def parse():
    with open(fname) as f:
        for line in f:
            if "drill-down" in line:
                drill_down.append(float(line.split()[-1]))
            elif "roll-up" in line:
                roll_up.append(float(line.split()[-1]))
            elif "similarity" in line:
                similarity.append(float(line.split()[-1]))

def main():
    parse()

    if len(drill_down):
        print "Avg drill down:", np.average(drill_down), np.std(drill_down)

    if len(roll_up):
        print "Avg roll_up:", np.average(roll_up), np.std(roll_up)

    if len(similarity):
        print "Avg similarity:", np.average(similarity), np.std(similarity)

if __name__ == '__main__':
    main()
