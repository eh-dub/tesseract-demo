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
print(f"FPS: {FPS}")
[rois] = extractROIsFromVideo(container, [(1215,30,1230,50)], FPS, 0, 10)
for r in rois:
    # draw = ImageDraw.Draw(r)
    # drawGrid(draw, 1280, 720)
    r.save(f'./kill-count-frames/{r.info["timestamp"]}.png')
exit(0)