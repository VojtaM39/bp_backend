import cv2
import numpy as np
import math

class CourtRecognitionService:
    MASK_LOWER_THRESHOLD = 180
    MASK_UPPER_THRESHOLD = 255

    BIG_NUMBER = 99999
    SMALL_NUMBER = -1
    CENTER_OFFSET = 20

    def get_court(self, image):
        """
        Returns:
            points(list): corner points of court (bottom_left, bottom_right, top_left, top_right)
        """
        try:
            height, width, _ = image.shape

            masked_image = self.__mask_image(image)
            lines = self.__get_lines(masked_image)
            filtered_lines = self.__filter_lines(lines, 0.1 * self.__get_max_distance(lines))
            vertical_lines = self.__get_vertical_lines(filtered_lines)
            top_left, top_right, bottom_left, bottom_right = self.__get_corners_from_lines(vertical_lines, width)

            is_court = self.__is_actual_court(height, width, bottom_left, top_left, bottom_right, top_right)
            if not is_court:
                return None

            # Normalize the court to 0-1 interval
            court = [top_left, top_right, bottom_left, bottom_right]
            court = [[corner[0] / width, corner[1] / height] for corner in court]
            return court
        except Exception as e:
            print('detect_corners failed on:')
            print(e)
            return None

    def __mask_image(self, image):
        lower = np.uint8([self.MASK_LOWER_THRESHOLD, self.MASK_LOWER_THRESHOLD, self.MASK_LOWER_THRESHOLD])
        upper = np.uint8([self.MASK_UPPER_THRESHOLD, self.MASK_UPPER_THRESHOLD, self.MASK_UPPER_THRESHOLD])
        return cv2.inRange(image, lower, upper)

    def __get_lines(self, image):
        rho = 1
        theta = np.pi / 180
        threshold = 4
        min_line_length = 26
        max_line_gap = 5

        return cv2.HoughLinesP(image, rho, theta, threshold, np.array([]),
                               min_line_length, max_line_gap)

    def __get_blurred_image(self, image):
        return cv2.GaussianBlur(image, (9, 27), 0)

    def __get_distance(self, line):
        x1, y1, x2, y2 = line[0]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def __is_vertical(self, line):
        x1, y1, x2, y2 = line[0]
        return abs(y1 - y2) > abs(x1 - x2)

    def __get_max_distance(self, lines, vertical=None):
        curr_max = -1
        for line in lines:
            if (vertical is not None):
                if vertical != self.__is_vertical(line):
                    continue

            curr_max = max(curr_max, self.__get_distance(line))
        return curr_max

    def __filter_lines(self, lines, threshold):
        filtered_lines = []
        for line in lines:
            size = self.__get_distance(line)
            if (size > threshold):
                filtered_lines.append(line)
        return filtered_lines

    def __get_vertical_outer_lines(self, lines, max_size):
        # ((top), (bot))
        max = ((-1, None), (-1, None))
        min = ((float('inf'), None), (float('inf'), None))
        for line in lines:
            if not self.__is_vertical(line):
                continue

            if self.__get_distance(line) < 0.4 * max_size:
                continue

            x1, y1, x2, y2 = line[0]
            if y1 > y2:
                curr = ((x1, y1), (x2, y2))
            else:
                curr = ((x2, y2), (x1, y1))

            if curr[0][0] > max[0][0] and curr[1][0] > max[1][0]:
                max = curr
            elif curr[0][0] < min[0][0] and curr[1][0] < min[1][0]:
                min = curr

        return [min, max]

    def __get_vertical_lines(self, lines):
        result = []
        for line in lines:
            if self.__is_vertical(line):
                result.append(line)
        return result

    def __is_actual_court(self, height, width, left_bot, left_top, right_bot, right_top):
        MIN_RATIO_TOP = 0.2
        MIN_RATIO_BOTTOM = 0.4
        MIN_RATIO_VERTICAL = 0.3

        all_corners = [left_bot, left_top, right_bot, right_top]
        for corner in all_corners:
            if corner == self.BIG_NUMBER:
                return False

            if corner == self.SMALL_NUMBER:
                return False

        top_width = abs(right_top[0] - left_top[0])
        bottom_width = abs(right_bot[0] - left_bot[0])
        left_height = abs(left_bot[1] - left_top[1])
        right_height = abs(right_bot[1] - right_top[1])

        if top_width < width * MIN_RATIO_TOP:
            return False

        if bottom_width < width * MIN_RATIO_BOTTOM:
            return False

        min_height = height * MIN_RATIO_VERTICAL

        if left_height < min_height:
            return False

        if right_height < min_height:
            return False

        return True

    def __create_line_image(self, image, lines):
        height, width, _ = image.shape
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        for line_wrapper in lines:
            line = line_wrapper[0]
            cv2.line(canvas, (line[0], line[1]), (line[2], line[3]), (255, 255, 255), 2)
        return canvas

    def __get_corners_from_lines(self, lines, width):
        x_mid = width // 2

        top_left = (self.BIG_NUMBER, self.BIG_NUMBER)
        top_right = (self.SMALL_NUMBER, self.BIG_NUMBER)
        bottom_left = (self.BIG_NUMBER, self.SMALL_NUMBER)
        bottom_right = (self.SMALL_NUMBER, self.SMALL_NUMBER)

        for line_wrapper in lines:
            line = line_wrapper[0]

            point1 = [int(line[0]), int(line[1])]
            point2 = [int(line[2]), int(line[3])]

            for point in [point1, point2]:
                if point[0] < x_mid - self.CENTER_OFFSET and point[1] < top_left[1]:
                    top_left = point

                if point[0] > x_mid + self.CENTER_OFFSET and point[1] < top_right[1]:
                    top_right = point

                if point[0] < x_mid - self.CENTER_OFFSET and point[1] > bottom_left[1]:
                    bottom_left = point

                if point[0] > x_mid + self.CENTER_OFFSET and point[1] > bottom_right[1]:
                    bottom_right = point

        return top_left, top_right, bottom_left, bottom_right
