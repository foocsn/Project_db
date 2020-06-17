import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image

#地图层级结构："MAP_JPG"->"JPG"->"TOPOGRAPHY"/"WATER" -> scale -> part - > 具体图片
root = os.getcwd()
map_root = os.path.join(root,"MAP_JPG","JPG","TOPOGRAPHY")
water_root = os.path.join(root,"MAP_JPG","JPG","WATER")

