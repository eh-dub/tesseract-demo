#!/usr/bin/python3
import numpy as np
import av
from PIL import Image, ImageDraw, ImageShow, ImageFilter, ImageOps
import pathlib
from extractROIsFromVideo import extractROIsFromVideo

def drawGrid(draw, w, h): 
    gridSize = 20
    for i in range(int(w/gridSize)):
        x = gridSize*i
        draw.line((x, 0) + (x, h))
    
    for i in range (int(h / gridSize)):
        y = gridSize*i
        draw.line((0, y) + (w, y))

def extractROIsAtTimes(container, roi, FPS, times):
    roisByTimes = []
    for t in times:
        roisByTimes.append(extractROIsFromVideo(container, roi, FPS, t-1, t+1))
    return [r for rois in roisByTimes for r in rois] # https://stackabuse.com/python-how-to-flatten-list-of-lists/

def computeAvgImg(buffer):
    if len(buffer) == 0:
        exit(1)

    w,h = buffer[0].size

    # rewrite this in a functional style. reduce using np.zeros as the initial accumulator value
    # iterate over a list of morphisms Could make a good blog post.
    avg = np.zeros((h,w), np.float)
    for i in buffer:
        i = i.convert('L')
        i = np.array(i, dtype=np.float)
        avg = avg + i/float(len(buffer))

    # Round values in array and cast as 8-bit integer
    avg = np.array(np.round(avg),dtype=np.uint8)
    # avg = avg.filter(ImageFilter.CONTOUR)
    finalImg = Image.fromarray(avg, 'L')
    finalImg = ImageOps.invert(finalImg)
    finalImg = finalImg.point(lambda i: 0 if i < 150 else 255)
    # finalImg = finalImg.filter(ImageFilter.CONTOUR)
    finalImg.info["name"] =f'.png' 
    # finalImg.info["name"] =f'{buffer[0].info["timestamp"]}-{buffer[-1].info["timestamp"]}.png' 
    return finalImg

video_path = pathlib.PurePath("./huskerrs_clip.mkv")
container = av.open(str(video_path))
# container.streams.video[0].thread_type = 'AUTO'
FPS = float(container.streams.video[0].average_rate)
# print(f"FPS: {FPS}")

bboxes = [(1212,30,1228,50), (1152, 30, 1187, 50), (1000,0,1280,100)] # right-eye, left-eye, both: (0,0,1280,720)
[rightEye, leftEye, both] = extractROIsFromVideo(container, bboxes, FPS, 0, 300)

buffer = []
for (i, roi) in enumerate(rightEye):
    if i % (2*FPS) == 0 and i != 0:
        buffer.append(roi)
        avg = computeAvgImg(buffer)
        avg.save(f'./kill-count-rois/right/{i}{avg.info["name"]}')
        # avg.show()
        buffer = [] 
    else:
        buffer.append(roi)
        
# for roi in leftEye:
# 	roi.save(f'./kill-count-rois/left/{roi.info["timestamp"]}.png')
# for roi in both:
# 	roi.save(f'./kill-count-rois/both/{roi.info["timestamp"]}.png')
exit(0)

