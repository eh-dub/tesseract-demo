import io
from pprint import pprint # https://jdhao.github.io/2019/07/06/python_opencv_pil_image_to_bytes/
from fastai.vision.all import PILImage

def extractROIsFromVideo(video, cropBoxes, FPS=30, startAt=0, stopAt=0):
    rois = [[] for cb in cropBoxes]
    for frame in video.decode(video=0):
        if frame.index < startAt*FPS:
            continue
        
        # print(f"index {frame.index} time (s): {frame.time}") # for whatever reason frame.time doesn't match timestamp in VLC
        # print(f"index {frame.index} ftime (s): {round(frame.index* (1.0/FPS), 3)}") # for whatever reason frame.time doesn't match timestamp in VLC
        img_pil = frame.to_image()
        for i, cropBox in enumerate(cropBoxes):
            roi = img_pil.crop(cropBox) # (x0, y0, x1, y1)

            # Convert from pyav's PIL Image to fastai's PIL Image
            byte_buffer = io.BytesIO()
            roi.save(byte_buffer, format='PNG')
            pil_roi = PILImage.create(byte_buffer)
            
            pil_roi.info["timestamp"] = round(frame.time, 3) # can store any metadata in "info"
            # pil_roi.info["timestamp"] = round(frame.index * (1.0/FPS), 3) # can store any metadata in "info"
            rois[i].append(pil_roi)

        # Log Progress
        if (frame.index % 10000 == 0):
            print(f"read frame index {frame.index}")

        # Stop after 10000 frames
        if stopAt != 0 and frame.index > stopAt*FPS:
            break
    return rois