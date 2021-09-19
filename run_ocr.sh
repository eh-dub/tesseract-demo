rm kill-count-rois/*.png
docker build -t tesseract-demo .
docker run -v "$(pwd)"/:/tesseract --rm tesseract-demo conda run -n tesseract python3 watch_video.py
ls kill-count-rois/ | grep png > kill-count-rois/imgs.txt
docker run -v "$(pwd)"/:/tesseract --rm tesseract-demo bash -c "cd kill-count-rois && conda run -n \"tesseract\" tesseract imgs.txt results --psm 8 -c tessedit_char_whitelist=0123456789"