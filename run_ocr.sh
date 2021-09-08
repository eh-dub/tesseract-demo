rm kill-count-rois/*.png
docker run tesseract-demo -v \"$(pwd)\"/:/tesseract-demo poetry run python3 watch_video.py
ls kill-count-rois/ | grep png > kill-count-rois/imgs.txt
docker run tesseract-demo -v \"$(pwd)\"/:/tesseract-demo cd kill-count-rois && poetry run tesseract imgs.txt results --psm 8 -c tessedit_char_whitelist=0123456789