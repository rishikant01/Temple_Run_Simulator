# 🏃‍♂️ Temple Run Motion Controller 🎮  
**Control Temple Run with your body movements using just your webcam!**  

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green?logo=opencv)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8.9-orange)](https://mediapipe.dev)
[![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)

</div>

![Demo](demo.gif)  
*(Watch the full demo [here](https://youtu.be/your-demo))*

## ✨ Features
- 🟡 **Jump** by raising your head above the yellow line  
- 🔴 **Slide** by lowering below the red line  
- ↔️ **Steer** by leaning left/right  
- 🖱️ **Adjustable** control lines (drag with mouse)  
- 📊 Real-time pose tracking visualization  

## 🛠️ Tech Stack
| Technology | Role |
|------------|------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Core programming language |
| ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?logo=opencv&logoColor=white) | Camera processing & visualization |
| ![MediaPipe](https://img.shields.io/badge/-MediaPipe-4285F4) | Body pose detection |
| ![PyAutoGUI](https://img.shields.io/badge/-PyAutoGUI-306998) | Keyboard input simulation |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam
- Temple Run 2 running in browser ([Poki](https://poki.com/en/g/temple-run-2))

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/temple-run-motion-controller.git
cd temple-run-motion-controller

# Install dependencies
pip install -r requirements.txt

Usage
bash
Copy
python temple_run_controller.py
Game Controls:

Movement	Action	Visual Cue
Head ↑	Jump	Nose crosses yellow line
Head ↓	Slide	Nose crosses red line
Lean ←/→	Steer	Nose moves left/right of center
📸 Screenshots
<div align="center"> <img src="screenshots/control-lines.jpg" width="45%" alt="Control Lines"> <img src="screenshots/jump-detection.jpg" width="45%" alt="Jump Detection"> </div>
🌟 Advanced Features
Customizable sensitivity in config.py

Performance modes for low-end devices

Multiplayer support (experimental)

🤝 Contributing
Pull requests welcome! See CONTRIBUTING.md for guidelines.

📜 License
This project is licensed under the MIT License - see LICENSE file for details.

Made with ❤️ by [Your Name] | Twitter
