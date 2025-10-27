## 项目创建
```
uv init removebg
cd removebg
uv venv
uv add opencv-python pillow numpy
```

## clone 后安装环境
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
set Path=C:\Users\xxxx\.local\bin;%Path%
cd removebg
uv sync
```
### 如本地python 版本>3.14 需升级 NumPy
```
uv remove numpy
uv add numpy --upgrade
```