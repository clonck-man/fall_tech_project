import pandas as pd
from collections import Counter, defaultdict


class recommandation_engine:
    def __init__(self):
        pass

    def predict(self):
        pass

    def predict_selection(self, selection_size=10):
        pass


class random_engin(recommandation_engine):
    def __init__(self, datas: pd.DataFrame):
        super().__init__()
        self.datas = datas

    def predict(self):
        return self.datas.sample(n=1)

    def predict_selection(self, selection_size=10):
        return self.datas.sample(n=selection_size)


class tag_engine(recommandation_engine):
    def __init__(self, datas, movies_tags, recommandations_results, known_ids):
        super().__init__()

        self.datas = datas
        self.movies_tags = movies_tags
        self.user_tags = self.get_user_tags(recommandations_results)

        self.known_ids = known_ids

        self.selection = self.create_selection()

    def get_user_tags(self, liked_movies_df):
        if not isinstance(liked_movies_df, pd.DataFrame):
            return []

        liked_tags = []
        for movie_id, liked, _ in liked_movies_df.values:
            if liked:
                tags = self.movies_tags.get(movie_id, [])
                liked_tags.extend(tags)
        return liked_tags

    def predict(self):
        for s in self.selection:
            if s not in self.known_ids:
                return s

    def predict_selection(self, selection_size=10):
        res = []
        for s in self.selection:
            if s not in self.known_ids:
                res.append(s)

        return res[:selection_size]

    def create_selection(self):
        liked_tags_freq = Counter(self.user_tags)

        movie_scores = defaultdict(int)
        for movie_id, tags in self.movies_tags.items():
            for tag in tags:
                if tag in liked_tags_freq:
                    movie_scores[movie_id] += liked_tags_freq[tag]

        recommended_movies = sorted(movie_scores.keys(), key=lambda x: movie_scores[x], reverse=True)

        return recommended_movies

