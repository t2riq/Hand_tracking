# 🤖 Hand Gesture Control System using Python & OpenCV

This repository contains a set of real-time computer vision projects developed to control various hardware components and computer functions using hand gestures. The system utilizes **MediaPipe** for hand tracking, **OpenCV** for image processing, and **Python** to process logic and connect to hardware like Raspberry Pi GPIO or system libraries. This work was developed during a summer training course at **Near East University (NEU)** under the supervision of **Prof. Dr. Fadi Al-Turjman**.

---

## 📁 Project Files Overview

### `hand_tracking_bulb.py`
**Controls a 220-240V bulb** using gestures:
- Open hand = Turn ON
- Closed fist = Turn OFF
- Uses a relay module connected to Raspberry Pi GPIO pins

### `hand_tracking_led.py`
**Controls 5V LEDs** based on the number of fingers raised:
- 0 to 5 fingers = Adjusts LED count/pattern
- Connects through GPIO pins for physical LED control

### `hand_tracking_vol.py`
**Controls system volume** using vertical distance between thumb and index finger:
- Smaller distance = Lower volume
- Larger distance = Higher volume
- Designed for Linux-based systems using `alsaaudio`

### `v_mouse.py`
**Virtual mouse control** using hand movement:
- Index finger moves cursor
- Pinch gesture simulates click
- Requires `pyautogui` installed

---

## 🛠 Requirements

Install these libraries before running:

```bash
pip install opencv-python mediapipe numpy pyautogui
```
Optional for volume control on Linux:
```
pip install pyalsaaudio
```
Make sure to enable your webcam and, if using GPIO, run on Raspberry Pi with:
```
sudo pip install RPi.GPIO
```

---
## 🧠 Technologies Used

- **Python 3.x** – Core development language  
- **OpenCV** – Image processing and camera frame capture  
- **MediaPipe** – Real-time hand landmark detection  
- **RPi.GPIO** – For controlling GPIO pins (LEDs, relay)  
- **pyautogui** – Mouse control  
- **alsaaudio** – Volume control (Linux)  
- **Thonny IDE** – Development environment for Raspberry Pi Pico  

---

## 🔌 Hardware Setup (For `bulb.py` and `led.py`)

- Raspberry Pi (any model)  
- Relay Module (for controlling 220-240V AC bulb)  
- 5V LEDs and 220Ω resistors  
- Breadboard and jumper wires  
- USB webcam or Raspberry Pi camera module  
- External 220-240V light bulb  

> ⚠️ **Warning:** Use extreme caution when working with 220V AC circuits. Always test with supervision and proper isolation when using relays to avoid electrical hazards.

---

## 📌 Author

Developed by **[Tariq fahed]**  
Summer Training Student – **Near East University (NEU)**  
Supervised by **Prof. Dr. Fadi Al-Turjman**  
AI and Computer Vision Department, Faculty of Engineering  

---

## 📝 License

This project is licensed under the **MIT License**.  
You are free to use, distribute, and modify this software with attribution.

