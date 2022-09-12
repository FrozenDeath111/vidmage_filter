import cv2
import os
import glob
import math
from moviepy.editor import *
import mediapipe as mp
import shutil
from .img_proc import *


def vid_to_frame(filepath, filename):
    vidcap = cv2.VideoCapture(filepath)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    count_digit = 0

    while frame_count > 0:
        count_digit += 1
        frame_count = int(frame_count/10)

    success, frame = vidcap.read()
    h, w, c = frame.shape
    size = (w, h)
    count = 0

    filename = os.path.splitext(filename)[0]

    temp = 'static/temp'+filename
    if not os.path.isdir(temp):
        os.mkdir(temp)

    while success:
        count_str = str(count)
        cv2.imwrite(temp + '/' + count_str.zfill(count_digit) + '.jpg', frame)
        success, frame = vidcap.read()
        count += 1

    return [size, fps]


def vid_write(filepath, savepath, size, fps, option):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter(savepath, fourcc, fps, size)

    if option == 'GreyScale':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = grey_scale_vid(img)
            output.write(img)

    elif option == 'Bright':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = bright_vid(img)
            output.write(img)

    elif option == 'Darker':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = darker_vid(img)
            output.write(img)

    elif option == 'Sharpen':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = sharpen_vid(img)
            output.write(img)

    elif option == 'Sepia':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = sepia_vid(img)
            output.write(img)

    elif option == 'HDR':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = hdr_vid(img)
            output.write(img)

    elif option == 'Inverted':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = inverted_vid(img)
            output.write(img)

    elif option == 'GreySketch':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = grey_sketch_vid(img)
            output.write(img)

    elif option == 'ColorSketch':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = color_sketch_vid(img)
            output.write(img)

    elif option == 'Stylize':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = stylize_vid(img)
            output.write(img)

    elif option == 'PencilSketch':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = sketch_vid(img)
            output.write(img)

    elif option == 'Summer':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = summer_vid(img)
            output.write(img)

    elif option == 'Winter':
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = winter_vid(img)
            output.write(img)

    else:
        for file in glob.glob(filepath+'*.jpg'):
            img = cv2.imread(file)
            img = gotham_vid(img)
            output.write(img)

    cv2.destroyAllWindows()
    output.release()

    # if os.path.isdir('temp'):
        # shutil.rmtree('temp')


def audio_extract(filepath):
    video = VideoFileClip(filepath)
    filename, ext = os.path.splitext(filepath)
    try:
        video.audio.write_audiofile(f"{filename}.mp3")
    except AttributeError:
        return 'not_exist'
    # print('Audio Extracted')
    return filename+'.mp3'


def audio_adder(audio_file, video_file, name):
    videoclip = VideoFileClip(video_file)
    audioclip = CompositeAudioClip([AudioFileClip(audio_file)])
    videoclip.audio = audioclip
    videoclip.write_videofile(r"./media/Converted/cnv_" + name)
    # os.remove(audio_file)


# if __name__ == '__main__':
# pass