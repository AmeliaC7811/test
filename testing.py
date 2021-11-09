# import gzip

# f = open('train-images.idx3-ubyte', 'rb')

# image_size = 28
# num_images = 5

import numpy as np

# f.read(16)
# buf = f.read(image_size * image_size * num_images)
# data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
# data = data.reshape(num_images, image_size, image_size, 1)
# import matplotlib.pyplot as plt

# image = np.asarray(data[4]).squeeze()
# plt.imshow(image)
# plt.show()
arr = np.arange(0, 30).reshape(2, 3, 5)
print(arr)
