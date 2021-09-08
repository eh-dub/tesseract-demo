#!/usr/bin/python3
import av
from extractROIsFromVideo import extractROIsFromVideo

video_path = "./kill-clip.mkp4"
container = av.open(video_path)

FPS = float(container.streams.video[0].average_rate)
print(f"FPS: {FPS}")

bboxes = [(1212,30,1228,50)]
[rois] = extractROIsFromVideo(container, bboxes, FPS, 0, 300)

for roi in rois:
    roi.save(f'./kill-count-rois/right/{roi.info["timestamp"]}.png')
        
exit(0)

