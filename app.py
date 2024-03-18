from PIL import Image
from io import BytesIO
import customtkinter as ctk
import os

from imdb.imdb import get_movie_poster
import pandas as pd

from recomendation_engine.recomandation_engine import random_engin, tag_engine, user_engine

import json
import random


def json_int_keys_decoder(dictionary):
    return {int(key): value for key, value in dictionary.items()}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.df_movies = pd.read_csv("data/clean_datas/movies_app.csv")
        self.__init_interface__()

        # Recommandations
        self.recommandations = []
        self.nbr_recommandations = 10
        self.recommandation_results = []
        self.known_ids = []

        # datas
        self.current_recommandation = None

        self.get_new_movie()

    def __init_interface__(self):
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

    def __init_data__(self):
        with open('data/clean_datas/movies_tags.json', 'r') as f:
            self.movies_tags = json.load(f, object_hook=json_int_keys_decoder)

        if os.path.isfile("data/kpi_datas/recommandation_results.csv"):
            self.user_pref = pd.read_csv("data/kpi_datas/recommandation_results.csv")
            for id_ in self.user_pref["0"].tolist():
                if id not in self.known_ids:
                    self.known_ids.append(id_)
        else:
            self.user_pref = None

    def __init_engines__(self):
        self.random_engine = random_engin(self.df_movies)
        self.tag_engine = tag_engine(self.df_movies, self.movies_tags, self.user_pref, self.known_ids)
        self.user_engine = user_engine(self.df_movies, self.user_pref)

    # ===================================== #
    def get_random_recommandation(self):
        res = []
        known_ids = []

        for _ in range(self.nbr_recommandations):
            while True:
                recommandation = self.random_engine.predict()
                current_movie_id = recommandation["id"].iloc[0]

                if current_movie_id not in self.known_ids and current_movie_id not in known_ids:
                    break

            res.append(
                [
                    recommandation["id"].iloc[0],
                    recommandation["title"].iloc[0],
                    recommandation["poster_path"].iloc[0],
                    "random"
                ]
            )
            known_ids.append(current_movie_id)

        return res

    def get_tags_recommandation(self):
        res = []
        for id_ in self.tag_engine.predict_selection(self.nbr_recommandations):
            recommandation = self.df_movies.loc[self.df_movies['id'] == id_]
            res.append(
                [
                    recommandation["id"].iloc[0],
                    recommandation["title"].iloc[0],
                    recommandation["poster_path"].iloc[0],
                    "tag"
                ]
            )

        return res

    def get_user_recommandation(self):
        reco_ids = self.user_engine.predict_selection(self.nbr_recommandations)

        res = []
        for id_ in reco_ids:
            recommandation = self.df_movies.loc[self.df_movies['id'] == id_]

            res.append(
                [
                    recommandation["id"].iloc[0],
                    recommandation["title"].iloc[0],
                    recommandation["poster_path"].iloc[0],
                    "users"
                ]
            )
        return res

    def get_new_recommandations(self):
        if not isinstance(self.user_pref, pd.DataFrame):
            self.recommandations = self.get_random_recommandation()
            return

        res = []

        random_reco = self.get_random_recommandation()
        tag_reco = self.get_tags_recommandation()
        users_reco = self.get_user_recommandation()

        for random_rec, tag_rec, user_rec in zip(random_reco, tag_reco, users_reco):
            if random_rec[0] not in self.known_ids:
                res.append(random_rec)
            if tag_rec[0] not in self.known_ids:
                res.append(tag_rec)
            if user_rec[0] not in self.known_ids:
                res.append(user_rec)

            if len(res) >= self.nbr_recommandations:
                break

        random.shuffle(res)

        self.recommandations = res
    # ===================================== #

    def get_new_movie(self):
        if len(self.recommandations) <= 0:
            if len(self.recommandation_results) > 0:
                self.write_to_csv()

            self.__init_data__()
            self.__init_engines__()
            self.get_new_recommandations()

        self.current_recommandation = self.recommandations.pop(0)

        try:
            img = Image.open(BytesIO(get_movie_poster(self.current_recommandation[2])))
            self.your_image = ctk.CTkImage(light_image=img, size=(333, 500))
            self.image_label.configure(image=self.your_image)
        except Exception as e:
            print(f"Error changing image: {e}")

    # ===================================== #
    def write_to_csv(self):
        file_path = "data/kpi_datas/recommandation_results.csv"

        df = []
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path).values.tolist()
        df.extend(self.recommandation_results)

        self.recommandation_results = []

        pd.DataFrame(df).to_csv(file_path, index=False)

    def load_csv(self):
        if os.path.isfile("data/kpi_datas/recommandation_results.csv"):
            self.user_pref = pd.read_csv("data/kpi_datas/recommandation_results.csv")
            self.known_ids = self.known_ids.extend(self.user_pref["0"].tolist())
        else:
            self.user_pref = None

        self.tag_engine = tag_engine(self.df_movies, self.movies_tags, self.user_pref, self.known_ids)
    # ===================================== #

    # ===================================== #
    def dislike_btn(self):
        self.recommandation_results.append([self.current_recommandation[0], False, self.current_recommandation[3]])
        self.known_ids.append(self.current_recommandation[0])
        self.write_to_csv()
        self.get_new_movie()

    def like_btn(self):
        self.recommandation_results.append([self.current_recommandation[0], True, self.current_recommandation[3]])
        self.known_ids.append(self.current_recommandation[0])
        self.write_to_csv()
        self.get_new_movie()

    def unknown_btn(self):
        self.known_ids.append(self.current_recommandation[0])
        self.get_new_movie()
    # ===================================== #


if __name__ == '__main__':
    app = App()

    app.mainloop()
