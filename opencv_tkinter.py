import Tkinter as tk
import cv2
from PIL import Image, ImageTk

#I had to uninstall PIL and pillow with conda, then use pip to install image

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    
def close():
    cap.release()
    root.destroy()
    
width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()
root.wm_protocol("WM_DELETE_WINDOW", close) 
lmain = tk.Label(root)
lmain.pack()    

show_frame()
root.mainloop()