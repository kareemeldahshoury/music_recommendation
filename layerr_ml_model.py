import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random

# Open the dataset and prepare it for the model
df = pd.read_csv("filtered_user_track_interactions.csv")
df['userID'] = pd.factorize(df['userID'])[0] + 1

# Create a dataset that keeps the amount of likes each track has
likes_per_track = df.groupby('trackID')['liked'].sum().reset_index()

# Rename columns for clarity
likes_per_track.columns = ['trackID', 'total_likes']

# Create a user-item matrix 
user_item_matrix = df.pivot_table(index="userID", columns="trackID", values="liked")
# Replace all the NaN's in the user-item matrix with 0's
user_item_matrix = user_item_matrix.fillna(0)


# Calculate the user similarity using the cosine similatiry function
user_similatiry = cosine_similarity(user_item_matrix)

# Function that gets the best track recommendations for the user
def get_recommendations(user_id, user_similarity, user_item_matrix, n=8):
  # Checks if the user doesnt have any likes, thus they dont exist on the user-item matrix
  # and it they arent on the table then they get the top 8 liked tracks
  if user_id not in user_item_matrix.index:
    top_liked_tracks = likes_per_track.sort_values(by="total_likes", ascending=False)['trackID'].tolist()
    return random.sample(top_liked_tracks, 8)
  # Gets the user similarities
  user_similarities = user_similatiry[user_id - 1]

  # Find the n simialr users exculding the user
  top_users = np.argsort(user_similarities)[-n-1:-1][::-1]
  
  recommended_items = set()
  for user in top_users:
    # Checks if the similar user is in the user-item matrix
    if user in user_item_matrix.index:
      # Is the list of tracks not liked by the user
      unrated_by_user = user_item_matrix.loc[user_id] == 0
      # Is the list of tracks liked by the user with the most similarity
      rated_by_user = user_item_matrix.loc[user] > 0

      # Recommends tracks that are not liked by the user and are liked by the similar user
      items_to_recommend = user_item_matrix.columns[unrated_by_user & rated_by_user]
      # Adds the recommended tracks for this similar user to the list of tracks to recommend
      recommended_items.update(items_to_recommend)
  # Checks if there are less than 8 tracks to recommend
  num_to_sample = min(len(recommended_items), 8)
  # Randomizes the tracks to recommend
  random_recommendations = random.sample(list(recommended_items), num_to_sample)
  # Returns 8 tracks to recommend
  return list(random_recommendations)

if __name__ == "__main__":
  print(get_recommendations(1, user_similatiry, user_item_matrix))
  print(get_recommendations(2, user_similatiry, user_item_matrix))
  print(get_recommendations(3, user_similatiry, user_item_matrix))
  print(get_recommendations(4, user_similatiry, user_item_matrix))
  print(get_recommendations(5, user_similatiry, user_item_matrix))
  print(get_recommendations(6, user_similatiry, user_item_matrix))

