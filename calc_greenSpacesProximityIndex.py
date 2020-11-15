import numpy as np
from read_shapeFile import loadShapeFile
from time import process_time
from rtree import index

def proxGreenSection(sectionAreas, greenSpaces):
    idx = index.Index()
    min_prox_dist = 200
    tic = process_time()
    gsprox = []

    # Populate R-tree index with greenSpaces
    for pos, cell in enumerate(greenSpaces['geometry']):
        idx.insert(pos, cell.bounds)

    for num, section in enumerate(sectionAreas['geometry']):
        sum = 0
        if (num + 1) % round(len(sectionAreas.index)/10) == 0:
            toc = process_time()
            print('Done with' + str(num + 1) + '/' + str(
                    len(sectionAreas.index)) + ' census. Time in this cicle: ' + str(toc - tic))
            tic = process_time()

        sub_green = [greenSpaces['geometry'][pos] for pos in idx.intersection(section.bounds)]
        for id1, green in enumerate(sub_green):
            distance = 200
            for i, green_area in enumerate(sub_green):
                if i != id1:
                    if green.distance(green_area) < distance <= min_prox_dist:
                        distance = green.distance(green_area)

            if distance != 200:
                try:
                    sum += green.area / (distance * distance)
                except ZeroDivisionError:
                    sum += green.area
        try:
            avg = sum/len(sub_green)
        except ZeroDivisionError:
            avg = 0
        gsprox.append(avg)

    sectionAreas['prox_avg'] = np.array(gsprox)
    return sectionAreas


def proxToSection(greenSpaces, sectionAreas):
    prox_avg = []

    print('Starting calculations for proximity index inside section areas')
    for section in sectionAreas['geometry']:
        sum = 0
        num = 0
        for i in range(len(greenSpaces.index)):
            if section.intersects(greenSpaces['geometry'][i]):
                sum += greenSpaces['proximityIndex'][i]
                num += 1
        try:
            prox = sum / num
        except ZeroDivisionError:
            prox = 0

        prox_avg.append(prox)

    sectionAreas['prox_avg'] = np.array(prox_avg)
    return sectionAreas

def prox_Ind(greenSpaces):
    # Crete arrays for the different calculated index
    prox_index = []
    # Minimum distance to which other green areas are checked
    min_prox_dist = 200
    tic = process_time()

    print('Starting calculations for proximity index')

    for idx, garden in enumerate(greenSpaces['geometry']):
        if ((idx + 1) % 5 == 0):
            toc = process_time()
            print('Done with ' + str(idx + 1) + '/' + str(
                len(greenSpaces.index)) + ' census. Time in this cicle: ' + str(toc - tic))
            tic = process_time()
        distance = 200



        for i, green_area in enumerate(greenSpaces['geometry']):
            if i != idx:
                distance = 1
                if garden.distance(green_area) < distance <= min_prox_dist:
                    distance = garden.distance(green_area)

        if distance == 200:
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

    # Load ShapeFiles of green areas and section areas
    greenSpaces = loadShapeFile('data/greenSpaces.shp')
    sectionAreas = loadShapeFile('out/indexes.shp')

    greenSpaces = proxGreenSection(sectionAreas, greenSpaces)


