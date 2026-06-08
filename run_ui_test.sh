#!/bin/bash
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
XVFB_PID=$!
sleep 2

cd Asta
python src/asta/interfaces/native_ui/holographic_pet.py &
APP_PID=$!
sleep 5

python -c "import pyautogui; pyautogui.screenshot('hologram_ui_test.png')"

kill $APP_PID
kill $XVFB_PID
