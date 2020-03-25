import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image as img
from PIL import ImageTk as img_tk
import cv2

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.file_path = tk.StringVar()
        self.curr_img_tk = None

        self.lab_fp = tk.Label(self)
        self.lab_fp["text"] = "影像檔位置："
        self.lab_fp.grid(row=0, column=0)

        self.entry_fp = tk.Entry(self)
        self.entry_fp["width"] = 30
        self.entry_fp["textvariable"] = self.file_path
        self.entry_fp.grid(row=0, column=1)

        self.btn_fd = tk.Button(self)
        self.btn_fd["text"] = "..."
        self.btn_fd["command"] = self.open_fd
        self.btn_fd.grid(row=0, column=2)

        self.btn_detect = tk.Button(self)
        self.btn_detect["text"] = "辨識偵測"
        self.btn_detect["command"] = self.detect
        self.btn_detect.grid(row=0, column=3)

        self.lab_image = tk.Label(self)        
        self.lab_image.grid(row=1, column=0, columnspan=4)

    def open_fd(self):
        """ 選取檔案對話框 """
        file_sel = fd.askopenfilename(title = "請選取影像檔",
            filetypes = (("jpeg","*.jpg"), ("png","*.png"), ("all files","*.*")))        
        self.file_path.set(file_sel)
        self.display_img(file_sel)

    def fitting_size(self, size):
        """ 計算影像應縮放比例 """
        w, h = size
        max_scale = 0
        w_scale = w / 800
        h_scale = h / 600
        if w_scale >= h_scale:
            max_scale = w_scale
        else:
            max_scale = h_scale 
    
        last_scale = 1 / max_scale
        w_size = int(w * last_scale)
        h_size = int(h * last_scale)

        return  (w_size, h_size)

    def display_img(self, image_name):
        orig_img = img.open(image_name)
        scale = self.fitting_size(orig_img.size)
        scale_img = orig_img.resize(scale)
        self.curr_img_tk = img_tk.PhotoImage(image=scale_img)
        self.lab_image["image"]= self.curr_img_tk

    def detect(self):
        cv_path = str(self.file_path.get()).replace('\\','\\\\')
        temp_img = cv2.imread(cv_path)
        gray_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
        faces_rets = face_cascade.detectMultiScale(gray_img, scaleFactor=1.05, 
            minNeighbors=5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)
        for (x,y,w,h) in faces_rets:
            img_rt = cv2.rectangle(temp_img, (x,y), (x+w, y+h), (255,0,0), 2)
            roi_gray = gray_img[y:y+h, x:x+w]
            roi_color = temp_img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
        # sub_file_name = self.file_path.get()        
        cv2.imwrite("tmp.jpg",temp_img)
        self.display_img("tmp.jpg")
        # 

if __name__ == "__main__":
    root = tk.Tk()
    root.title("opencv 範例程式")
    root.geometry("840x780")
    app = Application(master=root)
    app.mainloop()