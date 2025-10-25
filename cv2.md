
## 🔧 参数微调

如果你的白底不是纯白，可稍微放宽阈值：

```python
lower_white = np.array([0, 0, 180])
upper_white = np.array([180, 60, 255])
```

这样可以去掉浅灰或微黄背景。

---

是否希望我帮你加个选项（如“容忍度滑块”）让你在 GUI 里实时调节白色阈值？
→ 这样可以适应不同照片亮度，无需改代码。


当我们用 HSV 阈值去掉白背景时，如果**同时模糊了 alpha 通道（透明度）**，黑线边缘就会显得发灰、模糊、发虚。

你想要的效果是：
✅ 去掉白色背景
❌ 保留黑线的锐利边缘

---

## 🧠 造成模糊的原因

在你的脚本里，有这句：

```python
rgba[:, :, 3] = cv2.GaussianBlur(mask_inv, (3, 3), 0)
```

这会**模糊 alpha 通道**（透明度层），导致黑线边缘半透明 → 看起来灰灰的、糊掉。

---

## ✅ 解决方案

直接 **去掉或改成更“硬”的边缘处理**：

### ✅ 修改版（推荐）：

```python
# 不模糊 alpha 通道，保持锐利边缘
rgba[:, :, 3] = mask_inv
```

如果你仍想稍微柔化（避免锯齿），可以换成 **轻微腐蚀再膨胀**：

```python
kernel = np.ones((2, 2), np.uint8)
mask_inv = cv2.erode(mask_inv, kernel, iterations=1)
mask_inv = cv2.dilate(mask_inv, kernel, iterations=1)
rgba[:, :, 3] = mask_inv
```

---

## 🔍 可选优化：改善黑线锐度

你还可以在生成最终图像前，对 RGB 通道轻微增强对比度：

```python
img = cv2.convertScaleAbs(img, alpha=1.1, beta=0)  # alpha>1 提高对比
```

这能让线稿或黑色线条更清晰。

---

## ✨ 最终修改版核心片段：

替换你原脚本中的这一段👇：

```python
mask_inv = cv2.bitwise_not(mask)
result = cv2.bitwise_and(img, img, mask=mask_inv)

rgba = cv2.cvtColor(result, cv2.COLOR_RGB2RGBA)
rgba[:, :, 3] = cv2.GaussianBlur(mask_inv, (3, 3), 0)
```

改成这样👇：

```python
mask_inv = cv2.bitwise_not(mask)
result = cv2.bitwise_and(img, img, mask=mask_inv)

# 保留清晰边缘
rgba = cv2.cvtColor(result, cv2.COLOR_RGB2RGBA)
rgba[:, :, 3] = mask_inv
```

---

## 💡 可选增强（对扫描稿或手绘线条特别有效）

如果你的图像是黑白稿或线稿：

```python
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# 自动增强黑线对比
gray = cv2.equalizeHist(gray)
# 再合成回彩色图
img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
```

---

是否希望我帮你改成一个“**线稿优化版 GUI 工具**”，
自动去白底 + 保留锐利黑线 + 可调“线条增强强度”？
