from app import logging

def fahrenheit_to_celsius(fahrenheit: float):
    """
    Converts Fahrenheit to Celsius; returns Celsius if the conversion is successful, otherwise returns the original Fahrenheit value.
    """
    try:
        celsius = round((fahrenheit - 32) * 5 / 9, 2)
        logging.info(f"Converted {fahrenheit}F to {celsius}C")
        return celsius
    except Exception as e:
        logging.info(f"Unexpected error in converting Fahrenheit to Celsius: {e}")
        return fahrenheit