import cv2
import numpy as np
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_white_bg(input_path):
    """去除白色背景并保存为同目录的 _rbg 文件"""
    img = cv2.imread(input_path)
    if img is None:
        return False, "无法读取文件"

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # 白色范围，可微调
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 40, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)
    mask_inv = cv2.bitwise_not(mask)

    # 应用掩膜
    result = cv2.bitwise_and(img, img, mask=mask_inv)

    # 转为RGBA并添加透明通道
    rgba = cv2.cvtColor(result, cv2.COLOR_RGB2RGBA)
    rgba[:, :, 3] = mask_inv

    # 输出文件路径（同名 + _rbg）
    folder, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(folder, f"{name}_rbg{ext}")

    # 按原扩展名保存
    Image.fromarray(rgba).save(output_path)
    return True, output_path


def select_files():
    """选择文件并处理"""
    file_paths = filedialog.askopenfilenames(
        title="选择要处理的图片",
        filetypes=[("图片文件", "*.jpg;*.jpeg;*.png"), ("所有文件", "*.*")]
    )
    if not file_paths:
        return

    count = 0
    for path in file_paths:
        ok, msg = remove_white_bg(path)
        if ok:
            count += 1
            status_label.config(text=f"✅ 已处理：{os.path.basename(msg)}")
            root.update_idletasks()
        else:
            status_label.config(text=f"⚠️ {os.path.basename(path)} 处理失败")
            root.update_idletasks()

    messagebox.showinfo("完成", f"已成功处理 {count} 张图片！")
    status_label.config(text="🎉 全部处理完成！")


# ---------------- GUI ----------------
root = tk.Tk()
root.title("去白底图片工具")
root.geometry("400x220")
root.resizable(False, False)

title_label = tk.Label(root, text="🪄 去白色背景工具", font=("Microsoft YaHei", 14, "bold"))
title_label.pack(pady=15)

desc_label = tk.Label(
    root,
    text="选择一个或多个图片文件，将在同目录生成\n同名文件 + '_rbg' 后缀版本",
    font=("Microsoft YaHei", 10),
    justify="center"
)
desc_label.pack(pady=5)

btn_select = tk.Button(root, text="选择图片文件", font=("Microsoft YaHei", 11), command=select_files)
btn_select.pack(pady=15)

status_label = tk.Label(root, text="等待选择文件...", font=("Microsoft YaHei", 9))
status_label.pack(pady=10)

root.mainloop()
