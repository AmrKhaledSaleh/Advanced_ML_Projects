import tkinter as tk
from tkinter import filedialog
from inference import COD



class GUI:
    def __init__(self):

        # Create the window and set properties
        self.root = tk.Tk()
        self.root.title("Cars Object Detection")
        self.root.geometry("800x600")
        self.root.configure(bg="#34495E")  # Set background color

        # Configure a modern and elegant font
        font_style = ("Helvetica", 12)

        # Create app Frames
        self.MainFrame = tk.Frame(self.root, bg="#34495E")
        self.ModelFrame = tk.Frame(self.root, bg="#34495E")
        self.PhotoFrame = tk.Frame(self.root, bg="#34495E")

        # Home Button to get back to MainFrame
        self.home = tk.Button(self.root, text="Home", font=font_style, command=self.Home, bg="#2ECC71", fg="#FFFFFF")
        self.home.place(x=10, y=10, height=40, width=80)

        # model Variable contains the model as a string "ANN" or "CNN"
        self.model = ""

        # Call the main frame to start the app
        self.Make_ModelFrame()

        # Load the app
        self.root.mainloop()

    def set_model_cnn(self):
        self.model = "cnn"
        self.ModelFrame.pack_forget()
        self.Make_MainFrame()
        print("Selected model: CNN")


    def Home(self):
        self.ModelFrame.pack()
        self.MainFrame.pack_forget()
        self.PhotoFrame.pack_forget()

    def Make_MainFrame(self):
        self.MainFrame.configure(bg="#34495E")

        for i in range(4):
            self.MainFrame.grid_rowconfigure(i, weight=1)  # Allow rows to expand vertically
        self.MainFrame.grid_columnconfigure(0, weight=1)  # Allow column to expand horizontally

        # the label on the top
        self.Mainlabel = tk.Label(self.MainFrame, text="Choose Input Type", font=("Arial", 36), bg="#34495E", fg="#FFFFFF")

        '''
            - each button when you click it, Calls the new frame and makes the MainFrame invisible
            - each frame calls the Make_ModelFrame that is responsible for choosing the model
        '''
        self.PhotoButton = tk.Button(self.MainFrame, text="Photo", font=("Arial", 24), command=self.Make_PhotoFrame,
                                     bg="#3498DB", fg="#FFFFFF")


        self.Mainlabel.pack(pady=80)
        self.PhotoButton.pack(pady=30)


        self.MainFrame.pack()

    def Make_ModelFrame(self):
        self.ModelFrame.configure(bg="#34495E")

        self.Modellabel = tk.Label(self.ModelFrame, text="Choose Model", font=("Arial", 36), bg="#34495E", fg="#FFFFFF")

        self.ModelCNN = tk.Button(self.ModelFrame, text="CNN", font=("Arial", 24), command=self.set_model_cnn,
                                  bg="#3498DB", fg="#FFFFFF")

        self.Modellabel.pack(pady=100)
        self.ModelCNN.pack(pady=30)

        self.ModelFrame.pack()

    def open_photo_explorer(self):
        file_path = filedialog.askopenfilename(title="Select Photo",
                                               filetypes=[("Image Files", "*.jpg *.jpeg *.png")])

        # Update the photo path entry with the selected file path
        self.photo_path_entry.configure(state="normal")
        self.photo_path_entry.delete(0, tk.END)
        self.photo_path_entry.insert(0, file_path)
        self.photo_path_entry.configure(state="readonly")

        fer = COD(model_type=self.model)
        fer.image_use(file_path)


    def Make_PhotoFrame(self):
        self.MainFrame.pack_forget()

        # Set background color for PhotoFrame
        self.PhotoFrame.configure(bg="#34495E")

        # Button for browsing photo
        self.browse_photo_button = tk.Button(self.PhotoFrame, text="Browse Photo", font=("Arial", 20),
                                             command=self.open_photo_explorer, bg="#3498DB", fg="#FFFFFF")
        self.browse_photo_button.pack(pady=20)

        # Label to display selected photo path
        self.photo_path_label = tk.Label(self.PhotoFrame, text="Selected Photo Path:", font=("Arial", 16),
                                         bg="#34495E", fg="#FFFFFF")
        self.photo_path_label.pack(pady=10)

        # Placeholder for displaying the selected photo path
        self.photo_path_entry = tk.Entry(self.PhotoFrame, font=("Arial", 16), state="normal")
        self.photo_path_entry.pack(pady=10)

        self.PhotoFrame.pack()



GUI()
