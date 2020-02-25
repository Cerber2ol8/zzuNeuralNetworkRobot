import numpy as np
import glob

npz = glob.glob('./training_images/*.npz')[0]
print(npz)
data = np.load(npz, allow_pickle=True)
labels = data.f.train_labels.tolist()
#print(labels)
def delRepeat(data):
	last_frame = 0
	new_data = []
	for i in range(len(labels)):
		frame = data[i][3]
		if frame != last_frame:
			new_data.append(data[i])
		last_frame = frame
	return new_data

print('')
_labels = len(labels)
labels = delRepeat(labels)
print('')
label_array = np.array(labels)
print(label_array)
print('一共有{}个标签'.format(_labels))
print('处理结束,保留了{}个标签'.format(len(labels)))
np.savez(npz, train_labels=label_array)
