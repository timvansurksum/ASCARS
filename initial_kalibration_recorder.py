import sounddevice as sd
from Sound_Manager import Sound_Manager
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

devices = Sound_Manager.set_Audio_Devices()
sd.default.device = devices['record_device_name']
recording =  sd.rec(4 * 44100, samplerate=44100, channels=1, dtype='float64')
sd.wait()
time_data = np.linspace(0,4,4*44100)
get_Min = lambda sound_sample: float(sound_sample[0])

recording = list(map(get_Min, recording))

plt.plot(time_data, recording)
plt.show()
d = {'recording': recording, 'time_data': time_data}
df = pd.DataFrame(data=d)
df.to_csv('data.csv', sep=',', encoding='utf-8', index=False)