# SongRecommendationML-k-means-

the model works like this:
1. user inputs a song name he likes
2. user choses one of 3 modes:
    2.1 billboard - checking whether a song is in top-100 of billboard, and receiving a recomendation of a song from the same chart
    2.2 itunes - same idea with itunes chart
    2.3 spotify - receiving a recomendation based on ML model based on audiofeatures of songs from Spotify
3. if the song is not in the chosen chart - the user can chose:
    3.1 check the other chart
    3.2 check another song
    3.2 get a recommendation based on spotify ML model
4. when the recomendation based on chart is received, the user still can chose to get spotify ML model recomendation

ML model is built on >4.5k songs from spotify. It's based on audiofeatures, not genres

for reading convenience purposes all functions are defined within .pynb file
