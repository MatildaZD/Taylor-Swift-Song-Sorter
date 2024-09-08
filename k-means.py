import numpy as np
import matplotlib.pyplot as plt 
import random
import math

dataName = "clstrData3.txt" 



data = open(dataName, 'r')#open the file to read
listOfLines = data.readlines() #makes a list of each line 
length = len(listOfLines) #gets length of list 

dataArray = np.zeros((length,2)) #creates zeros array 


for i in range(0, len(listOfLines)): #for each line 
	line = listOfLines[i]
	linesplit = line.split() #split it by line breaks 
	x = linesplit[0] #x is the first value
	y = linesplit[1] #y is the second 
	dataArray[i]=[float(x),float(y)] #adds it to the data array at index i 

stand = True #if you want to standardize - set to true
if stand == True:
	x = dataArray[:,0]
	y = dataArray[:,1]
	x -= min(x)
	x = x / np.ptp(x) #numpy range function 
	
	y -= min(y)
	y = y / np.ptp(y) #do same for y


	dataArray=np.column_stack((x,y))


#K-means algorithm
def k_means(k): #k = number of cluster centers 
	Distance_clusterx = np.zeros((length,2)) #create empty arrays 
	Distance_clustery = np.zeros((length,2)) #for later 
	
	#---Get Cluster Centers:---
	clusterCenters = np.zeros((k,2)) #create kx2 Array
	indicies = np.random.choice(np.arange(0,length), size=k, replace = False)
	#creates a list of indices of size k with random choices from 0 to length

	OldPoints = None
	NewPoints = None 
	equal_Array = False
	flag = True

	while equal_Array != True:  
		if flag == True: #FIRST TIME - FLAG ENSURES THIS ONLY HAPPENS ONCE 
			for i in range(k):
				clusterCenters[i] = dataArray[indicies[i]] #uses the random indices to set intial cluster centers 
		else: #after first time we set the clusters to the new points 
			for i in range(k):
				clusterCenters[i] = NewPoints[i]
	

		#---Assign Points---
		for i in range(length): 
			tempList = []
			x1,y1 = dataArray[i] #set two points to be x1 and y1 from the data sets
			for j in range(k):
				x2,y2 = clusterCenters[j] #set two points to be x2 and y2 from the k cluster centers
				tempList.append(math.sqrt(((x1-x2)**2)+((y1-y2)**2))) #distance formula 

				#grab index of the cluster of least distance 
				mini = min(tempList) 
				cluster = tempList.index(mini)
			
			#arrays of the x and y values with their respective clusters 
			Distance_clusterx[i] = [dataArray[i][0],cluster] 
			Distance_clustery[i] = [dataArray[i][1],cluster]
		
		#---Find Average of Each Cluster for X Values---
		clusterXavgs = []
		for i in range(k):
			temp = []
			for j in Distance_clusterx:
				if j[1] == i: #if the cluster value is equal to i
					temp.append(j[0]) #add it to a temporary list
			if len(temp) != 0:
				avg = sum(temp) / len(temp) #find the average of this list
			else:
				pass
			clusterXavgs.append(avg) #append each cluster value to list of averages 


		#---Find Average of Each Cluster for Y Values (Same as x)---
		clusterYavgs = []
		for i in range(k):
			temp = []
			for j in Distance_clustery:
				if j[1] == i:
					temp.append(j[0])
			if len(temp) != 0:
				avg = sum(temp) / len(temp)
			else:
				pass
			clusterYavgs.append(avg)
		
		#---Grab New Points---
		NewPoints = np.zeros((k,2)) #create the new array of the new points
		for i in range(k):
			NewPoints[i][0] = clusterXavgs[i]
			NewPoints[i][1] =  clusterYavgs[i] 
		

		OldPoints = clusterCenters #set old points to the cluster centers from beginning
		#of this looping turn 
		
		#Looked up how to compare all values of a numpy array 
		#this is the way to do it 
		comparison = OldPoints == NewPoints
		equal_Array = comparison.all()#uses the comparison made to check if every value is the same 
		 
		flag = False #set flag to false so first set only happens one time 
	

	return (Distance_clusterx, Distance_clustery, NewPoints) #return three sets of data 
	#the xs and ys and their clusters and the final points 

def SSE(d):#sum of all of squared distances to their cluster centers 
	t = np.zeros((length,3))
	distList = []
	xs = d[0][:,0] #create variables for x and y
	ys = d[1][:,0]
	clusters = d[0][:,1] #grab the clusters 
	centers = d[2] #grab the center VALUES 

	for i in range(length): 
		t[i] = xs[i],ys[i],clusters[i] #make them all into 1 list 
	for i in t: #iterate through  
		x1 = i[0]
		x2 = centers[int(i[2]),0] #the center based on which cluster is assigned in var t
		y1 = i[1]
		y2 = centers[int(i[2]),1]

		distance = ((x1-x2)**2)+((y1-y2)**2) #calculate distance squared 
		distList.append(distance) #add it to list

	SSEsum = sum(distList) #find sum of list 

	return SSEsum #return sum 

def findK(): #elbow method 
	#up to six clusters (only 6 colors):
	yVals = []
	"""
	slopes = []
	differences = []
	"""
	for i in range(1,7):
		temp = k_means(i)
		yVals.append(SSE(temp))
	"""
	for i in range(1,6):
		slopes.append((yVals[i-1]-yVals[i])/-1)
	for i in range(1,5):
		differences.append(slopes[i-1]-slopes[i])
	minval = min(differences)
	mindex = differences.index(minval)
	"""
	plt.scatter(np.arange(1,7),yVals)
	plt.plot(np.arange(1,7),yVals) 
	plt.show() #graph elbow 
	#return mindex+2 #accounting for the list as the ranges go down with 
	#subtracting - this happened twice - one for slope - one for differences of slops 


findK()
k = 2 #arbitary - tried to set from findK but did not work 
temp = k_means(k)


colorList = ["b","r","g","m","y","k"]#setting up the different colors
for i in range(k):
	t1 = []
	t2 = []
	for j in temp[0]:
		if j[1] == i: #if the cluster value is equal to i
			t1.append(j[0]) #add it to temporary list 
	for j in temp[1]:
		if j[1] == i: 
			t2.append(j[0]) #do same for y values 
	plt.scatter(t1,t2,c=colorList[i], s=2) #graph it in a color from color list 
setPointsx = temp[2][:,0] #set up the found centers 
setPointsy = temp[2][:,1]
plt.scatter(setPointsx,setPointsy,c="k",marker='x',s=40) 
plt.show()




