import numpy as np
from read_shapeFile import loadShapeFile


def proxToCensal(greenSpaces, censalAreas):
    prox_avg = []
    print('Starting calculations for proximity index inside censal areas')
    for censal in censalAreas['geometry']:
        sum = 0
        num = 0
        for i in range(len(greenSpaces.index)):
            if censal.intersects(greenSpaces['geometry'][i]):
                sum += greenSpaces['proximityIndex'][i]
                num += 1
        try:
            prox = sum / num
        except ZeroDivisionError:
            prox = 0

        prox_avg.append(prox)

    censalAreas['prox_avg'] = np.array(prox_avg)
    return censalAreas

def prox_Ind(greenSpaces):
    # Crete arrays for the different calculated index
    prox_index = []

    # Minimum distance to which other green areas are checked
    min_prox_dist = 200

    print('Starting calculations for proximity index')
    for idx, garden in enumerate(greenSpaces['geometry']):
        distance = 10000

        for i, green_area in enumerate(greenSpaces['geometry']):
            if i != idx:
                if (garden.distance(green_area) < distance) and (garden.distance(green_area) <= min_prox_dist):
                    distance = garden.distance(green_area)

        if distance == 10000:
            prox = 0
        else:
            try:
                prox = garden.area/(distance * distance)
            except ZeroDivisionError:
                prox = garden.area

        prox_index.append(prox)

    print('Saving files')

    # Convert files to geoPandas GeoDataFrame and save them
    greenSpaces['proximityIndex'] = np.array(prox_index)

    print('Finished greenSpacesProximityIndex calculations')

    return greenSpaces

if __name__ == '__main__':

    # Load ShapeFiles of green areas and censal areas
    greenSpaces = loadShapeFile('data/greenSpaces.shp')
    censalAreas = loadShapeFile('out/indexes_try.shp')

    greenSpaces = prox_Ind(greenSpaces, censalAreas)


