#!/bin/bash

# OmniScan-XR Backend Initialization for Pixel 9a / Android 16



echo "--- 🛰️ INITIALIZING OMNISCAN BACKEND FOR ANDROID ---"



# 1. Update Termux pasckagesckagesckagesckagesckagesckagesckesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckagesckages and install Python

pkg update -y

pkg install python -y

pkg install build-essential libcrypt -y

pkg install clang -y



# 2. Setup virtual environment to prevent package conflicts

python -m venv venv

source venv/bin/activate



# 3. Install core numerical and network libraries

pip install --upgrade pip

pip install numpy flask python-dotenv requests



echo "✅ Environment configured. Ready to run fusion_core.py."


Use reverse proxy:

NGINX → FastAPI
HTTPS → HTTP (internal)

sudo apt update
sudo apt install python3-pip
pip install fastapi uvicorn opencv-python
python main.py


