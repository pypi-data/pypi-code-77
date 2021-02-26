""" Implements support for CX Controller Hardware features

Copyright (C) Nanosurf AG - All Rights Reserved (2021)
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
https://www.nanosurf.com
"""

import nanosurf.spmcontroller as spmcontroller
import matplotlib.pyplot as plt

# connect to running application
spm = spmcontroller.connect()

# write a dc level to an output
tipdac = spm.get_dac(spmcontroller.Converter.HiResOut_TIPVOLTAGE)
tipdac.dc = 5

# reading an analog input
userin = spm.get_adc(spmcontroller.Converter.HiResIn_USER1)
print(f"User input: {userin.dc:g}{userin.unit}")

# capture some data and plot
capture = spm.get_data_capture(spmcontroller.Module.CaptureHiRes)
capture.channels = ['InUser1', 'InUser2']
capture.samples = 10000
capture.measure()

print(f"Sample rate ={capture.sample_rate}Hz")
for ch in capture.channels:
    plt.plot(capture.timeline, capture.data[ch], label=f"{ch}, range={capture.data_max[ch]}, unit={capture.data_unit[ch]}")
plt.legend()