# 🎬 Movie Recommendation System

A content-based movie recommendation system that suggests films based on genre similarity and user preferences using cosine similarity and PCA visualization.

## 🚀 Features

- **Content-Based Filtering**: Uses movie genres to calculate similarity
- **User Profile Analysis**: Builds personalized genre preferences for each user
- **Cosine Similarity**: Measures similarity between movies based on genre vectors
- **PCA Visualization**: 2D visualization of recommendation diversity
- **Customizable Recommendations**: Adjustable number of recommendations

## 📊 How It Works

1. **Data Loading**: Reads movie metadata and user ratings
2. **Genre Encoding**: One-hot encodes movie genres into feature vectors
3. **Similarity Calculation**: Computes cosine similarity between all movies
4. **User Profiling**: Analyzes user's rating history to determine genre preferences
5. **Recommendation Generation**: Suggests movies similar to user's highly-rated films
6. **Visualization**: Projects recommendations into 2D space using PCA

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
