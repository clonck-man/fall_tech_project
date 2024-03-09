from PIL import Image, ImageTk
from io import BytesIO
import customtkinter as ctk
import os

from imdb.imdb import get_movie_poster
import pandas as pd

from recomendatio_engine.recomandation_engine import random_engin


def load_and_resize_image(path, width, height):
    original_image = Image.open(path)
    resized_image = original_image.resize((width, height))
    tk_image = ImageTk.PhotoImage(resized_image)
    tk_image.image = tk_image
    return tk_image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # prediction
        self.df_movies = pd.read_csv("data/movies_app.csv")
        self.recommandation_results = []
        self.known_ids = []

        # Engines
        self.random_engine = random_engin(self.df_movies)

        # datas
        self.current_movie_name = None
        self.current_movie_id = None
        self.current_movie_img_url = None
        self.current_reco_engine = None

        self.geometry("450x625")
        self.resizable(False, False)
        self.title("Technical Project - Movie Tinder")

        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Row 1
        self.image_path = "technichal_issue.png"
        # self.img = Image.open(BytesIO(get_movie_poster(self.df_movies["poster_path"].iloc[0])))
        self.your_image = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path)), size=(333, 500))
        # self.your_image = ctk.CTkImage(light_image=self.img, size=(333, 500))
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

        # end of setup
        self.get_new_movie()

    def get_new_movie(self):
        while True:
            prediction = self.random_engine.predict()
            current_movie_id = prediction["id"].iloc[0]

            if current_movie_id not in self.known_ids:
                break

        self.current_movie_id = current_movie_id
        self.current_movie_name = prediction["title"].iloc[0]
        self.current_movie_img_url = prediction["poster_path"].iloc[0]

        try:
            img = Image.open(BytesIO(get_movie_poster(self.current_movie_img_url)))
            self.your_image = ctk.CTkImage(light_image=img, size=(333, 500))
            self.image_label.configure(image=self.your_image)
        except Exception as e:
            print(f"Error changing image: {e}")

    def write_to_csv(self):
        file_path = "data/recommandation_results.csv"

        df = []
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path).values.tolist()
        df.extend(self.recommandation_results)

        self.recommandation_results = []

        pd.DataFrame(df).to_csv(file_path, index=False)

    def dislike_btn(self):
        self.recommandation_results.append([self.current_movie_id, False, "random"])
        self.known_ids.append(self.current_movie_id)
        self.write_to_csv()
        self.get_new_movie()

    def like_btn(self):
        self.recommandation_results.append([self.current_movie_id, True, "random"])
        self.known_ids.append(self.current_movie_id)
        self.write_to_csv()
        self.get_new_movie()

    def unknown_btn(self):
        self.known_ids.append(self.current_movie_id)
        self.get_new_movie()


if __name__ == '__main__':
    app = App()

    app.mainloop()
