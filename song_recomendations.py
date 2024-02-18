#STAGE 1
# user inputs a song and a mode: either choosing otehr 'hot songs' or 'spotify rec'
# if the song is in the cart - recommendation from the same chart, if not - can check the other chart or go to spotify rec

import numpy as np
import pandas as pd
import pickle
from sklearn import datasets # sklearn comes with some toy datasets to practice
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import json
from spotipy.oauth2 import SpotifyClientCredentials
import config #file with client_id and secret for the Spotify API
import spotipy
from IPython.display import IFrame
import pandas as pd
from bs4 import BeautifulSoup
import requests
import random

def user_input_song():
    song_input=input("input your favourite song:")
    print("")
    song_input=song_input.lower()
    k=0 #count of how many times we checked the charts
    return user_input_chart(song_input,k)

def user_input_chart(song,k):
    print("Got your song!")
    print("")
    print (f"We can check iTunes or Billboard, and if your song {song.upper()} is in top-100 recommend you other 'HOT' song")
    print("OR we can recommend you a similar song based on Spotify analysis")
    mode_choice=input("chose one of options. Billboard/iTunes/Spotify: ")
    mode_choice=mode_choice.lower()
    song_input=song
    k=k
    if mode_choice in ("itunes", "billboard"):
        if mode_choice=="itunes":
            return webscrap(mode_choice, song_input, k)
        else:
            return webscrap(mode_choice, song_input, k)
    elif mode_choice=="spotify":
        return search_spotify(song_input)
    else:
        print("sorry, don't understand you. Please, try again")
        return user_input_chart(song_input)

def soup_func(url):
    import requests
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    return soup
        
def webscrap(chart, song, k):
    import requests
    song_input=song
    chart_input=chart
    k=k
    if chart_input=="itunes":
        #webscrapping iTunes
        url="https://www.popvortex.com/music/charts/top-100-songs.php"
        response=requests.get(url)
        soup_i=soup_func(url)
        #creating a lits of songs
        list_songs_itunes=[]
        for song in soup_i.select("cite.title"):
            list_songs_itunes.append(song.get_text(strip=True))

            #creating a lits of artists
        list_artists_itunes=[]
        for artist in soup_i.select("em.artist"):
            list_artists_itunes.append(artist.get_text(strip=True))

            #creating a dataframe

        df=pd.DataFrame({"song": list_songs_itunes, "artist":list_artists_itunes})
        df['source']='itunes'

        return recommendation_stage_1(song_input, chart_input, df, k)
    else:
            #webscrapping billboard
        url="https://www.billboard.com/charts/hot-100/"
        response=requests.get(url)
        soup_b=soup_func(url)

            #creating a list of top-100 songs
        list_songs=[]
        for song in soup_b.select("div.chart-results-list h3#title-of-a-story.c-title.a-no-trucate.a-font-primary-bold-s.u-letter-spacing-0021"):
            list_songs.append(song.get_text(strip=True))

            #creating a list of top-100 artists for those songs
        list_art=[]
        for artist in soup_b.select("div.chart-results-list span.c-label.a-no-trucate.a-font-primary-s"):
            list_art.append(artist.get_text(strip=True))

            #creating a dataframe
        df=pd.DataFrame({"song": list_songs, "artist": list_art})
        df['source']='billboard'

        return recommendation_stage_1(song_input, chart_input, df, k)

def recommendation_stage_1(song, chart, df_to_check, k):
    i=0
    check=0
    k=k
    song=song
    df=df_to_check
    for song_from_list in df_to_check['song']:
        if song!=song_from_list.lower():
            i=i+1
        else:
            check=1
            break
   
    if check==0 and k==0:
        other_chart_check=input(f"sorry your chosen song is not in the {chart.upper()} chart, do you want to try the other chart? Yes or no: ")
        print("")
        if other_chart_check.lower()=="yes" and chart=="itunes":
            k+=1
            chart="billboard"
            return webscrap(chart, song,k)
        elif other_chart_check.lower()=="yes" and chart=="billboard":
            k+=1
            chart="itunes"
            return webscrap(chart, song,k)
        else:
            other_song_check=input(f"Do you want to check another song in {chart} chart maybe? yes/no:")
            if other_song_check.lower()=="yes":
                song_new=input(f"another song you want to check in {chart.upper()} chart:")
                song_new=song_new.lower()
                return recommendation(song_new, chart, df,k)
            else:
                spotify_check=input("Do you want to get recomendation based on Spotify analysis? yes/no: ")
                spotify_check=spotify_check.lower()
                if spotify_check=="yes":
                    return search_spotify(song)
                else:
                    print("okay, see you later")
    elif check==0 and k!=0:
        if chart=="billboard":
            chart="itunes"
        else:
            chart="billboard"
            
        stage2_check=input(f"Sorry, not in the other list either. Do you want to have a recomendation of a song from Spotify? yes/no:")
        if stage2_check.lower()=="yes":
            return search_spotify(song)
        else:
            print("whatever, see ya later!")
    else:
        print(f"The song you've inputed is in {chart.upper()} chart!")
        print("")
        random_song = random.choice(df_to_check['song'])
        if random_song!=song.lower():
            row_w_song=df_to_check[df_to_check['song']==random_song]
            artist=row_w_song['artist'].iloc[0]
            print("You may like another one from the same chart, try this one:", random_song.upper(), "by", artist.upper())
            print("")
            spotify_check=input("Do you still want to get recomendation based on Spotify analysis? yes/no: ")
            spotify_check=spotify_check.lower()
            if spotify_check=="yes":
                return search_spotify(song)
        else:
            random_song = random.choice(filtered_df['song'])
            row_w_song=df_to_check[df_to_check['song']==random_song]
            artist=row_w_song['artist'].iloc[0]
            print("You may like another one from the same chart, try this one:", random_song.upper(), "by", artist.upper())
            print("")
            spotify_check=input("Do you still want to get recomendation based on Spotify analysis? yes/no: ")
            spotify_check=spotify_check.lower()
            if spotify_check=="yes":
                return search_spotify(song)
        choice=input('Do you want to try again? yes/no:')
        if choice.lower()=='yes':
            return user_input_song()
        
        
        
#STAGE 2
#functions for Spitify check

def search_spotify(song):
    song_name=song
    result=sp.search(q=song_name,type="track",market="GB")
    song_id=result['tracks']['items'][0]['id']
    return extracting_AF(song_id)

def extracting_AF(song_id):
    song_af=pd.DataFrame(sp.audio_features(song_id))
    song_af=song_af.drop(['type', 'uri', 'track_href', 'analysis_url'], axis=1)
    song_af=song_af.set_index("id")
    return scaling_transform(song_af)

def scaling_transform(df):
    ids=df.index
    scaled_df=pd.DataFrame(scaler.transform(df), columns=df.columns)
    scaled_df=scaled_df.set_index(ids)
    return recomendation(scaled_df)

def recomendation(scaled_df):
    #getting the cluster
    cluster_for_rec=kmeans.predict(scaled_df)[0]
    #checking df with this cluster and extracting sample
    recomended_song=X_scaled_w_clusters[X_scaled_w_clusters['cluster']==cluster_for_rec].sample()
    recomended_song_id=recomended_song.index[0]
    #playing recommended song
    recomended_song_id = str(recomended_song_id)
    return IFrame(src="https://open.spotify.com/embed/track/"+recomended_song_id,
                 width="320", height="80", frameborder="0",allowtransparency="true",allow="encrypted-media")