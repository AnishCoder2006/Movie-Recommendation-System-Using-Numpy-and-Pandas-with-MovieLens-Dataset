import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

np.random.seed(42)

def load_preprocess_data():
    movies = pd.read_csv("C:\\Users\\ashwi\\OneDrive\\movies.csv")
    ratings = pd.read_csv("C:\\Users\\ashwi\\OneDrive\\ratings.csv")

    print(f"Loaded {len(movies)} movies and {len(ratings)} ratings")
    print("\nFirst few movies:")
    print(movies.head())

    return movies, ratings

def create_genre_matrix(movies):
    # One-hot encode genres
    genres = movies['genres'].str.get_dummies(sep='|')
    genre_matrix = pd.concat([movies[['movieId', 'title']], genres], axis=1)

    print(f"\nGenreMatrixShape: {genre_matrix.shape}")
    print("\nGenre Matrix Sample")
    print(genre_matrix.iloc[:5, :10])

    return genre_matrix, genres

def calculate_similarity(genres, movies):
    cosine_sim = cosine_similarity(genres)
    cosine_sim_df = pd.DataFrame(cosine_sim, index=movies['movieId'], columns=movies['movieId'])

    print(f"\nSimilarityMatrixShape: {cosine_sim_df.shape}")
    print("\nSimilarity sample for 'Toy Story (1995)':")
    toy_story_id = movies[movies['title'] == 'Toy Story (1995)']['movieId'].values[0]
    print(cosine_sim_df.loc[toy_story_id].sort_values(ascending=False).head(6))

    return cosine_sim, cosine_sim_df

def get_user_profile(user_id, ratings, genre_matrix):
    user_ratings = ratings[ratings['userId'] == user_id]
    user_profile = pd.merge(user_ratings, genre_matrix, on='movieId')
    genre_columns = genre_matrix.columns[2:]
    user_genre_preferences = {}

    for genre in genre_columns:
        user_genre_preferences[genre] = (user_profile[genre] * user_profile['rating']).sum()

    user_profile_vector = pd.Series(user_genre_preferences)
    user_profile_vector = user_profile_vector / user_profile_vector.sum()
    print(f"User {user_id} top genre preferences:\n")
    print(user_profile_vector.sort_values(ascending=False).head(10))

    return user_profile, user_profile_vector

def recommend_movies(user_id, movies, ratings, genre_matrix, cosine_sim_df, n_recommendations=10):
    user_ratings = ratings[ratings['userId'] == user_id]
    rated_movie_ids = user_ratings['movieId'].tolist()

    liked_movies = user_ratings[user_ratings['rating'] >= 4.0]
    liked_movie_ids = liked_movies['movieId'].tolist()

    if not liked_movie_ids:
        print(f"User {user_id} has no highly rated movies. Using all rated movies")
        liked_movie_ids = rated_movie_ids

    recommendations = []

    for idx, movie in movies.iterrows():
        if movie['movieId'] not in rated_movie_ids:
            movie_id = movie['movieId']
            movie_title = movie['title']

            similarities = []
            for liked_id in liked_movie_ids:
                if liked_id in cosine_sim_df.index and movie_id in cosine_sim_df.index:
                    sim = cosine_sim_df.loc[liked_id, movie_id]
                    similarities.append(sim)

            if similarities:
                avg_similarity = np.mean(similarities)
                recommendations.append({
                    'movieId': movie_id,
                    'title': movie_title,
                    'avg_similarity': avg_similarity,
                    'genres': movie['genres']
                })

    recommendations_df = pd.DataFrame(recommendations)
    recommendations_df = recommendations_df.sort_values('avg_similarity', ascending=False)

    return recommendations_df.head(n_recommendations)

def visualize_recommendations(user_id, recommendations, user_profile, genre_matrix):
    recommended_titles = recommendations['title'].tolist()
    rec_genres = genre_matrix[genre_matrix['title'].isin(recommended_titles)]

    genre_columns = rec_genres.columns[2:]
    if len(rec_genres) < 2:
        print("Not enough recommendations for PCA visualization.")
        return

    # Standardize genre data
    scaler = StandardScaler()
    genre_data_scaled = scaler.fit_transform(rec_genres[genre_columns])

    # PCA
    pca = PCA(n_components=2)
    genre_2d = pca.fit_transform(genre_data_scaled)

    # Add jitter for better visualization
    jitter = np.random.normal(0, 0.08, genre_2d.shape)
    genre_2d_jittered = genre_2d + jitter

    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(genre_2d_jittered[:, 0], genre_2d_jittered[:, 1], s=200, alpha=0.7)

    # Add labels (show only first 10 to avoid clutter)
    for i, title in enumerate(rec_genres['title']):
        if i < 10:
            plt.annotate(title[:20] + '...', (genre_2d_jittered[i, 0], genre_2d_jittered[i, 1]), fontsize=8, alpha=0.8)

    plt.title(f'Movie Recommendations for User {user_id} (PCA of Genres, Spread Out)')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    movies, ratings = load_preprocess_data()
    genre_matrix, genres = create_genre_matrix(movies)
    cosine_sim, cosine_sim_df = calculate_similarity(genres, movies)
    user_id = 7
    user_profile, user_preferences = get_user_profile(user_id, ratings, genre_matrix)
    recommendations = recommend_movies(user_id, movies, ratings, genre_matrix, cosine_sim_df, n_recommendations=15)

    print(f"\n===Top 15 Recommendations for User {user_id}===")
    for i, (idx, row) in enumerate(recommendations.iterrows(), 1):
        print(f"{i:2d}. {row['title']}")
        print(f" Similarity: {row['avg_similarity']:.3f}, Genres: {row['genres']}")
        print()

    try:
        visualize_recommendations(user_id, recommendations, user_profile, genre_matrix)
    except Exception as e:
        print(f"Visualization skipped due to: {e}")

if __name__ == "__main__":
    main()