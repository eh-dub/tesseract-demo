#!/usr/bin/python3

import av
from PIL import Image, ImageDraw, ImageShow
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

video_path = pathlib.PurePath("./huskerrs_clip.mkv")
container = av.open(str(video_path))
# container.streams.video[0].thread_type = 'AUTO'
FPS = float(container.streams.video[0].average_rate)
# print(f"FPS: {FPS}")

bboxes = [(1212,30,1247,50), (1152, 30, 1187, 50), (1000,0,1280,100)] # right-eye, left-eye, both: (0,0,1280,720)
[rightEye, leftEye, both] = extractROIsFromVideo(container, bboxes, FPS, 797, 1000)
for roi in rightEye:
	roi.save(f'./kill-count-rois/right/{roi.info["timestamp"]}.png')
for roi in leftEye:
	roi.save(f'./kill-count-rois/left/{roi.info["timestamp"]}.png')
for roi in both:
	roi.save(f'./kill-count-rois/both/{roi.info["timestamp"]}.png')
exit(0)