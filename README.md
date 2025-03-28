Statistical Anomaly Zone Detector v2.0

Project Description:
Advanced statistical anomaly detection device with extended functionality. The main purpose is data analysis, random number generation, arithmetic mean calculation and results visualization on LCD with full statistical analysis capabilities.

New Features:
- Fullscreen statistics mode (activated by double button press)
- Display of most frequent value range and hit count
- Frequency analysis of last 1600 values
- Data split into 16 ranges of 100 values
- Improved mode indication

Components:
- Raspberry Pi Pico
- WS2812 RGB LED
- 16x2 LCD (I2C)
- Button
- Resistors and wires

Connections:

RGB LED (WS2812):
- DIN -> GPIO23 (Pin 29)
- GND -> GND
- VCC -> 3.3V

LCD (I2C):
- SDA -> GPIO0 (Pin 1)
- SCL -> GPIO1 (Pin 2)
- VCC -> 3.3V
- GND -> GND

Button:
- One pin -> GPIO15 (Pin 20)
- Second pin -> GND
- Use internal PULL_UP resistor

Installation:
1. Install latest MicroPython on Raspberry Pi Pico
2. Copy project files (main.py, lcd_api.py, i2c_lcd.py)
3. Connect components according to scheme
4. Run main.py

Functionality:

Main Mode:
- Random number generation and array filling
- Arithmetic mean calculation
- Cursor position visualization on scale
- Anomaly detection (cursor deviation)
- Color status indication (blue - init, green - ready, purple - filling)

Statistics Mode (double button press):
- Display of most frequent value range
- Show hit count for this range
- Yellow LED indication

Data Reset:
- Single button press resets array
- Returns to main mode

Configuration:
- array_size - analysis array size
- stat_window - statistics window
- stat_bins - number of ranges
- bin_size - single range size

Use Cases:
- Educational statistics projects
- Random number generation experiments
- Analytics systems prototyping

License:
MIT License. Free use, modification and distribution.

Author:
Alex Cube (drLexium)
GitHub: https://github.com/drlexium/statistical_anomaly_zone_finder
