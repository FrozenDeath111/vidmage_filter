import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline


def grey_scale(img, des):
    Grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(des, Grey_scale)


def bright(img, des):
    Bright = cv2.convertScaleAbs(img, beta=60)
    cv2.imwrite(des, Bright)


def darker(img, des):
    Darker = cv2.convertScaleAbs(img, beta=-60)
    cv2.imwrite(des, Darker)


def sharpen(img, des):
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    Sharpen = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(des, Sharpen)


def sepia(img, des):
    Sepia = np.array(img, dtype=np.float64)
    Sepia = cv2.transform(Sepia, np.matrix([[0.272, 0.534, 0.131],
                                           [0.349, 0.686, 0.168],
                                           [0.393, 0.769, 0.189]]))
    Sepia[np.where(Sepia > 255)] = 255
    Sepia = np.array(Sepia, dtype=np.uint8)

    cv2.imwrite(des, Sepia)


def hdr(img, des):
    HDR = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)

    cv2.imwrite(des, HDR)


def inverted(img, des):
    Inverted = cv2.bitwise_not(img)

    cv2.imwrite(des, Inverted)


def grey_sketch(img, des):
    GSketch, CSketch = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
    cv2.imwrite(des, GSketch)


def color_sketch(img, des):
    GSketch, CSketch = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
    cv2.imwrite(des, CSketch)


def stylize(img, des):
    Stylize = cv2.stylization(img, sigma_s=15, sigma_r=0.55)
    cv2.imwrite(des, Stylize)


def sketch(img, des):
    Grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Inverted = cv2.bitwise_not(Grey_scale)
    Inverted_blur = cv2.GaussianBlur(Inverted, (21, 21), 0)
    Inverted_blur = cv2.bitwise_not(Inverted_blur)
    Sketch = cv2.divide(Grey_scale, Inverted_blur, scale=240)
    Sketch = np.stack((Sketch,)*3, axis=-1)
    cv2.imwrite(des, Sketch)


def lookup_table(x, y):
    spline = UnivariateSpline(x, y)
    return spline(range(256))


