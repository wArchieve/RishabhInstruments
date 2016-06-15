# python file to return cardinal contours

import cv2
import math
import numpy as np
import Find_Angle


def get_contours(img_path):
    meter_image = cv2.imread(img_path + "\\MeterImages\\cardinals.jpg")
    try:
        gray = cv2.cvtColor(meter_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)
        try:
            _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        except Exception, e:
            # print "Error in reading Image:", str(e)
            # print "error"
            return
        cardinal = []
        # Todo: find contours area between cardinal points area in image
        for cnt in contours:
            if 300 < cv2.contourArea(cnt) < 700:
                cardinal.append(cnt)
        return cardinal
    except Exception, e:
        # print "get_contours", str(e)
        # print "error"
        return


# TODO: Function to get contour at full deflection position contour
def find_top_cardinal(contours):
    i = 0
    for cnt in contours:
        try:
            if 300 < cv2.contourArea(cnt) < 700:
                if i >= len(contours) - 1:
                    # print cv2.contourArea(cnt)
                    (x, y), radius = cv2.minEnclosingCircle(cnt)
                    c = cnt.ravel()
                    cx = c[::2]
                    cy = c[1::2]
                    top_x = int(round(sum(cx) / len(cx)))
                    top_y = int(round(sum(cy) / len(cy)))
                    top_x = (top_x + x) / 2
                    top_y = (top_y + y) / 2

                    return int(top_x), int(top_y)
                    # return x, y
                i += 1
        except Exception, e:
            # print "find_top_cardinal", str(e)
            continue


def draw_main_cardinals(meter, contours, top_x, base_y, min_dist):
    i = 0
    contour_list = contours
    cardinal_cordinates = []
    try:
        for cnt in contours[:-1]:
            if 300 < cv2.contourArea(cnt) < 700:
                # (x, y), radius = cv2.minEnclosingCircle(cnt)
                #print cv2.contourArea(cnt)
                # TODO: Angle calculation between each contour
                c = cnt.ravel()
                cx = c[::2]
                cy = c[1::2]
                x = int(round(sum(cx) / len(cx)))
                y = int(round(sum(cy) / len(cy)))
                dist = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
                # Todo: only compare distance of zero cardinal and five cardinal
                if dist >= min_dist - 20:
                    cv2.line(meter, (int(x), int(y)), (int(top_x), int(base_y)), (255, 0, 0), 1)
                    cardinal_cordinates.append((x, y))
                    contour_list[i] = cnt
                i += 1
    except Exception, e:
        # print "draw_main_contours", str(e)
        # print "error"
        return
    return meter, contour_list, cardinal_cordinates


# Todo: Get pointer angle w.r.t. cardinals
def get_needle_angles(contours, top_x, base_y, pointer, base_line, min_dist):
    i = 0
    contour_list = contours
    angle_list = []
    cardinal_angle = []
    try:
        for cnt in contours:
            if 350 < cv2.contourArea(cnt) < 700:
                # (x, y), radius = cv2.minEnclosingCircle(cnt)
                c = cnt.ravel()
                cx = c[::2]
                cy = c[1::2]
                x = int(round(sum(cx) / len(cx)))
                y = int(round(sum(cy) / len(cy)))
                # TODO: Angle calculation between each contour
                dist = round(math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2), ndigits=2)
                if min_dist - 20 <= dist < min_dist + 20:
                    cardinal = ((x, y), (top_x, base_y))
                    cardinal_ang = round(Find_Angle.ang(cardinal, base_line), ndigits=2)
                    cardinal_angle.append(cardinal_ang)
                    base_and_pointer_angle = Find_Angle.ang(base_line, pointer)
                    needle_angle = Find_Angle.ang(cardinal, pointer)
                    if base_and_pointer_angle >= cardinal_ang:
                        angle_list.append(round(needle_angle, ndigits=2))
                    else:
                        angle_list.append(round(-needle_angle, ndigits=2))
                    contour_list[i] = cnt
                    i += 1
    except Exception, e:
        # print "Exception in get_cardinal_angles", str(e)
        # print "error"
        return
    return angle_list, cardinal_angle


def draw_intermediate_cardinals(meter, base_contour, top_x, top_y):
    try:
        (base_x, base_y) = base_contour
        # (top_x, top_y), radius = cv2.minEnclosingCircle(topcontour)
        cv2.line(meter, (int(base_x), int(base_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)
        cv2.line(meter, (int(top_x), int(top_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)
    except Exception, e:
        # print "basic_structure", str(e)
        # print "error"
        return
    return meter
