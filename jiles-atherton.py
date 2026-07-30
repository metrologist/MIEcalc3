# from __future__ import division
import numpy as np
from matplotlib import pyplot as plt

mu0 = 4 * np.pi * 1e-7  # H/m
scale = 1  # this is an attempt to get more resolution with smaller H steps, but it seems to change behaviour?
a = 470  # A/m
alpha = 9.38e-4
c = 0.0889
k = 483  # A/m
Ms = 1.48e6  # A/m

# a = a*2
# alpha = alpha*0.5
# c = c*2
Ms = Ms*0.01
k = k*0.6

H = [0]
delta = [0]
Man = [0]
dMirrdH = [0]
Mirr = [0]
M = [0]

DeltaH = 10 / scale  # original 20
Nfirst = 125 * scale
Ndown = 250 * scale
Nup = 250 * scale

for i in range(Nfirst):
    H.append(H[i] + DeltaH)

for i in range(Ndown):
    H.append(H[-1] - DeltaH)

for i in range(Nup):
    H.append(H[-1] + DeltaH)

delta = [0]
for i in range(len(H) - 1):
    if H[i + 1] > H[i]:
        delta.append(1)
    else:
        delta.append(-1)


def L(x):
    """Langevin equation"""
    return (np.cosh(x) / np.sinh(x)) - (1 / x)


for i in range(Nfirst + Ndown + Nup):
    Man.append(Ms * L((H[i + 1] + alpha * M[i]) / a))
    dMirrdH.append((Man[i + 1] - M[i]) / (k * delta[i + 1] - alpha * (Man[i + 1] - M[i])))
    Mirr.append(Mirr[i] + dMirrdH[i + 1] * (H[i + 1] - H[i]))
    M.append(c * Man[i + 1] + (1 - c) * Mirr[i + 1])

print('H1', H)
for x in H:
    print(x)
print('M1', M)
for x in M:
    print(x)

plt.plot(H, M)
## for i in range(Nfirst + 1):
##     print H[i]
##
## for i in range(Nfirst + 1):
##     print M[i]

# repeat for a different loop
DeltaH = 2

H2 = [0]
delta2 = [0]
Man2 = [0]
dMirrdH2 = [0]
Mirr2 = [0]
M2 = [0]
for i in range(Nfirst):
    H2.append(H2[i] + DeltaH)

for i in range(Ndown):
    H2.append(H2[-1] - DeltaH)

for i in range(Nup):
    H2.append(H2[-1] + DeltaH)

for i in range(len(H2) - 1):
    if H2[i + 1] > H2[i]:
        delta2.append(1)
    else:
        delta2.append(-1)

for i in range(Nfirst + Ndown + Nup):
    Man2.append(Ms * L((H2[i + 1] + alpha * M2[i]) / a))
    dMirrdH2.append((Man2[i + 1] - M2[i]) / (k * delta2[i + 1] - alpha * (Man2[i + 1] - M2[i])))
    Mirr2.append(Mirr2[i] + dMirrdH2[i + 1] * (H2[i + 1] - H2[i]))
    M2.append(c * Man2[i + 1] + (1 - c) * Mirr2[i + 1])
# print('H2', H)
# for x in H2:
#     print(x)
# print('M2', M2)
# for x in M2:
#     print(x)
# plt.plot(H2, M2)

# repeat for a different loop
DeltaH = 1

H3 = [0]
delta3 = [0]
Man3 = [0]
dMirrdH3 = [0]
Mirr3 = [0]
M3 = [0]
for i in range(Nfirst):
    H3.append(H3[i] + DeltaH)

for i in range(Ndown):
    H3.append(H3[-1] - DeltaH)

for i in range(Nup):
    H3.append(H3[-1] + DeltaH)

for i in range(len(H3) - 1):
    if H3[i + 1] > H3[i]:
        delta3.append(1)
    else:
        delta3.append(-1)

for i in range(Nfirst + Ndown + Nup):
    Man3.append(Ms * L((H3[i + 1] + alpha * M3[i]) / a))
    dMirrdH3.append((Man3[i + 1] - M3[i]) / (k * delta3[i + 1] - alpha * (Man3[i + 1] - M3[i])))
    Mirr3.append(Mirr3[i] + dMirrdH3[i + 1] * (H3[i + 1] - H3[i]))
    M3.append(c * Man3[i + 1] + (1 - c) * Mirr3[i + 1])

# print('H3', H)
# for x in H3:
#     print(x)
# print('M3', M3)
# for x in M3:
#     print(x)
# plt.plot(H3, M3)

# repeat for a different loop
DeltaH = 5

H4 = [0]
delta4 = [0]
Man4 = [0]
dMirrdH4 = [0]
Mirr4 = [0]
M4 = [0]
for i in range(Nfirst):
    H4.append(H4[i] + DeltaH)

for i in range(Ndown):
    H4.append(H4[-1] - DeltaH)

for i in range(Nup):
    H4.append(H4[-1] + DeltaH)

for i in range(len(H4) - 1):
    if H4[i + 1] > H4[i]:
        delta4.append(1)
    else:
        delta4.append(-1)

for i in range(Nfirst + Ndown + Nup):
    Man4.append(Ms * L((H4[i + 1] + alpha * M4[i]) / a))
    ##     Man4.append(Ms * (1 / np.tanh((H4[i + 1] + alpha * M4[i]) / a) - a / (H4[i + 1] + alpha * M4[i])))
    dMirrdH4.append((Man4[i + 1] - M4[i]) / (k * delta4[i + 1] - alpha * (Man4[i + 1] - M4[i])))
    Mirr4.append(Mirr4[i] + dMirrdH4[i + 1] * (H4[i + 1] - H4[i]))
    M4.append(c * Man4[i + 1] + (1 - c) * Mirr4[i + 1])

# print('H4', H)
# for x in H4:
#     print(x)
# print('M4', M4)
# for x in M4:
#     print(x)
# plt.plot(H4, M4)

plt.grid()
plt.show()