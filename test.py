import pydicom
import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use('ggplot')

df = pydicom.read_file("tes1.dcm")

a = df.ROIContourSequence[1].ContourSequence[0].ContourData
b = df.ROIContourSequence[1].ContourSequence[1].ContourData
fig, axes = plt.subplots(2)
axes[0].plot(a, label='legend label')
axes[1].plot(b, label='legend label')
plt.show()