This is an algorithm to give track recommendations for a music site. The algorithm is a user-item collaborative filtering algorithm. It works by taking the tracks the user has liked and then finding users that have liked similar tracks and recommends tracks that users with a similar taste have liked that the user has not liked. The algorithm uses a cosine similarity function to calculate the users that are most similar to the current user and creates a list with the most similar users appearing at the beginning of the list. The algorithm then loops through the list of similar users and finds the songs liked by those users that the current user hasnt liked and adds them to a list of songs to recommend the user. The algorithm returns 8 songs that similar users have liked that the current user has not liked.



Future Additions:
1. Once there are a bigger number of users on the music site I will add a feature that takes only the top 5 most similar users to pull tracks from.

