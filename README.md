# Telegram Weather Bot

#### Introduction
This is my first Python application, so I apologize in advance if it is not organized. Using the python-telegram-bot open source API and the
Python weather-api wrapper for Yahoo! weather, I created a script for a Telegram bot that allows the bot to text weather data back to you.

#### Usage
* ```/location``` sets the location via latitude and longitude coordinates.
* ```/weather``` gets the date, conditions, high, and low for the current day.
* ```/forecast``` gets the date, conditions, high, and low for the next 5 days.
* ```/time``` sets a daily timer at a specified hour and minute to text you the weather.
* ```/help``` prints out this help information.

#### Installation
It is highly recommended that you use virtualenv to make a virtual environment for this program, so that you do not contaminate your global
Python installation. Instructions can be found by searching online.
This specific bot script was built and tested with Python 3.6.6.

To install dependencies and run the program:
```Python
pip install -r requirements.txt
python app.py
```

On specific systems with Python 2 and 3 installed globally, you may need to use ```pip3``` and ```python3```.

This only provides basic weather functionality, so feel free to modify this app to your liking! 
