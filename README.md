# Distance measurement

This is a simple distance measurement project using a ESPCAM and Arduino IDE.

## Ball Tracking

This project uses OpenCV to track ball movement and measure the distance. The process for tracking is as follows:

* Convert color to HSV
* Create a pixel mask to identify the ball using upper and lower color bounds
* Erode and dilate the mask to reduce noise
* Indentify contours and draw a circle around the ball

## Prerequisites

* [Python 3](https://www.python.org/)
* [OpenCV](http://opencv.org/)
* [Arduino IDE](https://www.arduino.cc/en/Main/Software)
* [ESPCAM](https://www.amazon.com/gp/product/B07Q1QZQZQ/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)

## Setup

### Script

To install the python libraries run this command:

```sh
python3 -m pip install -r requirements.txt
or
pip3 install -r requirements.txt
```

### Arduino IDE

In order to install the ESPCAM library, you need to add the following URL to the Arduino IDE:
http://arduino.esp8266.com/stable/package_esp8266com_index.json

## Getting Started

Run the ball tracking script:

```sh
python3 main.py --video name_of_the_video.mp4
```
