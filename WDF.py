# WDF Equalizer
#
# Script written by David Ross
#
# Paper:
# Parametrically Tunable Audio Shelving And Equalizing Ladder Wave Digital Filters
# Salina Abdul Samad
#

import math
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

def decibels_to_ratio(x):
    y = math.pow(10.0, x/20.0);
    print("dB: %f" %x);
    print("ratio: %f\n" %y);
    return y;

fs = 44100.0;                   # sample rate
f0 = fs/4;                      # center frequency
w0 = 2.0 * math.pi * f0 / fs;   # center frequency digital

#fL = f0 - (f0 / 24.0);          # left band edge
#fH = f0 + (f0 / 24.0);          # right band edge
#wL = 2.0 * math.pi * fL / fs;   # left band digital
#wH = 2.0 * math.pi * fH / fs;   # right band digital
#w3db = wH - wL;                 # band width

Q = 6               # Q factor
w3db = w0 / Q;      # bandwith

m1 = math.tan(w3db/2) / (math.tan(w3db/2) + 1.0);   # m1 intermediate variable
w2 = math.pow(math.tan(w0/2), 2.0);                 # 
m2 = (1.0 - w2) / (1.0 + w2);                       # m2 intermediate variable

dB = 6;                         # decibel level
Gn = decibels_to_ratio(dB);     # convert decibel level to ratio, as per paper

b0 = 1.0 + ((Gn - 1.0) * m1);   # b0 coefficient
b1 = 2.0 * m2 * (m1 - 1.0);     # b1 coefficient
b2 = 1.0 - (m1 * (1.0 + Gn));   # b2 coefficient

a0 = 1.0;                       # a0 coefficient
a1 = b1;                        # a1 coefficient
a2 = 1.0 - (2.0 * m1);          # a2 coefficient

print("%f" %b0)
print("%f" %b1)
print("%f\n" %b2)
print("%f" %a0)
print("%f" %a1)
print("%f\n" %a2)

b = [b0, b1, b2];
a = [a0, a1, a2];

w, h = scipy.signal.freqz(b, a)                     # frequency response

fig, ax = plt.subplots(2, 1, figsize=(8, 6))        # plot
ax[0].plot(w, 20*np.log10(abs(h)), color='blue')
ax[0].set_title("Frequency Response")
ax[0].set_ylabel("Amplitude (dB)", color='blue')
ax[0].set_xlim(0, np.pi)
ax[0].set_ylim([-12, 12])
ax[0].grid()

ax[1].plot(w, np.unwrap(np.angle(h)), color='green')
ax[1].set_ylabel("Angle (degrees)", color='green')
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_xlim(0, np.pi)
ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
ax[1].set_ylim([-90, 90])
ax[1].grid()

plt.show()
