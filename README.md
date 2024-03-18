# fall_technichal_project
As part of our AIBT master's program at Skema/Esiea, we had to create an application using content recommendation systems.

We opted for a "Tinder-like" application where movies are suggested to the user based on their preferences and those of similar users. The user can indicate whether they like or dislike the suggested movie, or ignore it if they are unfamiliar with it.

The team consisted of Mériadec de Kerhor and Paul Noyer.

![](https://github.com/clonck-man/fall_tech_project/blob/main/screen_example.png)

## Datas
The data comes from the IMDB website and was retrieved using the site's API.

The data was then transformed to be usable. Two files were produced:
- [movies_app.csv](https://github.com/clonck-man/fall_tech_project/blob/main/data/clean_datas/movies_app.csv) a reduced file containing only the movie IDs, their titles, and the partial URL of their poster in the IMDB database.
- [movies_tags.json](https://github.com/clonck-man/fall_tech_project/blob/main/data/clean_datas/movies_tags.json) a file containing tags associated with each movie.

The tags were obtained using NLP processes on the descriptions of each movie. In order, we:
- Removed special characters and converted the text to lowercase.
- Tokenized the text and removed stopwords.
- Lemmatized the text.
- Finally, we used TfidfVectorizer from sklearn to create a matrix of tags using the Term Frequency-Inverse Document Frequency concept. For each tag, its TF-IDF score is calculated by multiplying the frequency of a term (TF) in a document by the inverse frequency of the term in all documents (IDF).

Other transformations were attempted, but most did not yield satisfactory results during prediction tests.

We considered adding the list of actors and the director to the list of tags for each movie. This option was not tested due to time constraints.

## Models
Three recommendation systems have been implemented:
- A random system, which provides diversity to the recommendations and serves as an initial base for models that require user data to function.
- A system that uses the tags of movies liked by the user. The system creates a list of tags representing the user's tastes and their frequency. This list is compared to the tag dictionary in the [movies_tags.json](https://github.com/clonck-man/fall_tech_project/blob/main/data/clean_datas/movies_tags.json) file and ranks movies according to their similarity to the user's known tastes.
- A system that uses data from other users to create clusters (via the KNN object from sklearn). We identify the cluster of the current user, retrieve movies liked by users in the cluster, and recommend them to the current user.

![](https://github.com/clonck-man/fall_tech_project/blob/main/data/kpi_datas/kpi.png)

The performance displayed is not very reassuring at first glance. It should be noted that:
- This display does not take into account movies unknown to the user (which could therefore appeal to them without them being able to signal it).
- The tag system could be improved by adding the list of actors and the director to the list of tags for each movie.
- The recommendation system based on user similarities is limited by the lack of data. Each user was manually designed as part of a test. It would be necessary to build a larger database to achieve truly accurate results.

## App
The choice of a "Tinder-like" application quickly imposed itself on us for practical reasons. It is a type of interface that is easy to design with Python tools and has the merit of providing simple data to exploit (like/dislike).

The application is therefore designed in Python using the [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)library. It uses CSV and JSON files to function, as well as calls to the IMDB database to retrieve movie posters in real-time.

The files usable by the user are:
- The [app.py](https://github.com/clonck-man/fall_tech_project/blob/main/app.py) file, which allows the use of the application.
- The [data_kpi.ipynb](https://github.com/clonck-man/fall_tech_project/blob/main/data/kpi_datas/data_kpi.ipynb) file, which allows displaying the performance of the models.
- The [data_prep.ipynb](https://github.com/clonck-man/fall_tech_project/blob/main/data/raw_datas/data_prep.ipynb) file, which allows producing the "clean" files from the "raw" data retrieved from IMDB.
