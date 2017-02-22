import csv
import numpy as np
import matplotlib.pyplot as plt


srt_year=1976 #data starting point
n_year=40 #data length
cnt =0


cities = ["Ishikari","Wakkanai","Aomori","Sakata","Toyama","Matsumoto","Kyoto","Yonago","Hamada","Fukuoka"] #name of the data points
index = [0,0,0,0,0,0,0,0,0,0] #indexing data names colum possition in csv file

mtx = np.zeros((len(cities),2,n_year+1))#3D matrix for the results
#indexing cities names in csv file
while cnt <len(cities):
	index[cnt] = (3+(4*cnt))

	cnt+=1


#read csv file
def cell(x, y):
    with open('snow_data.csv', 'r') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                val = n[x]
                return val
            y_count += 1

#calculate average given a city name and a year
def avg(city,year):

	pos = cities.index(city)
	col = index[pos]-2
	upp = year_range_up(year)
	low = year_range_low(year)
	average=0
	
	for x in range(low,upp):
		
		if bool(cell(col,x)):
				average += float(cell(col,x))
		

	average = average/(upp-low+1)
	print average
	return average
#find the staring row for a giving year in the cvs file
def year_range_low(year):
	
	low =(int(year)-srt_year)*365
	
	while  cell(0,low)[4:]!=year:
			low+=1
	
	return low+1
#find the last row for a giving year in the cvs file
def year_range_up(year):
	
	upp =year_range_low(year)
	year_upp = int(year)+1
	
	while cell(0,upp)[4:]!=str(year_upp):
		upp+=1
	return upp
#index the result of averaging the data for each city
def cities_to_matrix():

	for x in range(0,len(index)):
		for z in range(0,n_year):
			mtx[x][0][z]=  z+srt_year
			mtx[x][1][z]= avg(cities[x],str(z+srt_year))
			print "calculating "+ cities[x] + " "+ str(z+srt_year) + "..."
		#last data point	
		mtx[x][0][n_year]= srt_year+n_year
		mtx[x][1][n_year]= avg(cities[x],str(srt_year+n_year))
		print "calculating "+ cities[x] + " "+ str(srt_year+n_year) + "..."		
		print mtx

#start indexing
cities_to_matrix()

print mtx


print "slicing 3D matrix into 2D matrix..."

for x in range(0,len(index)):
	#extract the data for a given city from the 3D matrix to 2D matrix
	a = mtx[x,:,:]
	print a
	#get the x axis data for a given city 
	xaxi = a[0,:]
	xaxi.astype(int)
	#get the y axis data for a given city
	yaxi = a[1,:]
	fig = plt.figure(1)
	#plots the data for a given city
	with plt.style.context('fivethirtyeight'):
		plt.plot(xaxi,yaxi,marker="o", markerfacecolor="r",label=cities[x])
		plt.xticks(np.arange(srt_year, srt_year+45, 5.0))
		plt.xlabel('Year')
		plt.ylabel('Average snow fall (cm)')
		#adds legend to the plot
		legend = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

		
		frame = legend.get_frame()
		frame.set_facecolor('0.90')

		
		for label in legend.get_texts():
		    label.set_fontsize('large')

		for label in legend.get_lines():
		    label.set_linewidth(1.5) 

		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
		fig.savefig('samplefigure', bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.show()