def summer(img, des):
    increaseLookupTable = lookup_table([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = lookup_table([0, 64, 128, 256], [0, 50, 100, 256])

    B_channel, G_channel, R_channel = cv2.split(img)
    R_channel = cv2.LUT(R_channel, increaseLookupTable).astype(np.uint8)
    B_channel = cv2.LUT(B_channel, decreaseLookupTable).astype(np.uint8)

    Summer = cv2.merge((B_channel, G_channel, R_channel))
    cv2.imwrite(des, Summer)


def winter(img, des):
    increaseLookupTable = lookup_table([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = lookup_table([0, 64, 128, 256], [0, 50, 100, 256])

    B_channel, G_channel, R_channel = cv2.split(img)
    R_channel = cv2.LUT(R_channel, decreaseLookupTable).astype(np.uint8)
    B_channel = cv2.LUT(B_channel, increaseLookupTable).astype(np.uint8)

    Winter = cv2.merge((B_channel, G_channel, R_channel))
    cv2.imwrite(des, Winter)


def gotham(img, des):
    midtone_cont_increase = lookup_table([0, 25, 51, 76, 102, 128, 153, 178, 204, 229, 255],
                                         [0, 13, 25, 51, 76, 128, 178, 204, 229, 242, 255])
    lowermid_increase = lookup_table([0, 16, 32, 48, 64, 80, 96, 111, 128, 143, 159, 175, 191, 207, 223, 239, 255],
                                     [0, 18, 35, 64, 81, 99, 107, 112, 121, 143, 159, 175, 191, 207, 223, 239, 255])
    uppermid_decrease = lookup_table([0, 16, 32, 48, 64, 80, 96, 111, 128, 143, 159, 175, 191, 207, 223, 239, 255],
                                     [0, 16, 32, 48, 64, 80, 96, 111, 128, 140, 148, 160, 171, 187, 216, 236, 255])

    B_channel, G_channel, R_channel = cv2.split(img)

    R_channel = cv2.LUT(R_channel, midtone_cont_increase).astype(np.uint8)
    B_channel = cv2.LUT(B_channel, lowermid_increase).astype(np.uint8)
    B_channel = cv2.LUT(B_channel, uppermid_decrease).astype(np.uint8)

    Gotham = cv2.merge((B_channel, G_channel, R_channel))
    cv2.imwrite(des, Gotham)


# Video part
def grey_scale_vid(img):
    Grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Grey_scale = np.stack((Grey_scale,)*3, axis=-1)
    return Grey_scale


def bright_vid(img):
    Bright = cv2.convertScaleAbs(img, beta=60)
    return Bright


def darker_vid(img):
    Darker = cv2.convertScaleAbs(img, beta=-60)
    return Darker


def sharpen_vid(img):
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    Sharpen = cv2.filter2D(img, -1, kernel)
    return Sharpen


def sepia_vid(img):
    Sepia = np.array(img, dtype=np.float64)
    Sepia = cv2.transform(Sepia, np.matrix([[0.272, 0.534, 0.131],
                                           [0.349, 0.686, 0.168],
                                           [0.393, 0.769, 0.189]]))
    Sepia[np.where(Sepia > 255)] = 255
    Sepia = np.array(Sepia, dtype=np.uint8)
    return Sepia


def hdr_vid(img):
    HDR = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return HDR


def inverted_vid(img):
    Inverted = cv2.bitwise_not(img)
    return Inverted


def grey_sketch_vid(img):
    GSketch, CSketch = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
    GSketch = np.stack((GSketch,) * 3, axis=-1)
    return GSketch


def color_sketch_vid(img):
    GSketch, CSketch = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
    return CSketch


def stylize_vid(img):
    Stylize = cv2.stylization(img, sigma_s=15, sigma_r=0.55)
    return Stylize


def sketch_vid(img):
    Grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Inverted = cv2.bitwise_not(Grey_scale)
    Inverted_blur = cv2.GaussianBlur(Inverted, (21, 21), 0)
    Inverted_blur = cv2.bitwise_not(Inverted_blur)
    Sketch = cv2.divide(Grey_scale, Inverted_blur, scale=240)
    Sketch = np.stack((Sketch,)*3, axis=-1)
    return Sketch


def lookup_table(x, y):
    spline = UnivariateSpline(x, y)
    return spline(range(256))


def summer_vid(img):
    increaseLookupTable = lookup_table([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = lookup_table([0, 64, 128, 256], [0, 50, 100, 256])

    B_channel, G_channel, R_channel = cv2.split(img)
    R_channel = cv2.LUT(R_channel, increaseLookupTable).astype(np.uint8)
    B_channel = cv2.LUT(B_channel, decreaseLookupTable).astype(np.uint8)

    Summer = cv2.merge((B_channel, G_channel, R_channel))
    return Summer


def winter_vid(img):
    increaseLookupTable = lookup_table([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = lookup_table([0, 64, 128, 256], [0, 50, 100, 256])

    B_channel, G_channel, R_channel = cv2.split(img)
    R_channel = cv2.LUT(R_channel, decreaseLookupTable).astype(np.uint8)
    B_channel = cv2.LUT(B_channel, increaseLookupTable).astype(np.uint8)

    Winter = cv2.merge((B_channel, G_channel, R_channel))
    return Winter


def gotham_vid(img):
    midtone_cont_increase = lookup_table([0, 25, 51, 76, 102, 128, 153, 178, 204, 229, 255],
                                         [0, 13, 25, 51, 76, 128, 178, 204, 229, 242, 255])
    lowermid_increase = lookup_table([0, 16, 32, 48, 64, 80, 96, 111, 128, 143, 159, 175, 191, 207, 223, 239, 255],
                                     [0, 18, 35, 64, 81, 99, 107, 112, 121, 143, 159, 175, 191, 207, 223, 239, 255])
    uppermid_decrease = lookup_table([0, 16, 32, 48, 64, 80, 96, 111, 128, 143, 159, 175, 191, 207, 223, 239, 255],
                                     [0, 16, 32, 48, 64, 80, 96, 111, 128, 140, 148, 160, 171, 187, 216, 236, 255])

    B_channel, G_channel, R_channel = cv2.split(img)

    R_channel = cv2.LUT(R_channel, midtone_cont_increase).astype(np.uint8)
    B_channel = cv2.LUT(B_channel, lowermid_increase).astype(np.uint8)
    B_channel = cv2.LUT(B_channel, uppermid_decrease).astype(np.uint8)

    Gotham = cv2.merge((B_channel, G_channel, R_channel))
    return Gotham

# if __name__ == '__main__':
    # image = cv2.imread('TrailCircle.png')
    # grey_scale(image)
    # bright(image)
    # darker(image)
    # sharpen(image)
    # sepia(image)
    # hdr(image)
    # inverted(image)
    # grey_sketch(image)
    # color_sketch(image)
    # stylize(image)
    # sketch(image)
    # summer(image)
    # winter(image)
    # gotham(image)
