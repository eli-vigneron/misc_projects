from math import radians, cos, sin, asin, sqrt
from itertools import combinations
import heapq
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.tools.plotting import scatter_matrix
#from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingRegressor
import time
import numpy as np
import seaborn
import matplotlib.pyplot as plt
import matplotlib.cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas
from pandas.tools.plotting import scatter_matrix
import time
import numpy as np
from mpl_toolkits.basemap import Basemap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.tools.plotting import scatter_matrix
#from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingRegressor
import time
import numpy as np
import seaborn
import matplotlib.pyplot as plt
import matplotlib.cm
from scipy.spatial import distance
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.tools.plotting import scatter_matrix
import time
import numpy as np
from mpl_toolkits.basemap import Basemap

def haversine(origin, destination):
    """
    Find distance between a pair of lat/lng coordinates
    """
    lat1, lon1, lat2, lon2 = map(radians, [origin[0],origin[1],destination[0],destination[1]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Metres
    return (c * r)

def formatted_pairs(origin, data):
    """
    Format list of coordinates into list of coordinate pairs containing
    the origin in the first entry
    """
    new_pairs = []
    pairs = list(combinations(data, 2))
    for i in pairs:
        if i[0] == origin or i[1] == origin:
            new_pairs.append(i)
    return new_pairs


def n_closest(origin, data, n):
    """
    returns the closes n points, origin is list, data list of lists of coordinates
    """
    pairs = formatted_pairs(origin, data)
    #heapq.heapify(pairs)
    five_smallest = heapq.nsmallest(
        n, pairs, key=lambda p: haversine(p[0], p[1]))

    # format the closest
    closest_coord = []
    for i in five_smallest:
        if i[0] == origin:
            closest_coord.append(i[1])
        if i[1] == origin:
            closest_coord.append(i[0])
    return closest_coord


data = [[53.547052, -113.491337],
        [53.539983, -113.499774],
        [53.539502, -113.502388],
        [53.540590, -113.502488],
        [53.539093, -113.503441],
        [53.545045, -113.494634],
        [53.545092, -113.492993],
        [53.541474, -113.490690],
        [53.540590, -113.502488]]

print(n_closest([53.539093, -113.503441], data, 3))

# convert the data back to dataframe
df = pd.DataFrame(data, columns=['lat', 'long'])

# graph it
plt.scatter(x = df['lat'], y = df['long'], marker='.', c='green', s=20)

df2 = pd.DataFrame(n_closest([53.545045, -113.494634], data, 3), columns=['Lat', 'Long'])
plt.scatter(x = df2['Lat'], y = df2['Long'], marker='.', c='red', s=20)

# distance between origin and farthest point of n-nearest
radius = distance.euclidean([53.545045, -113.494634], n_closest([53.545045, -113.494634], data, 3)[-1])


circle1=plt.Circle((53.545045, -113.494634), radius, color='y', fill=False)
plt.gcf().gca().add_artist(circle1)
plt.axes().set_aspect('equal', 'datalim')
plt.show()

# convert dataframe columns lat and long to list of lists
#df = pd.read_csv('Downtown Oliver Assessments Comm Office.csv')
#data = [list(i) for i in list(zip(df['Lat'].tolist(), df['Long'].tolist()))]


