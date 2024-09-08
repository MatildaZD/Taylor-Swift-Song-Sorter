import numpy as np
import matplotlib.pyplot as plt 


def standardize(dataArray):
	length = dataArray.shape[1] #grab the number of rows 
	for i in range(length): 
		dataArray[:,i] -= min(dataArray[:,i]) #subtract min from all values 
		dataArray[:,i] = dataArray[:,i]/np.ptp(dataArray[:,i]) #divide by the range of values 
	return dataArray

#K-means algorithm
def k_means(dataArray, k):
	rows,d = dataArray.shape
	
	 #k = number of cluster centers 
	DistanceClusters = np.zeros((rows,d+1)) 
	#---Get Cluster Centers:---
	clusterCenters = np.zeros((k,d)) #create kxd Array
	indicies = np.random.choice(np.arange(0,rows), size=k, replace = False)
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
				clusterCenters[i] = clusteravgs[i]
		
		cluster = []

		#---Assign Points---
		for i in range(rows): 
			tempList = []
			tempData = dataArray[i] #set two points to be x1 and y1 from the data sets
			for j in range(k):
				tempCenters = clusterCenters[j] #set two points to be x2 and y2 from the k cluster centers
				dist = np.linalg.norm(tempData-tempCenters)#distance formula 
				tempList.append(dist)
				#grab index of the cluster of least distance 
				mini = min(tempList) 
				cluster = tempList.index(mini)
			
				DistanceClusters[i] = np.concatenate([dataArray[i],np.array([int(cluster)])])#distance and respective cluster
		"""	
		clusteravgs=np.zeros((k,d))
		for i in range(k):		
			points = dataArray[i==cluster]
			avg = points.mean()
			clusteravgs[i] = avg
		"""
		clusteravgs=np.zeros((k,d)) 
		avg = 0
		for i in range(k):
			temp = []
			for j in DistanceClusters: # 
					if j[d] == i: #if the cluster value is equal to i
						temp.append(j[:d]) #add it to a temporary list
					if len(temp) != 0:
						avg = sum(temp) / len(temp) #find the average of this list
					else:
						pass
					clusteravgs[i] = avg#append each cluster value to list of averages 
	
		#print(clusteravgs)
		OldPoints = clusterCenters #set old points to the cluster centers from beginning
		#of this looping turn 
		
		#Looked up how to compare all values of a numpy array 
		#this is the way to do it 
		comparison = OldPoints == clusteravgs	
		equal_Array = comparison.all()#uses the comparison made to check if every value is the same 
		flag = False #set flag to false so first set only happens one time 
	return (DistanceClusters,clusteravgs) #return two sets of data 
		#datapoints with their clusters
		#and the centers 

#sum of all of squared distances to their cluster centers
def SSE(KM):
	distList = []
	rows,cols = KM[0].shape #grab the shape of the data 
	centers = KM[1] #the center VALUES
	points_clusters = KM[0] #the data points and their clusters 
	for i in range(rows): #go through each row 
		tempData = points_clusters[i] 
		clusterNum = tempData[-1] #last value IS THE CLUSTER, going to
		#use this value to index the centers 
		

		tempData = tempData[0:cols-1] #CUT OFF CLUSTER VAL

		tempCenters = centers[int(clusterNum)] #set temp centers to value at cluster number 
		distance = np.linalg.norm(tempData-tempCenters) #calculate distance  
		distList.append(distance) #add it to list

	SSEsum = sum(distList) #find sum of list 

	return SSEsum #return sum 

#graph - elbow method 
def findK(data,choice): 
	cols = data.shape[1]
	clusterV = []
	yVals = []
	for i in range(1,13):
		if i == choice:
			temp = k_means(standardize(data),i)
			clusterV = temp[0][:,cols]
			yVals.append(SSE(temp))
		else:
			temp = k_means(standardize(data),i)
			yVals.append(SSE(temp))

	
	plt.scatter(np.arange(1,13),yVals)
	plt.plot(np.arange(1,13),yVals) 
	plt.show() #graph elbow 
	return clusterV,choice
	#return mindex+2 #accounting for the list as the ranges go down with 
	#subtracting - this happened twice - one for slope - one for differences of slops 



