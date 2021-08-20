import math
import matplotlib.pyplot as plt


def nCr(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n - r)

#number of steps
nSteps = 99

x = list(range(-nSteps,nSteps+1))
p = [0.0]*(2*nSteps+1)
div = 2**nSteps

if nSteps%2==0:
    for i in range(2*nSteps+1):
        if x[i]%2==0:
            p[i] = nCr(nSteps, nSteps/2-x[i]/2)/div
else:
    for i in range(2*nSteps+1):
        if x[i]%2==1:
            p[i] = nCr(nSteps, nSteps/2-x[i]/2)/div

plt.bar(x,p)
plt.show()