import cv2
import numpy as np
import mediapipe as mp


def change_bg(filepath, filepath_bg, cnv_filepath):
    img = cv2.imread(filepath)
    shape = (img.shape[1], img.shape[0])
    bg_img = cv2.imread(filepath_bg)
    bg_img = cv2.resize(bg_img, shape, interpolation=cv2.INTER_AREA)

    img_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    img_frame = selfie_segmentation.process(img_frame)

    mask = img_frame.segmentation_mask

    condition = np.stack((mask,)*3, axis=-1) > .5
    out_img = np.where(condition, img, bg_img)

    cv2.imwrite(cnv_filepath, out_img)
