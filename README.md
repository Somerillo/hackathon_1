# Python Fitness Tracker

A Python fitness tracker that provides weather information and stores user session data in the `sessions` table for future data analysis.

## How to Run It

1. Run `main.py` in the console.
2. When prompted for the user email, you can input:
   - `random` (for testing purposes)
   - An existing email from the list
   - `q` to quit

3. A random city will be chosen, and its weather information will be displayed. The city is chosen randomly because there is no `geolocator` feature implemented in the code. 

4. After the weather information is presented, you can input any string or simply press the ENTER key. A (very) rudimentary session dashboard will be displayed. After closing the dashboard, all obtained data will be stored in the `sessions` table.

## Features

- **user_generator.py**: Generates random user personal data (using the `Faker` module) and random biometric data (using the `random` module) within human ranges. It then exports this data (using the `psycopg2` module) to the `users` table in the database. This feature is standalone and runs at the beginning to generate the `users` table.

- **weather_api.py**: Retrieves data from a JSON file provided by the Open Weather API. The inputs are the city code and the current datetime (using the `datetime` module). It returns weather statistics (temperature, humidity, status) at that moment.

- **mock_tracker.py**: Generates random sport session data (steps, blood pressure, etc.) using the `random` module.

- **session_manager.py**: Calls the mock tracker and simulates 60 cycles with a time step of 0.01 seconds. The cycle limit simulates the "start-stop sport session button" on a fitness band. The time step is set to 0.01 seconds instead of 1 minute or more for testing purposes. It prints a biometrics dashboard (pyplot module) of the session and returns the biometric statistics.

- **main.py**: This is the main feature that runs all components (except for the user generator). After verifying that the user exists in the database, it displays the weather and initiates a sport session. The data is displayed on a dashboard and exported to the `sessions` table.

## Required Modules

To run this project, you need to install the following Python modules:

```python
from pyowm import OWM
import random
import psycopg2
from faker import Faker
from datetime import datetime
import pandas as pd
import time
from matplotlib import pyplot
