powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
set Path=C:\Users\sunny\.local\bin;%Path%
uv init removebg
cd removebg
uv venv
uv pip install opencv-python pillow numpy
