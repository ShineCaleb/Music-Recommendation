import pandas as pd

from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


import warnings
warnings.filterwarnings('ignore')

Cluster_Data=pd.read_csv(r'D:\Project\Recommendation_Engine\Cluster_Data.csv')
Cluster_Data=Cluster_Data.drop(columns="Unnamed: 0")
Cluster_Data_first=Cluster_Data.copy()

ss=StandardScaler()
scaled_df=ss.fit_transform(Cluster_Data.drop(columns=["name","artists","cluster_label"]))

scaled_df=pd.DataFrame(scaled_df)
scaled_df["cluster_label"]=Cluster_Data["cluster_label"]
scaled_df.index=Cluster_Data_first["name"]

def get_reccomendation(song_name):
    
    if len(list(Cluster_Data_first[Cluster_Data_first['name']==song_name].index.values))==0:
        print('Sorry!! Song not available')
        
    else:
        index = int(Cluster_Data_first[Cluster_Data_first['name']==song_name].index.values)
        df = scaled_df[scaled_df['cluster_label']==scaled_df['cluster_label'][index]]
        
        distances = pd.DataFrame(data=pairwise_distances(X=df ,Y=None,metric='euclidean')).round(2)
        distances.index   = df.index # movie_data['userId'].unique()
        distances.columns = df.index
        
        rec_df = pd.DataFrame(distances[song_name])  #.sort_values(by=distances[name], ascending = True, axis=0)
        rec = rec_df.sort_values(song_name, axis = 0, ascending = True, inplace = False, na_position ='last')
        
        return pd.DataFrame(rec.iloc[1:20].index.values, columns=['Songs'])

Artist_Rec_Data=Cluster_Data_first.copy()

Artist_Rec_Data["artists"]=Artist_Rec_Data["artists"].str.replace("[", "")
Artist_Rec_Data["artists"]=Artist_Rec_Data["artists"].str.replace("]", "")
Artist_Rec_Data["artists"]=Artist_Rec_Data["artists"].str.replace("'", "")
Artist_Rec_Data["artists"]=Artist_Rec_Data["artists"].str.replace("\'", "")
Artist_Rec_Data["artists"]=Artist_Rec_Data["artists"].str.replace("\(", "")
Artist_Rec_Data["artists"]=Artist_Rec_Data["artists"].str.replace("\)", "")

Artist_Data=pd.read_csv(r"D:\Project\Recommendation_Engine\Artist_Data.csv")
Artist_Data=Artist_Data.drop(columns="Unnamed: 0")

def similar_Song_Artist(song_name):
    
    if len(list(Cluster_Data_first[Cluster_Data_first['name']==song_name].index.values))==0:
        print('Sorry!! Song not available')
        
    else:
        index = int(Artist_Rec_Data[Artist_Rec_Data['name']==song_name].index.values)
        Ar = Artist_Rec_Data.iloc[index,3]
        artist_name = Ar.split(",")
        
        if len(artist_name)==1:
            index = int(Artist_Data[Artist_Data['artists']==artist_name[0]].index.values)
            df = Artist_Data[Artist_Data['cluster_label']==Artist_Data['cluster_label'][index]]
        
            artist_index=df["artists"]
            distances = pd.DataFrame(data=pairwise_distances(X=df.drop(columns=["artists"]) ,Y=None,metric='euclidean')).round(2)
            distances.index   = artist_index
            distances.columns = artist_index
        
            art_df = pd.DataFrame(distances[artist_name])
            art = art_df.sort_values(artist_name, axis = 0, ascending = True, inplace = False, na_position ='last')

            Axe=pd.DataFrame(art.head(5).index)
        
        elif len(artist_name)==2:
            index = int(Artist_Data[Artist_Data['artists']==artist_name[0]].index.values)
            df = Artist_Data[Artist_Data['cluster_label']==Artist_Data['cluster_label'][index]]
        
            artist_index=df["artists"]
            distances = pd.DataFrame(data=pairwise_distances(X=df.drop(columns=["artists"]) ,Y=None,metric='euclidean')).round(2)
            distances.index   = artist_index
            distances.columns = artist_index
        
            art_df = pd.DataFrame(distances[artist_name])
            art = art_df.sort_values(artist_name, axis = 0, ascending = True, inplace = False, na_position ='last')
            
            Merged_Df=art.head(3)
            
            index = int(Artist_Data[Artist_Data['artists']==artist_name[1]].index.values)
            df = Artist_Data[Artist_Data['cluster_label']==Artist_Data['cluster_label'][index]]
        
            artist_index=df["artists"]
            distances = pd.DataFrame(data=pairwise_distances(X=df.drop(columns=["artists"]) ,Y=None,metric='euclidean')).round(2)
            distances.index   = artist_index
            distances.columns = artist_index
        
            art_df = pd.DataFrame(distances[artist_name])
            art = art_df.sort_values(artist_name, axis = 0, ascending = True, inplace = False, na_position ='last')
            
            Merged_Df=pd.concat(Merged_Df,art.head(2),axis=0)
            
            Axe= Merged_Df
        
        else:
            
            Axe= pd.DataFrame(artist_name)
            
        ar_names = []
        ar_song = []
        pop = []
        
        for j in Axe["artists"]:
            a = 0
            b = 0
            for i in Artist_Rec_Data["artists"]:
                if j.lower() in Artist_Rec_Data["artists"][a].lower():
                    ar_names.append(Artist_Rec_Data["artists"][a]) 
                    ar_song.append(Artist_Rec_Data["name"][a])
                    pop.append(Artist_Rec_Data["popularity"][a])
                    df = pd.DataFrame()
                    df['Songs']=ar_song
                    df['Artists']=ar_names
                    df['Popularity']=pop
                    df.sort_values('Popularity', axis=0, ascending=False, inplace=True)
                    b+=1
                a+=1
            if b == 0:
                print("Nothing found. Please try something else :)")
            Out=df.drop(columns=["Popularity"])
            df.drop_duplicates(inplace=True)
        return pd.DataFrame(Out)

