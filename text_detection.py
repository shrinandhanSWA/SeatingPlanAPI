import cv2
import pytesseract
import numpy as np

from statistics import mean
import sys

def matrix_representation(number_of_seats, image_location, result_image_location):
    seats = {}
    for i in range(1, number_of_seats):
        seats[i] = []

    widths = {}
    heights = {}

    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    img = cv2.imread(image_location)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_org = img.copy()

    for high in range(0, 21):
        for low in range(0, 12):
            # blue limits
            lower_limit = np.array([80 + low * 10, 0, 0])
            higher_limit = np.array([255, 20 + high * 10, 20 + high * 10])

            # blue mask
            mask = cv2.inRange(img, lower_limit, higher_limit)

            # take a copy of the image
            img1 = img.copy()
            img1[mask == 0] = (255, 255, 255)

            gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
            _, img1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # word detection
            boxes = pytesseract.image_to_data(img1)

            for number, box in enumerate(boxes.splitlines()):
                if number != 0:
                    box = box.split()
                    if len(box) == 12:
                        x, y, width, height = int(box[6]), int(box[7]), int(box[8]), int(box[9])

                        if box[11].isdigit() and int(box[11]) != 0:
                            if len(seats) > int(box[11]):
                                seats[int(box[11])].append((x, y, width, height))

                                # width and height statistics
                                if width in widths:
                                    widths[width] = widths[width] + 1
                                else:
                                    widths[width] = 0
                                if height in heights:
                                    heights[height] = heights[height] + 1
                                else:
                                    heights[height] = 0

    revised_seats = {}
    for seat_number, box in seats.items():
        if len(box) == 0:
            continue
        best_stat = max([heights[height] + widths[width] for x, y, width, height in box])  # choose best statistics
        for x, y, width, height in box:
            if heights[height] + widths[width] == best_stat:
                revised_seats[seat_number] = (x, y, width, height)

    # matrix according to coordinates
    average_width = mean(sorted(widths, key=widths.get, reverse=True)[:3]) * 2  # multiply 1.5 to add space between seats.
    average_height = mean(
        sorted(heights, key=heights.get, reverse=True)[:3]) * 2  # multiply 1.5 to add space between seats.

    height, width, _ = img.shape

    dim_x = int(width / average_width)
    dim_y = int(height / average_height)

    matrix = np.zeros((dim_x, dim_y))

    # fill matrix
    for seat_number, box in revised_seats.items():
        x, y, width, height = box

        mean_x = int(x / average_width)
        mean_y = int(y / average_height)
        matrix[mean_x][mean_y] = seat_number

        cv2.rectangle(img_org, (x, y), (width + x, height + y), (0, 0, 255), 3)
        cv2.putText(img_org, str(seat_number), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

    cv2.imwrite(result_image_location, img_org)

    return matrix

if __name__ == '__main__':
    np.set_printoptions(precision=3)
    np.set_printoptions(threshold=sys.maxsize, linewidth=75 * 3)

    print(matrix_representation(77, 'theatre_images/3.png', "result.png"))