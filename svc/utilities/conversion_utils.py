def convert_to_imperial(distance, is_imperial):
    if is_imperial:
        return distance / 2.54
    return distance


def convert_to_fahrenheit(celsius_temp):
    return celsius_temp * 1.8 + 32


def convert_to_celsius(fahrenheit_temp):
    return round((fahrenheit_temp - 32) / 1.8, 2)