def artist(song_name):
    if len(list(Artist_Rec_Data[Artist_Rec_Data['name']==song_name].index.values))==0:
        print('Sorry!! Song not available')
        
    else:
        index = int(Artist_Rec_Data[Artist_Rec_Data['name']==song_name].index.values)
        Ar = Artist_Rec_Data.iloc[index,3]
        Artists = Ar.split(",")
        Artists = Artists[0]
            
        return (Artists)

def Final_recommendations(song_name):
    if len(list(Artist_Rec_Data[Artist_Rec_Data['name']==song_name].index.values))==0:
        print('Sorry!! Song not available')
    else:
        try:
            a=get_reccomendation(song_name)
            list_a=[]
            for i in a["Songs"]:
                list_a.append(artist(i))
            a["Artists"]=list_a
            b=similar_Song_Artist(song_name)
            Final_Df=pd.concat([a,b], axis=0)
        except:
            a=get_reccomendation(song_name)
            list_a=[]
            for i in a["Songs"]:
                list_a.append(artist(i))
            a["Artists"]=list_a
            Final_Df=a
            
            return pd.DataFrame(Final_Df.sample(10))

from flask import *
import numpy as np
import pandas as pd

app = Flask(__name__)  
  
@app.route('/')  
def customer():  
   return render_template('Home.html')  

@app.route("/About")
def About():
    return render_template('About.html')

@app.route('/Rec',methods = ["POST", "GET"])  
# def print_data():  
#    if request.method == 'POST':  
#       result = request.form  
#       return render_template("result_data.html",result = result)
def html_table():
    if request.method == 'POST':
        result = request.form
        df=Final_recommendations(result["Song Name"])
        df.index=range(1,11)
        # return df.to_html(header="true", table_id="table")
        # return result
        return render_template("Rec.html",
        Song1=df["Songs"][1],
        Song2=df["Songs"][2],
        Song3=df["Songs"][3],
        Song4=df["Songs"][4],
        Song5=df["Songs"][5],
        Song6=df["Songs"][6],
        Song7=df["Songs"][7],
        Song8=df["Songs"][8],
        Song9=df["Songs"][9],
        Song10=df["Songs"][10],
        Artist1=df["Artists"][1],
        Artist2=df["Artists"][2],
        Artist3=df["Artists"][3],
        Artist4=df["Artists"][4],
        Artist5=df["Artists"][5],
        Artist6=df["Artists"][6],
        Artist7=df["Artists"][7],
        Artist8=df["Artists"][8],
        Artist9=df["Artists"][9],
        Artist10=df["Artists"][10]
        )

if __name__ == '__main__':  
   app.run(debug=True)
