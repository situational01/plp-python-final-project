import requests

# Function to get current weather data
def get_current_weather(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']

        # Extracting relevant data
        temperature = main['temp']
        humidity = main['humidity']
        description = weather['description']
        wind_speed = wind['speed']
        return temperature, humidity, description, wind_speed
    else:
        return None

# Function to get weather forecast (for 5 days)
def get_weather_forecast(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == '200':
        forecast = []
        for item in data['list']:
            forecast.append({
                'date': item['dt_txt'],
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description']
            })
        return forecast
    else:
        return None

import matplotlib.pyplot as plt

# Function to plot the forecast
def plot_weather_forecast(forecast):
    dates = [entry['date'] for entry in forecast]
    temperatures = [entry['temperature'] for entry in forecast]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('5-Day Weather Forecast')
    plt.tight_layout()
    plt.show()

# Example usage:
forecast = get_weather_forecast("London", "your_api_key")
plot_weather_forecast(forecast)


import tkinter as tk
from tkinter import messagebox

def show_weather():
    city = city_entry.get()
    api_key = "your_api_key"
    
    # Get current weather
    weather_data = get_current_weather(city, api_key)
    if weather_data:
        temperature, humidity, description, wind_speed = weather_data
        result_label.config(text=f"Temperature: {temperature}°C\nHumidity: {humidity}%\nDescription: {description}\nWind Speed: {wind_speed} m/s")
    else:
        messagebox.showerror("Error", "City not found")

# GUI setup
root = tk.Tk()
root.title("Weather Application")

tk.Label(root, text="Enter City:").pack()
city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=show_weather)
get_weather_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
