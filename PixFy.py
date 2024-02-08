# importing library
from tkinter import *
from tkinterdnd2 import TkinterDnD, DND_ALL, Tk

import customtkinter as ctk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import cv2
import numpy as np
from skimage.util import random_noise
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter.font as font


class LeftFrame(ctk.CTkFrame, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


w = Tk()

# Using piece of code from old splash screen
width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
w.geometry(
    "%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate)
)
# w.configure(bg='#ED1B76')
w.overrideredirect(1)  # for hiding titlebar


# new window to open
def new_win():
    def dropImg(event):
        global filename
        global input_image
        filename = event.data.strip(r"{}")
        img = Image.open(filename)
        input_image = cv2.imread(filename)
        for widget in left_frame.winfo_children():
            widget.destroy()

        max_width = 750
        max_height = 450

        img.thumbnail((max_width, max_height))

        # Create a blank image with fixed frame size
        fixed_size_img = Image.new("RGB", (max_width, max_height))
        fixed_size_img.paste(
            img, ((max_width - img.width) // 2, (max_height - img.height) // 2)
        )

        resized_imgtk = ImageTk.PhotoImage(fixed_size_img)

        img_label = ctk.CTkLabel(left_frame, text="")
        img_label.configure(image=resized_imgtk)
        img_label.image = resized_imgtk
        img_label.grid(row=0, column=0, padx=10, pady=5)
        img_label.drop_target_register(DND_ALL)
        img_label.dnd_bind("<<Drop>>", dropImg)
        lab = ctk.CTkLabel(left_frame, text="Original Image")
        lab.grid(row=1, column=0, padx=10, pady=5)
        lab["font"] = font.Font(weight="bold", size=12)

    w.destroy()
    root = ctk.CTk()
    root.title("PixFy")
    width_of_window = 1283
    height_of_window = 575
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    root.geometry(
        "%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate)
    )
    ctk.set_appearance_mode("dark")
    root.resizable(width=False, height=False)

    left_frame = LeftFrame(root, width=620, height=400)
    left_frame.grid(row=0, column=0, padx=10, pady=5)
    left_frame.grid_propagate(False)

    img_label = ctk.CTkLabel(left_frame, text="", width=750, height=450)
    img_label.grid(row=0, column=0, padx=10, pady=5)
    img_label.drop_target_register(DND_ALL)
    img_label.dnd_bind("<<Drop>>", dropImg)

    left_frame_down = ctk.CTkFrame(root, width=200, height=300)
    left_frame_down.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

    left_frame_down_basic = ctk.CTkFrame(root, width=200, height=300)
    left_frame_down_basic.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

    right_frame = ctk.CTkFrame(root, width=620, height=400)
    right_frame.grid(row=0, column=1, padx=10, pady=5)

    def show_popup(type):
        popup = ctk.CTk()
        popup.title("Custom Popup")
        popup.resizable(width=False, height=False)
        s_w = popup.winfo_screenwidth()
        s_h = popup.winfo_screenheight()
        pop_w = 170
        pop_h = 130
        x = (s_w // 2) - (pop_w // 2)
        y = (s_h // 2) - (pop_h // 2)

        if type == "r":
            pop_h = 80
            angle_entry = ctk.CTkEntry(popup, width=150, placeholder_text="Enter Angle")
            angle_entry.place(x=10, y=10)

            # Create a button to submit the form
            submit_button = ctk.CTkButton(
                popup, text="Rotate", command=lambda: submit_form(angle_entry.get())
            )
            submit_button.place(x=15, y=45)

            # Function to handle form submission
            def submit_form(angle):
                if angle:
                    popup.destroy()
                    Rot(angle)
                else:
                    messagebox.showerror("Error", "Please fill in all fields.")

        elif type == "t":
            x_entry = ctk.CTkEntry(popup, width=150, placeholder_text="Enter X axis")
            x_entry.place(x=10, y=10)
            y_entry = ctk.CTkEntry(popup, width=150, placeholder_text="Enter Y axis")
            y_entry.place(x=10, y=50)

            # Create a button to submit the form
            submit_button = ctk.CTkButton(
                popup,
                text="Transalete",
                command=lambda: submit_form(x_entry.get(), y_entry.get()),
            )
            submit_button.place(x=15, y=90)

            # Function to handle form submission
            def submit_form(x, y):
                if x and y:
                    popup.destroy()
                    Trans(x, y)
                else:
                    messagebox.showerror("Error", "Please fill in all fields.")

        elif type == "res":
            w_entry = ctk.CTkEntry(popup, width=150, placeholder_text="Enter new width")
            w_entry.place(x=10, y=10)
            h_entry = ctk.CTkEntry(
                popup, width=150, placeholder_text="Enter new height"
            )
            h_entry.place(x=10, y=50)

            # Create a button to submit the form
            submit_button = ctk.CTkButton(
                popup,
                text="Resize",
                command=lambda: submit_form(w_entry.get(), h_entry.get()),
            )
            submit_button.place(x=15, y=90)

            # Function to handle form submission
            def submit_form(w, h):
                if w and h:
                    popup.destroy()
                    Resize(w, h)
                else:
                    messagebox.showerror("Error", "Please fill in all fields.")

        popup.geometry(f"{pop_w}x{pop_h}+{x}+{y}")
        popup.mainloop()

    #
    def dropImg(event):
        global filename
        global input_image
        filename = event.data.strip(r"{}")
        img = Image.open(filename)
        input_image = cv2.imread(filename)
        for widget in left_frame.winfo_children():
            widget.destroy()

        max_width = 750
        max_height = 450

        img.thumbnail((max_width, max_height))

        # Create a blank image with fixed frame size
        fixed_size_img = Image.new("RGB", (max_width, max_height))
        fixed_size_img.paste(
            img, ((max_width - img.width) // 2, (max_height - img.height) // 2)
        )

        resized_imgtk = ImageTk.PhotoImage(fixed_size_img)

        img_label = ctk.CTkLabel(left_frame, text="")
        img_label.configure(image=resized_imgtk)
        img_label.image = resized_imgtk
        img_label.grid(row=0, column=0, padx=10, pady=5)
        img_label.drop_target_register(DND_ALL)
        img_label.dnd_bind("<<Drop>>", dropImg)
        lab = ctk.CTkLabel(left_frame, text="Original Image")
        lab.grid(row=1, column=0, padx=10, pady=5)
        lab["font"] = font.Font(weight="bold", size=12)

    # Function to upload image
    def uploadImg():
        global filename
        global input_image
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            filetypes=(("JGP File", "*.jpg"), ("PNG File", "*.png")),
        )
        img = Image.open(filename)
        input_image = cv2.imread(filename)
        for widget in left_frame.winfo_children():
            widget.destroy()

        max_width = 750
        max_height = 450

        img.thumbnail((max_width, max_height))

        # Create a blank image with fixed frame size
        fixed_size_img = Image.new("RGB", (max_width, max_height))
        fixed_size_img.paste(
            img, ((max_width - img.width) // 2, (max_height - img.height) // 2)
        )

        resized_imgtk = ImageTk.PhotoImage(fixed_size_img)

        img_label = ctk.CTkLabel(left_frame, text="")
        img_label.configure(image=resized_imgtk)
        img_label.image = resized_imgtk
        img_label.grid(row=0, column=0, padx=10, pady=5)
        img_label.drop_target_register(DND_ALL)
        img_label.dnd_bind("<<Drop>>", dropImg)
        lab = ctk.CTkLabel(left_frame, text="Original Image")
        lab.grid(row=1, column=0, padx=10, pady=5)
        lab["font"] = font.Font(weight="bold", size=12)

    # Function to convert image to gray
    def ConvertGray():
        imgg = input_image
        gray_image = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)

        img = Image.fromarray(gray_image)
        # imgtk = ImageTk.PhotoImage(img)
        Display(img, "Gray Image")
        return gray_image

    # Function to resize image
    def Resize(w, h):
        imgg = Image.open(filename)
        # resized_img = cv2.resize(imgg, (int(w), int(h)))
        # img = Image.fromarray(resized_img)
        # resize with pillow
        n = (int(w), int(h))
        resized_img = imgg.resize(n, Image.ANTIALIAS)

        Display(resized_img, "Resized Image")

    # Function to rotate image
    def Rot(anglee):
        imgg = Image.open(filename)
        # With cv2
        # center = (imgg.shape[0] // 2, imgg.shape[1] // 2)
        # rotation_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        # rotated_img = cv2.warpAffine(imgg, rotation_mat, (imgg.shape[0], imgg.shape[1]))
        # img = Image.fromarray(rotated_img)

        # With Pillow
        rotated_img = imgg.rotate(int(anglee))
        Display(rotated_img, "Rotated Image")

    # Function to Transalte image
    def Trans(x, y):
        imgg = Image.open(filename)
        # trans_mat = np.float32([[1, 0, int(x)], [0, 1, int(y)]])
        # trans_img = cv2.warpAffine(imgg, trans_mat, (imgg.shape[0], imgg.shape[1]))
        #
        # img = Image.fromarray(trans_img)
        t_img = imgg.transform(imgg.size, Image.AFFINE, (1, 0, int(x), 0, 1, int(y)))
        Display(t_img, "Transaleted Image")

    # Function to Equalized image
    def equalize():
        eq_img = cv2.equalizeHist(ConvertGray())
        img = Image.fromarray(eq_img)

        Display(img, "Equalized Image")
        return eq_img

    # Function to stretch image
    def stretch():
        imgg = input_image
        # Max - Min input img
        min_in = np.min(imgg)
        max_in = np.max(imgg)

        # Max - Min input img
        min_out = 0
        max_out = 255
        # Stretch Equation
        stretch_img = np.uint8(
            (imgg - min_in) * ((max_out - min_out) / (max_in - min_in)) + max_out
        )
        img = Image.fromarray(stretch_img)
        Display(img, "Stretch Image")

    # Function Thresholding image
    def thresh():
        k = 128
        f, thresh_img = cv2.threshold(input_image, k, 255, cv2.THRESH_BINARY)
        img = Image.fromarray(thresh_img)
        Display(img, "Thresholding Image")

    # Function Negtive filter
    def neg():
        neg_img = 255 - input_image
        img = Image.fromarray(neg_img)
        Display(img, "Negtive Image")

    # Function Log filter
    def log():
        c = 255 / np.log(1 + np.max(input_image))
        log_img = np.uint8(c * np.log(1 + input_image))
        img = Image.fromarray(log_img)
        Display(img, "Log Image")

    # Function Power filter
    def power():
        norm_img = input_image / 255.0
        gamma = 2.2  # Lower than 10

        power_img = np.power(norm_img, gamma)
        power_img2 = np.uint8(power_img * 255)
        img = Image.fromarray(power_img2)
        Display(img, "Power Image")

    # Function Gaussian filter smoothing
    def gaus():
        mask = (9, 9)
        gas_img = cv2.GaussianBlur(input_image, mask, 0)
        img = Image.fromarray(gas_img)
        Display(img, "Gaussian Image")
        return gas_img

    def smooth():
        mask2 = (9, 9)
        avg_img = cv2.blur(input_image, mask2)
        img = Image.fromarray(avg_img)
        Display(img, "Smoothing Image")

    # Function  Create filters Sharp
    def sharp(ftype):
        if ftype == "f1":
            f1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            img_f1 = cv2.filter2D(input_image, -1, f1)
            img = Image.fromarray(img_f1)
            Display(img, "Sharping F1 Image")
        elif ftype == "f2":
            f2 = np.array([[1, 1, 1], [1, -7, 1], [1, 1, 1]])
            img_f2 = cv2.filter2D(input_image, -1, f2)
            img = Image.fromarray(img_f2)
            Display(img, "Sharping F2 Image")
        elif ftype == "f3":
            f3 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
            img_f3 = cv2.filter2D(input_image, -1, f3)
            img = Image.fromarray(img_f3)
            Display(img, "Sharping F3 Image")

    # Function gaussian noise
    def gausnoise():
        img_gauss = random_noise(
            cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY),
            mode="gaussian",
            mean=0,
            var=0.01,
        )
        img_gauss = np.uint8(img_gauss * 255)
        img = Image.fromarray(img_gauss)
        Display(img, "Gaussian Noise Image")

    # Function s&p noise
    def sandp():
        img_salt_pepper = random_noise(
            cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY), mode="s&p", amount=0.15
        )
        img_salt_pepper = np.uint8(img_salt_pepper * 255)
        img = Image.fromarray(img_salt_pepper)
        Display(img, "Salt & Pepper Noise Image")

    # Function canny filter
    def canny():
        img_canny = cv2.Canny(cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY), 50, 100)
        img = Image.fromarray(img_canny)
        Display(img, "Canny Image")

    # Function sobel filter
    def sobel(pos):
        if pos == "x":
            img_soblex = cv2.Sobel(
                cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY), -1, 1, 0
            )
            img = Image.fromarray(img_soblex)
            Display(img, "Sobalx Image")

        elif pos == "y":
            img_sobley = cv2.Sobel(
                cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY), -1, 0, 1
            )
            img = Image.fromarray(img_sobley)
            Display(img, "Sobaly Image")

        elif pos == "xy":
            img_soblex = cv2.Sobel(
                cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY), -1, 1, 0
            )
            img_sobley = cv2.Sobel(
                cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY), -1, 0, 1
            )
            img_soblexy = cv2.addWeighted(img_soblex, 1, img_sobley, 1, 0)
            img = Image.fromarray(img_soblexy)
            Display(img, "Sobalxy Image")

    # Function med filter
    def med():
        img_med = cv2.medianBlur(input_image, 5)
        img = Image.fromarray(img_med)
        Display(img, "Median Image")

    def box():
        img_box = cv2.boxFilter(input_image, -1, (5, 5))
        img = Image.fromarray(img_box)
        Display(img, "Box Image")

    # Function to save image
    def save():
        if img:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png", filetypes=[("PNG files", "*.png")]
            )

            if file_path:
                img.save(file_path)

    # Display image
    def Display(imgtk, type):
        for widget in right_frame.winfo_children():
            widget.destroy()

        max_width = 750
        max_height = 450
        global img
        img = imgtk
        img.thumbnail((max_width, max_height))

        # Create a blank image with fixed frame size
        fixed_size_img = Image.new("RGB", (max_width, max_height))
        fixed_size_img.paste(
            img, ((max_width - img.width) // 2, (max_height - img.height) // 2)
        )

        resized_imgtk = ImageTk.PhotoImage(fixed_size_img)

        img_label = ctk.CTkLabel(right_frame, text="")
        img_label.configure(image=resized_imgtk)
        img_label.image = resized_imgtk
        img_label.grid(row=0, column=0, padx=10, pady=5)

        lab = ctk.CTkLabel(right_frame, text=type)
        lab.grid(row=1, column=0, padx=10, pady=5)
        lab["font"] = font.Font(weight="bold", size=12)

    def selected_value(val):
        if combo.get() == "Equalized":
            # Equalized Image
            equalize()
        elif combo.get() == "Show hist to OG":
            # Show hist to Original image
            showhist("og")
        elif combo.get() == "Show hist to EQ":
            # Show hist to Equalized image
            showhist("eq")
        elif combo.get() == "Stretch":
            # Show hist to Equalized image
            stretch()
        elif combo.get() == "Threshold":
            # Show hist to Equalized image
            thresh()
        elif combo.get() == "Negtive":
            # Show hist to Equalized image
            neg()
        elif combo.get() == "Log transform":
            # Show hist to Equalized image
            log()
        elif combo.get() == "Power":
            # Show hist to Equalized image
            power()
        elif combo.get() == "Gaussian Bluring":
            # Show hist to Equalized image
            gaus()
        elif combo.get() == "Smoothing":
            # Show hist to Equalized image
            smooth()
        elif combo.get() == "Sharping F1":
            # Show hist to Equalized image
            sharp("f1")
        elif combo.get() == "Sharping F2":
            # Show hist to Equalized image
            sharp("f2")
        elif combo.get() == "Sharping F3":
            # Show hist to Equalized image
            sharp("f3")
        elif combo.get() == "Gaussian Noise":
            # Show hist to Equalized image
            gausnoise()
        elif combo.get() == "Salt&Pepper Noise":
            # Show hist to Equalized image
            sandp()
        elif combo.get() == "Canny":
            # Show hist to Equalized image
            canny()
        elif combo.get() == "Sobelx":
            # Show hist to Equalized image
            sobel("x")
        elif combo.get() == "Sobely":
            # Show hist to Equalized image
            sobel("y")
        elif combo.get() == "Sobelxy":
            # Show hist to Equalized image
            sobel("xy")
        elif combo.get() == "Median":
            # Show hist to Equalized image
            med()
        elif combo.get() == "Box":
            # Show hist to Equalized image
            box()

    # Function to show histogram
    def showhist(type):
        if type == "og":
            fig = Figure(figsize=(6, 4.5), dpi=100)
            ax = fig.add_subplot(111)
            ax.hist(ConvertGray().ravel(), 256, [0, 255])
            canvas = FigureCanvasTkAgg(fig, master=right_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=5)
            lab = ctk.CTkLabel(right_frame, text="Histogram to original image")
            lab.grid(row=1, column=0, padx=10, pady=5)
        elif type == "eq":
            fig = Figure(figsize=(6, 4.5), dpi=100)
            ax = fig.add_subplot(111)
            ax.hist(equalize().ravel(), 256, [0, 255])
            canvas = FigureCanvasTkAgg(fig, master=right_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=5)
            lab = ctk.CTkLabel(right_frame, text="Histogram to equalized image")
            lab.grid(row=1, column=0, padx=10, pady=5)

    def light_mode():
        i = switch.get()
        if i == 1:
            ctk.set_appearance_mode("dark")

        else:
            ctk.set_appearance_mode("light")

    select_btn = ctk.CTkButton(left_frame_down, text="Upload Image", command=uploadImg)
    select_btn.grid(row=0, column=2, padx=10, pady=5)

    lab_com = ctk.CTkLabel(left_frame_down, text="Select image mode:     ")
    lab_com.grid(row=0, column=0)
    combo = ctk.CTkComboBox(
        left_frame_down,
        values=[
            "Equalized",
            "Stretch",
            "Threshold",
            "Negtive",
            "Log transform",
            "Power",
            "Gaussian Bluring",
            "Smoothing",
            "Sharping F1",
            "Sharping F2",
            "Sharping F3",
            "Gaussian Noise",
            "Salt&Pepper Noise",
            "Median",
            "Box",
            "Max",
            "Min",
            "Canny",
            "Sobelx",
            "Sobely",
            "Sobelxy",
            "Show hist to OG",
            "Show hist to EQ",
        ],
        command=selected_value,
    )
    combo.grid(column=1, row=0)

    # Basic
    gray = ctk.CTkButton(
        left_frame_down_basic, text="Convert to gray", command=ConvertGray
    )
    gray.grid(row=0, column=0, padx=10, pady=5)

    rotate = ctk.CTkButton(
        left_frame_down_basic, text="Rotate", command=lambda: show_popup("r")
    )
    rotate.grid(row=0, column=2, padx=10, pady=5)

    resize = ctk.CTkButton(
        left_frame_down_basic, text="Resize", command=lambda: show_popup("res")
    )
    resize.grid(row=0, column=1, padx=10, pady=5)

    tran = ctk.CTkButton(
        left_frame_down_basic, text="Translate", command=lambda: show_popup("t")
    )
    tran.grid(row=1, column=0, padx=10, pady=5)

    save = ctk.CTkButton(left_frame_down_basic, text="Save Image", command=save)
    save.grid(row=1, column=1, padx=10, pady=5)

    switch = ctk.CTkSwitch(
        master=left_frame_down_basic, text="Dark mode", command=light_mode
    )
    switch.grid(row=1, column=2)
    switch.select()

    root.mainloop()


Frame(w, width=427, height=250, bg="#272727").place(x=0, y=0)
label1 = Label(w, text="Welcome in PixFy", fg="white", bg="#272727")  # decorate it
label1.configure(
    font=("Game Of Squids", 24, "bold")
)  # You need to install this font in your PC or try another one
label1.place(x=73, y=90)


label2 = Label(
    w, text="Developed by Mohamed Anwar", fg="white", bg="#272727"
)  # decorate it
label2.configure(
    font=("Game Of Squids", 10)
)  # You need to install this font in your PC or try another one
label2.place(x=118, y=135)

label2 = Label(w, text="Loading...", fg="white", bg="#272727")  # decorate it
label2.configure(font=("Calibri", 11))
label2.place(x=10, y=215)

w.after(6000, new_win)
w.mainloop()
