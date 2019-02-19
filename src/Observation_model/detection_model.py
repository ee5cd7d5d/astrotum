# =============================================================================
# file detection_model.py
#
# Detection model for TUM current observatory
#
# -----------------------------------------------------------------------------
# Inputs:
# - task 1
Mmax=15     # magnitude of selected object
tmin=0      # min and max exposure time
tmax=300
g=1.4       # GAIN of the camera (to be verified)
            # defined as e-/DN (sometimes computed as Fullwell/res)
#
# - task 2
TEXP = 30.0   # Fixed Exposure time (sec)
minMag=-5   # min and max magnitude range
maxMag=25
#
# -----------------------------------------------------------------------------
# Outputs:
# - Plot 1
# Camera counts for changing exposure time
#
# - Plot 2
# Signal to Noise ration for changing exposure time
#
# - Plot 3
# Camera counts for changing magnitude at fixed exp time
#
# -----------------------------------------------------------------------------
# Author: Barbieri Edoardo, TU Munich
# Date: 19/02/2019
# =============================================================================

# -----------------------------------------------------------------------------
# Import required libraries
# -----------------------------------------------------------------------------
import numpy as np
from numpy import pi as pi
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
Influx_sun= 1367 #watt/m^2
Msun=-27.1 #magnitude of Sun
h=6.62606957e-34 #Js Plank cst.
c=299792458 #m/s

# wavelength in meters
wl_550=550e-9
wl_720=720e-9

# -----------------------------------------------------------------------------
# Telescope SPECS
# -----------------------------------------------------------------------------
D=0.28 #meter
Obstr=0.12 # Secondary mirror obstruction in %
tau=0.8 #throughput, not given in the spec-->we assume a standard value

A= ((D/2.)**2)*pi  #Area primary mirror
Aeff= A-(A*Obstr) #effective area( i.e. A - A obstruction)

# -----------------------------------------------------------------------------
# Camera SPECS
# -----------------------------------------------------------------------------
texp=np.arange(tmin,tmax,0.0001)  # sec - exposure time
# Quantum efficiency for each wavelength
QE_550=0.35
QE_440=0.4
QE_720=0.4

Fullwell=25500
res=(2**16) #Resolution :16 bits
#g= 1.4   # Gain defined as e-/DN (sometimes computed as Fullwell/res)
Ppx=0.4 #typical value ( not from spec.)
Npixel= 3326*2504 #Number of Pixels

# ---------------------------------------------------------
#   Computations of parameters
# ---------------------------------------------------------
# spectral influx for an object with given magnitude at the telescope
Fin = Influx_sun * (10 ** (-(Mmax - Msun) / 2.5))

# compute the influx at the detector
Fdet = Fin * Aeff * tau

# Compute the digital number, assuming average wavelength

coeff_550 = (h * c) / wl_550
coeff_720 = (h * c) / wl_720

# DN per total exposure
DN_550 = texp * Ppx * (1 / g) * (Fdet / coeff_550) * QE_550
DN_720 = texp * Ppx * (1 / g) * (Fdet / coeff_720) * QE_720
# DN rate per sec
DN_550_ps = Ppx * (1 / g) * (Fdet / coeff_550) * QE_550

# ---------------------------------------------------------
# compute DN for changing mag
# --------------------------------------------------------

Mmax_v = np.arange(minMag, maxMag, 0.01)
Fin_v = []
Fdet_v = []
DN_550_v = []

for i in range(0, Mmax_v.__len__()):
    Fin_v.append(Influx_sun * (10 ** (-(Mmax_v[i] - Msun) / 2.5)))
    Fdet_v.append(Fin_v[i] * Aeff * tau)
    DN_550_v.append(TEXP * Ppx * (1 / g) * (Fdet_v[i] / coeff_550) * QE_550)

    if (DN_550_v[i] > 65535):
        DN_550_v[i] = 65535

## Signal to noise ratio for VIS
DNsign = DN_550_ps * texp;

###Sky brightness noise over Munich
SKY = 18.91  ##mag of sky per arc second2 [mag/('')^2]

s = np.arctan(5.6e-6 / 2.8) * (180 / pi) * 3600  # pixel scale- [''/pixel]
R_20_vis = 1521  # e-/pixel
m_pix_vis = SKY - 2.5 * (np.log(s ** 2))  # magnitude per pixel

DNsky = R_20_vis * 10 ** (0.4 * (20 - m_pix_vis)) * QE_550 * texp  # DN of sky background %*Npixel(?)

# Rsky=DN_550_ps * 10^(0.4*(Mmax-m_pix_vis))


##Bias
DNbias = 2010

##Read out noise
ro = 8  # e-
DNro = (ro ** 2) * (g / 2) ** 2  # Npixel(?)

## Dark current
DNdark = 0.003 * texp  # Npixel(?)

###finally compute the SN ratio
SNR_vis = []
totalDN = []

for i in range(0, texp.__len__()):

    if (DNsign[i] > 65535):
        DNsign[i] = 65535

    SNR_vis.append(DNsign[i] / (np.sqrt(DNsign[i] + DNbias + DNro + DNdark[i] + DNsky[i])))
    totalDN.append(DN_550[i] + DNbias + DNro + DNdark[i] + DNsky[i])

# ------------------------------------------
#   PLOTS
# ------------------------------------------

# total DN as function of exp time change for VIS
plt.figure(1)
lin1=plt.plot([t for t in texp], totalDN, label='Digital number')
lin2=plt.plot([t for t in texp], 65535 * np.ones(texp.__len__()),label='Saturation threshold')

plt.legend(loc='lower right') #loc='lower right', [lin1,lin2],['Digital number','Saturation threshold'],['lower right']
plt.xlabel('Exposure time (sec)')
plt.ylabel('Counts number')
plt.grid()
plt.title('Camera counts as function of exposure time for ' + str(Mmax) + ' mag object')
plt.show()

plt.figure(2)
plt.plot(texp, SNR_vis)
plt.xlabel('Exposure time (sec)')
plt.ylabel('SNR')
plt.grid()
plt.title('Signal to Noise Ratio for VIS over Munich for ' + str(Mmax) + ' mag object')
plt.show()

plt.figure(3)
plt.plot(Mmax_v, DN_550_v)
plt.xlabel('Magnitude')
plt.ylabel('Counts number')
plt.grid()
plt.title('DN as function of mag for fixed ' + str(TEXP) + '  sec exposure')
plt.show()
