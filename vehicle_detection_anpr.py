import sqlite3
import cv2
import ast
import numpy as np

from detector import Detector
# from detector_lpr import DetectorLPR
from detector_lpr import LicensePlateReader
import cv2
import time
import sys
import datetime
from datetime import datetime
import torch
import math

from glob import glob
import os
import shutil

# cv2.namedWindow('img', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('img', (1000, 1000))
def read_license_plate_number(img, char_threshold):
    
    plate_reading = 'NA'
    
    # detect plate
    bboxes = detector.detect(img)
    
    # filter 'plate only' detections
    plate_only = []
    for i in bboxes:
        if i[4] == 'plate':
            plate_only.append(i)
    if not plate_only:
        print('no plate detected in img')
    if plate_only:
        max_tuple = max(plate_only, key=lambda x:x[5].item()) # find the most probable plate detection
        x1 = max_tuple[0]
        y1 = max_tuple[1]
        x2 = max_tuple[2]
        y2 = max_tuple[3]
        plate_crop = img[y1:y2, x1:x2]
        # cv2.resizeWindow('img', (1000, 1000))
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        # cv2.imshow('img', plate_crop)
        # cv2.waitKey(0)
        # print(plate_crop.shape)
        try:
            plate_reading = detector_lpr.detect(plate_crop)
        except Exception as e:
            print('could not lpr, reason: ', e)
        
        
    return plate_reading

# Initialize yolov5; for plate localization and LPR
detector = Detector()
detector_lpr = LicensePlateReader('E:\\estudy\\City\\SafeCity\\chilas\\chilas_code_2\\yolov5-master-car_match\\yolov5-master\\trained_models\\best_v8.pt')

# initialize LPR prediction threshold
licence_plate_char_threshold = 0.70

start = datetime.now()

while True:
    try:
        conn = sqlite3.connect('E:\\estudy\\City\\chilas\\dbs\\central_db.db')   
        c=conn.cursor()
        # c.execute("DELETE FROM node_database WHERE ismatched = 0 AND ANPR = 'NP'")
        c.execute(f"SELECT * FROM node_database WHERE ismatched = 0 AND ANPR='NP'")
        rows=c.fetchall()
        
        if rows is not None:
            for row in rows:
                print(row)
                try:
                    jpg_img=cv2.imread(row[4])
                    if jpg_img is not None:
                        boundingbox=ast.literal_eval(row[5])
                        if len(boundingbox)>1:
                            print('Error in bounding box length is greater than 1')
                        else:
                            boundingbox=list(map(int, boundingbox[0]))
                            target_width, target_height = 999, 999
                            original_width = jpg_img.shape[1]
                            original_height = jpg_img.shape[0]
                            # print('height, width: ', original_height, original_width)
                            x_scale = target_width / original_width
                            y_scale = target_height / original_height
                            # print('x_scale, y_scale: ', x_scale, y_scale)
                            left=boundingbox[0]
                            top=boundingbox[1]
                            right=boundingbox[2]
                            bottom=boundingbox[3]
                            left, top, right, bottom = left / x_scale, top / y_scale, right / x_scale, bottom / y_scale
                            left, top, right, bottom = map(int, (left, top, right, bottom))
                            left, top, right, bottom = left-100, top+100, right+100, bottom-200   #adjust bbox to safely capture complete car.
                            top = original_height  - top
                            bottom = original_height  - bottom
                            # cv2.imshow('img', jpg_img)
                            # cv2.waitKey(0)
                            img = jpg_img[top:bottom, left:right]
                            plate_reading = read_license_plate_number(img, licence_plate_char_threshold)
                            anpr = '\''+plate_reading+'\''
                            path, image_name = os.path.split(row[4])
                            # print(path)
                            # print(image_name)
                            img_path=path+'/'+plate_reading+'_'+image_name
                            os.rename(row[4], img_path)
                            img_path='\''+img_path+'\''
                            # print(img_path)
                            c.execute(f"UPDATE node_database SET ANPR={anpr},imagePath={img_path} WHERE id ={row[0]}")
                            print(plate_reading)
                        # cv2.imshow('vehicle', img)
                        # cv2.waitKey(1)
                    # print(row)
                except Exception as e:
                    print('Error in opening file', e)
        conn.commit()
        conn.close()
        time.sleep(1)
    except Exception as e:
        print('Error in Fetching Data from server', e)