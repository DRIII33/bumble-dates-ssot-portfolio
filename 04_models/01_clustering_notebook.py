# 04_models/01_clustering_notebook.py
# Behavioral Clustering Notebook

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Assume 'df' (features_for_modeling) is loaded from BigQuery
# Example of how it would be loaded in a Colab environment:
# from google.cloud import bigquery
# from google.colab import auth
# auth.authenticate_user()
# client = bigquery.Client(project='driiiportfolio')
# query = 'SELECT * FROM `driiiportfolio.bumble_portfolio.features_for_modeling`'
# df = client.query(query).to_dataframe()

# For this script, we'll assume 'df' is already loaded and available.
# If running standalone, ensure 'df' is loaded appropriately.

# --- 1. Exploratory Data Analysis (EDA) ---
print("
--- EDA: DataFrame Head ---")
display(df.head())

print("
--- EDA: DataFrame Info ---")
df.info()

print("
--- EDA: DataFrame Description ---")
display(df.describe())

print("
--- EDA: Missing Values ---")
display(df.isna().mean().sort_values(ascending=False))

print("
--- EDA: Intent Level Distribution ---")
display(df['intent_level'].value_counts(normalize=True))

print("
--- EDA: Verification Passed Distribution ---")
display(df['verification_passed'].value_counts(normalize=True))

# --- 2. Feature Preparation for Clustering ---
# Select numerical features relevant for clustering
cluster_features_cols = [
    'sessions_30d',
    'matches_30d',
    'date_suggestions_30d',
    'match_rate_30d',
    'swipe_to_match_ratio'
]

# Fill missing values (NaNs from SAFE_DIVIDE result in no activity) with 0
# Making a copy to avoid SettingWithCopyWarning
clustering_data = df[cluster_features_cols].fillna(0).copy()

print("
--- Feature Preparation: Clustering Data Head (after NaN fill) ---")
display(clustering_data.head())

# Scale the features using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(clustering_data)

print("
--- Feature Preparation: Scaled Features Shape ---")
print(X_scaled.shape)

# --- 3. K-Means Clustering ---
# Define number of clusters
n_clusters = 4

kmeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_SEED, n_init='auto')
df['cluster'] = kmeans.fit_predict(X_scaled)

print(f"
--- K-Means Clustering: {n_clusters} Clusters Created ---")
display(df['cluster'].value_counts().sort_index())

# --- 4. Cluster Profile Analysis ---
print("
--- Cluster Profiles: Mean Feature Values ---")
cluster_profile = df.groupby('cluster')[cluster_features_cols].mean().round(3)
display(cluster_profile)

print("
--- Cluster Profiles: Mean Verification Passed ---")
display(df.groupby('cluster')['verification_passed'].mean().round(3))

print("
--- Cluster Profiles: Intent Level Distribution ---")
display(df.groupby('cluster')['intent_level'].value_counts(normalize=True).unstack().round(3))

# --- 5. Visualization of Cluster Profiles ---
plt.figure(figsize=(12, 6))
sns.heatmap(cluster_profile.T, cmap='viridis', annot=True, fmt=".3f", linewidths=.5)
plt.title('Mean Feature Values by Cluster')
plt.xlabel('Cluster')
plt.ylabel('Feature')
plt.tight_layout()
plt.show()

print("
--- Clustering analysis complete. Clusters added to 'df' DataFrame.---")
