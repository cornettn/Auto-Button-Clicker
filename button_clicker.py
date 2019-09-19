import autopy
import time
import numpy
import cv2
from PIL import ImageGrab

def get_screenshot():
    """
    This function captures a screenshot, and converts it to HSV format.
    :return: The array that the image is stored as
    """
    # Dimensions of screenshot 2100, 3360
    # Dimensions of my screen 1050, 1670
    image = ImageGrab.grab()
    image.save("screenshot.png", "PNG")

    # change image to BGR format
    image = cv2.imread("screenshot.png")

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv_image

def analyze_screenshot(image, boundaries):
    """
    This function will analyze the screenshot for pixels with the
    specific boundaries.

    :param image: The image that is to be analyzed
    :param boundaries: The list of HSV values that are being searched for
    :return: A version of the image where the correct color pixels are white,
        and any other pixel that is not the desired color is black.
    """
    for (lower_bound, upper_bound) in boundaries:
        # Convert the limits into numpy arrays
        lower = numpy.array(lower_bound)
        upper = numpy.array(upper_bound)

        # Find the colors within the orange boundaries (uses HSV)
        # The inRange function changes anything in the range to white
        #  everything else turns black
        mask = cv2.inRange(image, lower, upper)

        # Restores the image back to original colors, but anything not
        # within the bounds is black
        output = cv2.bitwise_and(image, image, mask=mask)

    return mask


def find_button_coords():
    # Get the mouse out of the way
    autopy.mouse.move(0, 0)
    time.sleep(.1)

    # Get the HSV formatted screenshot
    image = get_screenshot()

    # Values are stored as HSV
    orange_boundaries = [([13, 203, 187], [13, 203, 187])]

    # Analyze the screenshot to find specific colored pixels
    analzyed_image = analyze_screenshot(image, orange_boundaries)

    # Get location of desired pixels
    indices = numpy.where(analzyed_image == [255])

    # Get mean of x location and y location to find center of circle
    x_location = numpy.mean(indices[1])
    y_location = numpy.mean(indices[0])

    # Divided by 2 to scale to my screen
    return x_location / 2, y_location / 2


def find_and_click_button():
    x, y = find_button_coords()
    print(f"Button Coords: x: {x} y: {y}")

    # Move the mouse to the specific location
    autopy.mouse.move(x, y)

    # Wait for autopy to move the mouse
    time.sleep(.1)

    # Click
    autopy.mouse.click()

    autopy.mouse.move(0, 0)
    time.sleep(.1)

    return x, y

def calculate_distance():

    # Clicks the button once
    x1, y1 = find_and_click_button()

    # Find the coords of the button again
    x2, y2 = find_button_coords()

    x = x2 - x1
    y = y2 - y1
    return x, y

def main():
    """
    This where the main loop occurs.
    """

    while (True):
        find_and_click_button()



if __name__ == "__main__":
    main()