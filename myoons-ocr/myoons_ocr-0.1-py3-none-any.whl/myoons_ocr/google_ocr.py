"""Visualizing OCR Results"""
import os
import cv2


def google_ocr(word_bounding_boxes, img_path):

    img = cv2.imread('./images/korean_hand.jpg')

    for bbox in word_bounding_boxes:
        cv2.rectangle(img, bbox[0], bbox[2], (0, 0, 255), 1)

    cv2.imwrite(f'results_{os.path.basename(img_path)}', img)
    cv2.imshow('img', img)
    cv2.waitKey()
    cv2.destroyAllWindows()