import os

# How to execute shell commands with Python https://janakiev.com/blog/python-shell-commands/
# rois = ['left', 'right', 'both']
rois = ['right']
for r in rois:
	os.system(f'rm kill-count-rois/{r}/*.png')

os.system("conda run -n tesseract python3 watch_video.py")
tesseract_command = f"tesseract imgs.txt results --dpi 300 --psm 7 -c tessedit_char_whitelist=0123456789 pdf" # tessedit_write_images=true"
for r in rois:
	os.system(f"ls kill-count-rois/{r} | grep png > kill-count-rois/{r}/imgs.txt")
	if r != 'both':
		os.system(f"cd kill-count-rois/{r} && {tesseract_command}")
