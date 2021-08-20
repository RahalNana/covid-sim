import numpy as np
import csv

# number of samples per day and number of days
nSamples = 12
nDays = 7


def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# loads list of locations and coordinates
with open('nodes.csv', newline='') as f:
    reader = csv.reader(f)
    data = np.array(list(reader))
locs = data[:, 0:2].astype(np.float)
locNames = data[:, 2]

# number of locations
nLocs = len(locNames)


def getLoc(pos):
    minDist = 9999999999999999
    minPos = 0
    for i in range(len(locs)):
        if dist(pos, locs[i]) < minDist:
            minDist = dist(pos, locs[i])
            minPos = i
    return minPos


# read location data into posData array
posData = np.zeros([nDays, nSamples, 2])
for i in range(nDays):
    with open('day' + str(i + 1) + '.csv', newline='') as f:
        reader = csv.reader(f)
        posData[i] = np.array(list(reader))

locData = np.zeros([nDays, nSamples], dtype=np.int)

for i in range(nDays):
    for j in range(nSamples):
        locData[i, j] = getLoc(posData[i, j])

# construct markov matrix
m = np.zeros([nLocs, nLocs])
for i in range(nDays):
    for j in range(nSamples - 1):
        m[locData[i, j + 1], locData[i, j]] += 1
mSum = m.sum(axis=0)
m = m / mSum

w, v = np.linalg.eig(m)
for i in range(nLocs):
    if np.round(w[i], decimals=5) == 1:
        stable = np.reshape(v[:, i], (nLocs, 1))

if stable[0] < 0:
    stable *= -1

print(m)
print()
print(stable)
