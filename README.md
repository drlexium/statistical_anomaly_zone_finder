Project: Statistical Anomaly Zone Detector
Project Description
This project is a statistical anomaly zone detector using Raspberry Pi Pico. The main task of the device is to analyze data, generate random numbers, calculate the arithmetic mean, and visualize the results on an LCD screen. The project includes:

Generating random numbers and filling a data array.

Calculating the arithmetic mean and detecting anomalies.

Visualizing data on the LCD screen using custom characters.

Indicating the device status using an addressable RGB LED (WS2812).

The device can be used for educational purposes, data processing experiments, and visualizing statistical anomalies.

Components
Raspberry Pi Pico – microcontroller for running the program.

Addressable RGB LED (WS2812) – for indicating the device status.

LCD screen (16x2, I2C) – for displaying information.

Button – for resetting the data array.

Resistors and wires – for connecting components.

Component Connections
RGB LED (WS2812)
DIN pin – connect to GPIO23 (Pin 29) on Raspberry Pi Pico.

GND – connect to GND on Raspberry Pi Pico.

VCC – connect to 3.3V on Raspberry Pi Pico.

LCD Screen (I2C)
SDA – connect to GPIO0 (Pin 1) on Raspberry Pi Pico.

SCL – connect to GPIO1 (Pin 2) on Raspberry Pi Pico.

VCC – connect to 3.3V on Raspberry Pi Pico.

GND – connect to GND on Raspberry Pi Pico.

Button
One button pin – connect to GPIO15 (Pin 20) on Raspberry Pi Pico.

The other button pin – connect to GND on Raspberry Pi Pico.

Use a pull-up resistor (internal PULL_UP).

Installation and Launch
Ensure you have the latest version of MicroPython installed on your Raspberry Pi Pico.

Copy the project files (including the libraries lcd_api.py and i2c_lcd.py) to the Raspberry Pi Pico.

Connect the components according to the diagram.

Run the main.py file on the Raspberry Pi Pico.

Program Functionality
Initialization:

On startup, the LED lights up blue, and the LCD screen displays "Initializing...".

After initialization, the LED changes to green, and a scale with the message "Wait" appears on the screen.

Data Generation:

The program generates random numbers and fills an array with them.

After filling the array, the arithmetic mean is calculated, and the position of the rectangle (cursor) corresponding to this value is displayed on the LCD screen.

Anomaly Detection:

Under normal conditions, the cursor oscillates around the center of the screen, not exceeding one segment to the left or right.

If the cursor deviates from the central zone by 3-4 segments, this indicates a statistical anomaly.

Anomalies are visualized only on the LCD screen using the cursor position.

LED Indicator:

Blue color – device initialization.

Yellow color – issues with the LCD screen (e.g., no connection).

Purple color – initial data array filling.

Green color – the device is ready for operation.

Array Reset:

When the button is pressed, the data array is reset, the LED changes to purple, and the scale with the message "Wait" reappears on the screen.

Custom Characters:

Custom characters are used on the LCD screen to display the scale and cursor.

Customization
Changing the array size: To analyze more or fewer data points, modify the array_size variable.

Setting the anomaly threshold: You can adjust the logic for detecting anomalies by modifying the value range in the code.

Changing the LCD address: If your LCD screen address differs from 0x27, change the I2C_ADDR variable.

Customizing characters: You can modify or add your own characters by editing the arrays in the "Custom Character Creation" section.

Use Cases
Educational project: Learning about PIO, I2C, random number generation, and LCD screens.

Data experiments: Analyzing random data and detecting anomalies.

Prototyping: Rapid prototyping using Raspberry Pi Pico.

License
This project is distributed under the MIT license. You are free to use, modify, and distribute the code.

Author
Project developed by Alex Cube (drLexium).
GitHub page: https://github.com/drlexium/statistical_anomaly_zone_finder

Acknowledgments
MicroPython developers for excellent support for Raspberry Pi Pico.

Raspberry Pi community for inspiration and support.

Links
Official Raspberry Pi Pico website: https://www.raspberrypi.org/products/raspberry-pi-pico/

MicroPython documentation: https://docs.micropython.org/

<<<<<<< HEAD
I2C LCD library: https://github.com/dhylands/python_lcd
=======
I2C LCD library: https://github.com/dhylands/python_lcd
>>>>>>> 3a74bc307db6dc31d11f6aa9c059b8b2a4236c0d
