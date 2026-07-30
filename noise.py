from GTC import ureal, sqrt
from matplotlib import pyplot as plt

def amp_noise(r1, u0, u1):
    # input noise of preamp
    k = 1.380649e-23
    temp = 293.15
    cur_in = 1e-15*0.00001  # add current noise which goes linearly with resistance
    # er = sqrt(4 * k * temp * r1 + cur_in * r1)  # calculate the noise from r1
    er = sqrt(4 * k * temp * r1)  # calculate the noise from r1
    u1_u0 = 10**((u1 - u0)/20)  # linear, not log, ratio of u2/u1
    # u1_u0 = (u1**10)/(u0**10)
    print(u1_u0)
    en = sqrt(er**2 /(u1_u0**2 - 1))  # calculate input noise
    # en = sqrt(er ** 2 * (-u1_u0 ** 2 + 1))  # calculate input noise
    return(en)


uu0 = ureal(-100.1199, 2)
rr = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1001, 2001, 3001, 4001, 5001, 6001, 7001, 8001, 9001, 10001, 10002, 20002, 30002, 40002, 50002, 60002, 70002, 80002, 90002, 100002, 111110]
urr = [-99.3763, -96.9213, -96.8094, -93.9569, -94.3455, -92.7408, -91.4785, -91.3232, -89.9267, -89.1748, -89.9722, -85.2703, -80.6657, -77.8231, -76.2719, -75.4423, -75.9284, -72.3571, -73.2402, -70.3327, -70.9769, -63.3641, -60.3595, -59.446, -58.4852, -58.3181, -57.8915, -58.0031, -57.1308, -58.1394, -57.9621]
ur = []
for x in urr:
    ur.append(ureal(x, 0.5))

een = []
for i in range(len(rr)):
    calc = amp_noise(rr[i], uu0, ur[i])
    een.append(calc)
en_plt =[]
en_err =[]
for x in een:
    en_plt.append(x.x)
    en_err.append(x.u)
    print(repr(x))

name = 'noise'
fig, axs = plt.subplots(1, 1, layout='constrained')
fig.suptitle(name, fontsize=12)
axs.errorbar(rr, en_plt, yerr=en_err, fmt='o', capsize=2, markersize=3)
plt.xscale("log")
# plt.plot(rr, en_plt)
plt.show()