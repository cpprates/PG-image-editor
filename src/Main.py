from tkinter import (ttk,Tk,Canvas, filedialog, RIDGE, GROOVE, Scale, HORIZONTAL)
from PIL import ImageTk, Image
import cv2 as cv
import Filters as filters
import Overlay as overlay

class Main:
    def __init__(self, master):        
        self.master = master
        self.frame_header = ttk.Frame(self.master)
        self.frame_header.pack()
        
        ttk.Label(self.frame_header, text='90s Photo Editor!').grid(
            row=0, column=2, columnspan=1)

        self.frame_menu = ttk.Frame(self.master)
        self.frame_menu.pack()
        self.frame_menu.config(relief=RIDGE, padding=(50, 15))
        
        # left menu
        ttk.Button(
            self.frame_menu, text="Open Camera", command=self.camera_action).grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        
        ttk.Button(
            self.frame_menu, text="Upload Image", command=self.upload_action).grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
         
        ttk.Button(
            self.frame_menu, text="Apply Filters", command=self.filter_action).grid(
            row=2, column=0, columnspan=2,  padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.frame_menu, text="Blur", command=self.blur_action).grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.frame_menu, text="Apply Sticker", command=self.sticker_action).grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.frame_menu, text="Save As", command=self.save_action).grid(
            row=5, column=0, columnspan=2, padx=5, pady=5, sticky='sw')

        self.canvas = Canvas(self.frame_menu, bg="gray", width=400, height=500)
        self.canvas.grid(row=0, column=2, rowspan=10)

        self.side_frame = ttk.Frame(self.frame_menu)
        self.side_frame.grid(row=0, column=4, rowspan=10)
        self.side_frame.config(relief=GROOVE, padding=(50,15))        
        
        #  bottom menu
        self.apply_and_cancel = ttk.Frame(self.master)
        self.apply_and_cancel.pack()        
        self.apply = ttk.Button(self.apply_and_cancel, text="Apply", command=self.apply_action).grid(
            row=0, column=0, columnspan=1, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.apply_and_cancel, text="Cancel", command=self.cancel_action).grid(
                row=0, column=2, columnspan=1,padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.apply_and_cancel, text="Revert All Changes", command=self.revert_action).grid(
                row=0, column=1, columnspan=1,padx=5, pady=5, sticky='sw')
        
        #   right menu
        ttk.Label(self.side_frame, text='Optional Menu').grid(row=0, column=0)

    #  right menu updates according to the option selected
    def refresh_side_frame(self):
        try:
            self.side_frame.grid_forget()
        except:
            pass

        self.canvas.unbind("")
        self.canvas.unbind("")
        self.canvas.unbind("")
        self.display_image(self.edited_image)
        self.side_frame = ttk.Frame(self.frame_menu)
        self.side_frame.grid(row=0, column=4, rowspan=10)
        self.side_frame.config(relief=GROOVE, padding=(50, 15))

    # upload image
    def upload_action(self):
        self.canvas.delete("all")
        self.filename = filedialog.askopenfilename()
        
        self.original_image = cv.imread(self.filename)
        self.edited_image = cv.imread(self.filename)
        self.filtered_image = cv.imread(self.filename)

        self.display_image(self.edited_image)
    
    # save image
    def save_action(self):
        original_file_type = self.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type

        save_as_image = self.edited_image
        cv.imwrite(filename, save_as_image)
        self.filename = filename

    # open camera
    def camera_action(self):
        capture = cv.VideoCapture(0)
        if not capture.isOpened():
            print('Unable to open')
            exit(0)
        while True:
            ret, frame = capture.read()
            if frame is None:
                break

            self.filename = 'webcam.jpg'
            self.original_image = frame
            self.edited_image = frame
            self.filtered_image = frame

            # takes a picture of the webcam and displays on screen
            cv.imshow('video', self.display_image(self.edited_image))

            # Display the resulting frame in a new window
            # cv.imshow('frame', frame)
      
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
  
        # After the loop release the cap object
        capture.release()
        # Destroy all the windows
        capture.destroyAllWindows()

    # display image on screen
    def display_image(self, image=None):
        self.canvas.delete("all")
        if image is None:
            image = self.edited_image.copy()
        else:
            image = image

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > 400 or width > 300:
            if ratio < 1:
                new_width = 300
                new_height = int(new_width * ratio)
            else:
                new_height = 400
                new_width = int(new_height * (width / height))

        self.ratio = height / new_height
        self.new_image = cv.resize(image, (new_width, new_height))

        self.new_image = ImageTk.PhotoImage(
            Image.fromarray(self.new_image))

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(
            new_width / 2, new_height / 2,  image=self.new_image)

    # filters menu (right)
    def filter_action(self):
        self.refresh_side_frame()
        ttk.Button(
            self.side_frame, text="Negative", command=self.negative_action).grid(row=0, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Gray", command=self.gray_action).grid(row=1, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Stylisation", command=self.stylisation_action).grid(row=2, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Sketch Effect", command=self.sketch_action).grid(row=3, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Emboss", command=self.emb_action).grid(row=4, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Sepia", command=self.sepia_action).grid(row=5, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Binary Thresholding", command=self.binary_threshold_action).grid(
            row=6, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Erosion", command=self.erosion_action).grid(
            row=7, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Dilation", command=self.dilation_action).grid(
            row=8, column=2, padx=5, pady=5, sticky='sw')
        
        ttk.Button(
            self.side_frame, text="Sharpen", command=self.sharpen_action).grid(
            row=9, column=2, padx=5, pady=5, sticky='sw')
        
        ttk.Button(
            self.side_frame, text="Techno", command=self.techno_action).grid(
            row=10, column=2, padx=5, pady=5, sticky='sw')
        
        ttk.Button(
            self.side_frame, text="Cartoon", command=self.cartoon_action).grid(
            row=11, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Pink Negative", command=self.pinkNegative_action).grid(
            row=12, column=2, padx=5, pady=5, sticky='sw')
        
        ttk.Button(
            self.side_frame, text="Ultraviolet", command=self.purpleUv_action).grid(
            row=13, column=2, padx=5, pady=5, sticky='sw')
        
        ttk.Button(
            self.side_frame, text="Contour", command=self.cannyContour_action).grid(
            row=14, column=2, padx=5, pady=5, sticky='sw')
    
    # stickers menu (right)
    def sticker_action(self):
        self.refresh_side_frame()
        ttk.Button(
            self.side_frame, text="Cat", command=self.cat_sticker).grid(row=0, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Heart", command=self.heart_sticker).grid(row=1, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Star", command=self.star_sticker).grid(row=2, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Santa Claws", command=self.santa_sticker).grid(row=3, column=2, padx=5, pady=5, sticky='sw')

        ttk.Button(
            self.side_frame, text="Tamagotchi", command=self.tama_sticker).grid(row=4, column=2, padx=5, pady=5, sticky='sw')
        
        ttk.Button(
            self.side_frame, text="Vuvuzela", command=self.vuvuzela_sticker).grid(row=5, column=2, padx=5, pady=5, sticky='sw')

    # blur slide menu (right)
    def blur_action(self):
        self.refresh_side_frame()
        ttk.Label(
            self.side_frame, text="Averaging Blur").grid(row=0, column=3, padx=5, sticky='sw')

        self.average_slider = Scale(
            self.side_frame, from_=0, to=256, orient=HORIZONTAL, command=self.averaging_action)
        self.average_slider.grid(row=1, column=3, padx=5,  sticky='sw')

        ttk.Label(
            self.side_frame, text="Gaussian Blur").grid(row=2, column=3, padx=5, sticky='sw')

        self.gaussian_slider = Scale(
            self.side_frame, from_=0, to=256, orient=HORIZONTAL, command=self.gaussian_action)
        self.gaussian_slider.grid(row=3, column=3, padx=5,  sticky='sw')

        ttk.Label(
            self.side_frame, text="Median Blur").grid(row=4, column=3, padx=5, sticky='sw')

        self.median_slider = Scale(
            self.side_frame, from_=0, to=256, orient=HORIZONTAL, command=self.median_action)
        self.median_slider.grid(row=5, column=3, padx=5,  sticky='sw')

    # bottom menu
    def apply_action(self):
        self.edited_image = self.filtered_image
        self.display_image(self.edited_image)

    def cancel_action(self):
        self.display_image(self.edited_image)

    def revert_action(self):
        self.edited_image = self.original_image.copy()
        self.display_image(self.original_image)

    # blur filters
    def averaging_action(self, value):
        self.filtered_image = filters.blurAverage(self.edited_image, value)
        self.display_image(self.filtered_image)

    def gaussian_action(self, value):
        self.filtered_image = filters.blurGaussian(self.edited_image, value)
        self.display_image(self.filtered_image)

    def median_action(self, value):
        self.filtered_image = filters.blurMedian(self.edited_image, value)
        self.display_image(self.filtered_image)

    # color filters
    def negative_action(self):
        self.filtered_image = filters.negative(self.edited_image)
        self.display_image(self.filtered_image)

    def gray_action(self):
        self.filtered_image = filters.gray(self.edited_image)
        self.display_image(self.filtered_image)

    def stylisation_action(self):
        self.filtered_image = filters.stylisation(self.edited_image)
        self.display_image(self.filtered_image)

    def sketch_action(self):
        self.filtered_image = filters.pencil(self.edited_image)
        self.display_image(self.filtered_image)

    def emb_action(self):
        self.filtered_image = filters.emboss(self.edited_image)
        self.display_image(self.filtered_image)

    def sepia_action(self):
        self.filtered_image = filters.sepia(self.edited_image)
        self.display_image(self.filtered_image)

    def binary_threshold_action(self):
        self.filtered_image = filters.binaryThreshold(self.edited_image)
        self.display_image(self.filtered_image)

    def erosion_action(self):
        self.filtered_image = filters.erosion(self.edited_image)
        self.display_image(self.filtered_image)

    def dilation_action(self):
        self.filtered_image = filters.dilation(self.edited_image)
        self.display_image(self.filtered_image)

    def sharpen_action(self):
        self.filtered_image = filters.sharpen(self.edited_image)
        self.display_image(self.filtered_image)

    def techno_action(self):
        self.filtered_image = filters.purpleGreen(self.edited_image)
        self.display_image(self.filtered_image)

    def cartoon_action(self):
        self.filtered_image = filters.cartoon(self.edited_image)
        self.display_image(self.filtered_image)

    def pinkNegative_action(self):
        self.filtered_image = cv.cvtColor(self.edited_image, cv.COLOR_BGR2HSV)
        self.display_image(self.filtered_image)

    def purpleUv_action(self):
        self.filtered_image = filters.purpleUv(self.edited_image)
        self.display_image(self.filtered_image)

    def cannyContour_action(self):
        self.filtered_image = filters.cannyBlur(self.edited_image)
        self.display_image(self.filtered_image)

    # stickers
    def cat_sticker(self):
        sticker = cv.imread('./src/stickers/rawr.png', cv.IMREAD_UNCHANGED)
        sticker = cv.resize(sticker, (0, 0), fx=0.5, fy=0.5)
        self.filtered_image = overlay.alphaMerge(self.filtered_image, sticker, 200, 64)
        self.display_image(self.filtered_image)

    def heart_sticker(self):
        sticker = cv.imread('./src/stickers/coracao.png', cv.IMREAD_UNCHANGED)
        sticker = cv.resize(sticker, (0, 0), fx=0.5, fy=0.5)
        self.filtered_image = overlay.alphaMerge(self.edited_image, sticker, 100, 200)
        self.display_image(self.filtered_image)

    def star_sticker(self):
        sticker = cv.imread('./src/stickers/star.png', cv.IMREAD_UNCHANGED)
        sticker = cv.resize(sticker, (0, 0), fx=0.5, fy=0.5)
        self.filtered_image = overlay.alphaMerge(self.edited_image, sticker, 80, 100)
        self.display_image(self.filtered_image)

    def santa_sticker(self):
        sticker = cv.imread('./src/stickers/santaclaws.png', cv.IMREAD_UNCHANGED)
        sticker = cv.resize(sticker, (0, 0), fx=0.5, fy=0.5)
        self.filtered_image = overlay.alphaMerge(self.edited_image, sticker, 100, 80)
        self.display_image(self.filtered_image)

    def tama_sticker(self):
        sticker = cv.imread('./src/stickers/tama.png', cv.IMREAD_UNCHANGED)
        sticker = cv.resize(sticker, (0, 0), fx=0.5, fy=0.5)
        self.filtered_image = overlay.alphaMerge(self.edited_image, sticker, 150, 50)
        self.display_image(self.filtered_image)

    def vuvuzela_sticker(self):
        sticker = cv.imread('./src/stickers/vuvuzela.png', cv.IMREAD_UNCHANGED)
        sticker = cv.resize(sticker, (0, 0), fx=0.5, fy=0.5)
        self.filtered_image = overlay.alphaMerge(self.edited_image, sticker, 90, 150)
        self.display_image(self.filtered_image)

# render window
mainWindow = Tk()
mainWindow.title('PG | Photo Editor')
mainWindow.iconbitmap('./src/images/icon.ico')
Main(mainWindow)
mainWindow.mainloop()
