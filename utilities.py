# pip install pillow - thư viện ảnh
from PIL import Image as PILImage, ImageTk as PILImageTk

def loadImageToLabel(lblImage, imgPath, imgWidth, imgHeight):
    img = PILImage.open(imgPath)
    img = img.resize(size=(imgWidth, imgHeight))
    img = PILImageTk.PhotoImage(img)

    lblImage.configure(image= img)
    lblImage.image = img