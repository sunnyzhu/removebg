from rembg import remove
from PIL import Image

# 打开图片
input_path = "1.png"
output_path = "output.png"

input_image = Image.open(input_path)
output_image = remove(input_image)

# 保存去背景后的图片（自动变透明）
output_image.save(output_path)
