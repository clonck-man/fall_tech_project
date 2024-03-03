from PIL import Image, ImageTk
import customtkinter as ctk
import os


def load_and_resize_image(path, width, height):
    original_image = Image.open(path)
    resized_image = original_image.resize((width, height))
    tk_image = ImageTk.PhotoImage(resized_image)
    tk_image.image = tk_image
    return tk_image  # test


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("450x625")
        self.resizable(False, False)
        self.title("MetaData Cleaner")

        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Row 1
        self.image_path = "technichal_issue.png"
        self.your_image = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path)), size=(333, 500))
        self.image_label = ctk.CTkLabel(master=self, image=self.your_image, text='')
        self.image_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        # Row 2
        self.dislike_btn = ctk.CTkButton(master=self, text="Dislike", command=self.dislike_btn,
                                         fg_color="red", hover_color="dark red")
        self.dislike_btn.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="ew")

        self.like_btn = ctk.CTkButton(master=self, text="Like", command=self.like_btn,
                                      fg_color="green", hover_color="dark green")
        self.like_btn.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky="ew")

        # Row 3
        self.unknown_btn = ctk.CTkButton(master=self, text="I don't know this movie", command=self.unknown_btn,
                                         fg_color="gray", hover_color="gray39")
        self.unknown_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def dislike_btn(self):
        print("dislike_btn : " + self.title)

    def like_btn(self):
        print("like_btn : " + self.title)

    def unknown_btn(self):
        print("unknown_btn : " + self.title)


if __name__ == '__main__':
    app = App()

    app.mainloop()
