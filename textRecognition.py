import subprocess
import os

textOut = ""
file = "F:/NSC/opencv.png"
out = "F:/NSC/out"
os.system("tesseract {} {}".format(file, out))
textOut = open('F:/NSC/out.txt', 'r').read()
print textOut
