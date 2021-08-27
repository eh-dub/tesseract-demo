import os

# How to execute shell commands with Python https://janakiev.com/blog/python-shell-commands/

tesseract_command = f"tesseract imgs.txt results --psm 7 -c tessedit_char_whitelist=0123456789"
rois = ['left', 'right', 'both']
for r in rois:
	os.system(f"ls kill-count-rois/{r} | grep png > kill-count-rois/{r}/imgs.txt")
	os.system(f"cd kill-count-rois/{r} && {tesseract_command}")
