import pandas as pd

import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

import numpy as np


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


def preprocess_text(text):
    try:
        text = re.sub('[^a-zA-Z0-9\s]', '', text)
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if len(word) > 2 and word.isalnum() and word not in stopwords.words('english') and word != '']
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(tokens)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return ''


def extract_tags(descriptions, min_df=5):
    preprocessed_descriptions = [preprocess_text(description) for description in descriptions]

    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 3), min_df=min_df)
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_descriptions)

    tags = tfidf_vectorizer.get_feature_names_out()

    return tags, tfidf_matrix


df_actors = pd.read_csv("D:/Documents/projets/fall_technichal_project/data/actors_top500_final.csv")
df_movies = pd.read_csv("D:/Documents/projets/fall_technichal_project/data/movies_details_top500_final.csv")
df_real = pd.read_csv("D:/Documents/projets/fall_technichal_project/data/realisators_top500_final.csv")

df_movies_drops = ["adult", "backdrop_path", "original_language", "original_title", "video", "overview"]

df_movies_bis = df_movies.drop(columns=df_movies_drops)

col_app = ["id", "title", "poster_path"]
df_movies_app = df_movies_bis.loc[:, col_app]

"""
print(df_actors.columns)
print(df_movies_bis.columns)
print(df_movies_app.columns)


tags, tfidf_matrix = extract_tags(df_movies["overview"])

for i, description in enumerate(df_movies["overview"]):
    print("Film:", description)
    print("Tags:", [tags[j] for j in tfidf_matrix[i].indices])
    print()

print(f"il y a {len(tags)} tags")
"""

tags, tfidf_matrix = extract_tags(df_movies["overview"])

df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=tags, index=df_movies["id"])
df_tfidf = df_tfidf.set_index(df_tfidf.index.astype(int)).sort_index()
print(df_tfidf)


actor_matrix = df_actors.set_index("Actor")
actor_matrix.index.name = None
actor_matrix = actor_matrix.T
actor_matrix = actor_matrix.set_index(actor_matrix.index.astype(int)).sort_index()
print(actor_matrix)

real_matrix = df_real.set_index("Realisator")
real_matrix.index.name = None
real_matrix = real_matrix.T
real_matrix = real_matrix.set_index(real_matrix.index.astype(int)).sort_index()
real_matrix = real_matrix.add_suffix(' as real')
print(real_matrix)

df_merged = df_tfidf.join(actor_matrix).join(real_matrix)
df_merged = df_merged.fillna(0)
print(df_merged)


df_test = (df_tfidf != 0).astype(int)
print(df_test)


def elbow_method(X, max_clusters=10):
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)

    # Calcul de la dérivée de l'inertie
    derivatives = np.diff(inertias, 2)
    # Recherche du point de coude
    elbow_index = np.argmax(derivatives) + 1

    # Tracé de la courbe de l'inertie
    plt.plot(range(1, max_clusters + 1), inertias, marker='o')
    plt.xlabel('Nombre de clusters')
    plt.ylabel('Inertie')
    plt.title('Méthode du coude')
    plt.axvline(x=elbow_index, color='red', linestyle='--', label='Point de coude')
    plt.legend()
    plt.show()

    return elbow_index


# Méthode de la silhouette
def silhouette_method(X, max_clusters=10):
    silhouette_scores = []
    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k)
        cluster_labels = kmeans.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        silhouette_scores.append(silhouette_avg)

    # Trouver le nombre optimal de clusters
    optimal_clusters = np.argmax(silhouette_scores) + 2

    # Tracé de la courbe de la silhouette
    plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
    plt.xlabel('Nombre de clusters')
    plt.ylabel('Score de silhouette')
    plt.title('Méthode de la silhouette')
    plt.axvline(x=optimal_clusters, color='red', linestyle='--', label='Nombre optimal de clusters')
    plt.legend()
    plt.show()

    return optimal_clusters


elbow_method(df_tfidf, 100)
silhouette_method(df_tfidf, 100)

