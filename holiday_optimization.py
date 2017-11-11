''' Script to find the optimal location for a family holiday based on the locations of relatives and the 
number of people starting in each location. The algorithm minimizes the total number of miles traveled and 
plots a map of the starting locations (scaled by the number of people in a city) and the optimal destination.'''

import numpy as np
import scipy.optimize as optimize
from geopy.distance import vincenty
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# coordinate information and number of family members for each relevant city

Athens = [39.324389, -82.103139, 1.]
Columbus = [39.968660, -82.971611, 5.]
Pittsburgh = [40.444149, -79.961017, 1.]
Philadelphia = [40.028329, -75.280900, 3.]
DC = [38.910942, -77.013205, 2.]
Memphis = [35.099656, -89.954341, 2.]

places = [Athens, Columbus, Philadelphia, Pittsburgh, DC, Memphis]

def travel_distance(params):
	'''function to minimize total travel distance'''
	distance = 0.
	longitude, latitude = params 
	for location in places:
		distance += location[2] * (vincenty((location[0],location[1]), (longitude, latitude)).miles)
		return distance

initial_guess = [40, -85]
result = optimize.minimize(travel_distance, initial_guess)
fitted_params = result.x
print(fitted_params)

# set up the basemap extents

map = Basemap(projection='merc', lat_0 = 30, lon_0 = -90.,
    resolution = 'h', area_thresh = 0.1,
    llcrnrlon=-124.7844079, llcrnrlat=24.7433195,
    urcrnrlon=-66.9513812, urcrnrlat=49.3457868)

# plot the locations of family members

for location in places:
	lons = []
	lats = []
	lons = location[1]
	lats = location[0]
	#scale the marker according to number of family members in a city
	s = 3*location[2]
	x,y = map(lons, lats)
	map.plot(x, y, 'bo', markersize = s)

# plot the destination marker

lons_destination = fitted_params[1]
lats_destination = fitted_params[0]
x,y = map(lons_destination, lats_destination)
map.plot(x, y, 'r*', markersize=10)


import matplotlib.patches as mpatches
low = mpatches.Patch(color='blue', label='starting cities (scaled)')
high = mpatches.Patch(color='red', label='optimized destination')

map.drawcountries()
map.drawstates()
map.fillcontinents(color='beige',lake_color='lightblue')
map.drawmapboundary()
map.drawmapboundary(fill_color='lightblue')
plt.legend(handles=[low,high],title='Legend', loc = 3)
#plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
plt.title('Starting locations and optimized destination')
plt.show()

