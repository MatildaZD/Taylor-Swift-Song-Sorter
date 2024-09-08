import pandas as pd 
import numpy as np 
from kmeans3D import findK

df = pd.read_csv("spotify_taylorswift.csv",index_col=0) #makes sure not to include the
#first unnamed column

colsToDrop = ['artist','album','release_date']
df = df.drop(columns=colsToDrop) #drop artist because its all the same

columns = df.columns 


#THIS IS THE LINE THAT BREAKS THE CODE!!!!!!
#BELOW 

df = df[df["popularity"]>0] 

#Get rid of the voice memos - they will skew data 
#removes the rows with 0 popularity 


#Don't want to include albums because that makes it sort based on albums
#aka its boring --> trying to sort by genre and other stats 

"""
df_album = pd.get_dummies(df['album'],prefix="album")
df = df.join(df_album)
df = df.drop(columns = ['album'])

"""
df = df.reset_index()
SongNames = df['name']
df = df.drop(columns=['name'])
"""
#set dates 
def ChangeDashes(string):
	string = str(string)
	string = string.replace("-","")
	return float(string)
"""

""" Release date is similar to album - don't want values that are similar 
#trying to sort by genre 
cols = ["release_date"] 
df[cols] = df[cols].apply(np.vectorize(ChangeDashes))
"""
cols = ["length"]
df[cols] = df[cols]/60000
#convert length to decimal w minute 


data = np.array(df)

#print(data.shape)
finalGroupings = findK(data,5)


groups = finalGroupings[0]
number = finalGroupings[1]

for i in range(number):
	genre = []
	for j in range(len(groups)):
		if groups[j] == i:
			genre.append(SongNames[j])

	print(genre)







