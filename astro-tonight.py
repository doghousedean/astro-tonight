import requests
from PIL import Image, ImageDraw
import numpy as np
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    return False

def classify_colour(r, g, b):
    if r > 230 and g < 130 and b < 140:  # Red
        return "red"
    elif r > 230 and 130 < g < 200 and b < 140:  # Amber
        return "amber"
    elif r < 150 and g > 200 and b < 150:  # Green
        return "green"
    else:
        return "unknown"

def analyze_summary(image_path, debug_path=None):
    image = Image.open(image_path)
    pixels = np.array(image)

    summary_row = 103
    start_col = 102
    end_col = 670
    step = 16
    
    summary_colours = []
    debug_image = image.copy()
    draw = ImageDraw.Draw(debug_image)

    for col in range(start_col, end_col, step):
        r, g, b = pixels[summary_row, col][:3]
        # Uncomment for debugging
        # print(f"Pixel at {col}: {r}, {g}, {b}")
        colour = classify_colour(r,g,b)
        summary_colours.append(colour)

        # Draw a debug box
        if debug_path:
            box_top_left = (col - 5, summary_row - 5)
            box_bottom_right = (col + 5, summary_row + 5)
            box_colour = (255,0,255)
            draw.rectangle([box_top_left, box_bottom_right], outline=box_colour)

    # Save the debug image if required
    if debug_path:
        debug_image.save(debug_path)

    return summary_colours

def check_evening_conditions(summary_colours):
    return {
        'go': 'yes' if any(summary_colours[i] == 'green' for i in range(0, len(summary_colours))) else 'no',
        'states': summary_colours
    }

def send_notification(good_blocks):
    astro_start_time = block_to_time(good_blocks[0])
    print(f"Good conditions for astronomy on {astro_start_time.strftime("%d %b %Y %H:00:00")}!")

def block_to_time(block):
    current_hour = datetime.now().hour % 2
    blocks_in_hours = block * 2
    start_days = int((current_hour + blocks_in_hours) / 24)
    remaining_hours = (current_hour + blocks_in_hours) % 24
    return datetime.now() + timedelta(hours=remaining_hours, days=start_days) - timedelta(minutes=datetime.now().minute, seconds=datetime.now().second)

# Main script
if __name__ == "__main__":
    LAT = getenv("LAT", 50.7) # Defaults to FLO location
    LON = getenv("LON", -3.52)
    IMAGE_URL = f"https://clearoutside.com/forecast_image_large/{LAT}/{LON}/forecast.png"
    IMAGE_PATH = "forecast_large.png"
    DEBUG_PATH = getenv("DEBUG_PATH")
    
    if download_image(IMAGE_URL, IMAGE_PATH):
        summary_colours = analyze_summary(IMAGE_PATH, debug_path=DEBUG_PATH)

        if check_evening_conditions(summary_colours)['go'] == 'yes':
            send_notification([i for i,v in enumerate(summary_colours) if v == 'green'])
        else:
            print("No luck, best get browsing firstlightoptics.com")
    else:
        print("Failed to download the forecast image.")