import cv2
import numpy as np
from PIL import Image

# 读取图片
img = cv2.imread('1.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 转换到 HSV 空间（更适合颜色分割）
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

# 设定背景颜色范围（这里假设是白色背景）
lower = np.array([0, 0, 200])
upper = np.array([180, 25, 255])

# 创建掩膜并反转
mask = cv2.inRange(hsv, lower, upper)
mask_inv = cv2.bitwise_not(mask)

# 应用掩膜
result = cv2.bitwise_and(img, img, mask=mask_inv)

# 转换为带透明通道的 RGBA
rgba = cv2.cvtColor(result, cv2.COLOR_RGB2RGBA)
rgba[:, :, 3] = mask_inv

Image.fromarray(rgba).save('output.png')
