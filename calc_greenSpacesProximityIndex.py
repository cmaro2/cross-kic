import numpy as np
from read_shapeFile import loadShapeFile
from time import process_time
from rtree import index


def greenProxInd(greenSpaces):
    idx = index.Index()
    min_prox_dist = 200
    tic = process_time()
    gsprox = []

    # Populate R-tree index with greenSpaces
    for pos, cell in enumerate(greenSpaces['geometry']):
        idx.insert(pos, cell.bounds)

    #Get circular buffers around greenSpaces
    #centroids = greenSpaces.geometry.centroid
    buffers = greenSpaces.geometry.buffer(min_prox_dist)

    size = len(greenSpaces.index)
    print('Starting calculations for greenSpaceProximity in greenSpaces')
    for num, gsbase in enumerate(greenSpaces['geometry']):
        distance = min_prox_dist
        gsIndex = 0
        if (num + 1) % round(size/10) == 0:
            toc = process_time()
            print('Green Proximity Index. Done with' + str(num + 1) + '/' + str(
                size) + ' census. Time in this cicle: ' + str(toc - tic))
            tic = process_time()

        sub_green = [greenSpaces['geometry'][pos] for pos in idx.intersection(buffers[num].bounds) if pos != num]

        for id1, green in enumerate(sub_green):
            if green.distance(gsbase) < distance <= min_prox_dist:
                distance = green.distance(gsbase)

        if distance != min_prox_dist:
            if distance > 1:
                gsIndex = gsbase.area / (distance * distance)
            else:
                gsIndex = gsbase.area

        gsprox.append(gsIndex)

    greenSpaces['proxIndex'] = np.array(gsprox)
    #greenSpaces.to_file('data/greenSpaces.shp', driver='ESRI Shapefile')
    print('Finished calculations for greenSpaceProximity in greenSpaces')
    return greenSpaces


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
        if (num + 1) % round(len(sectionAreas.index) / 10) == 0:
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
            avg = sum / len(sub_green)
        except ZeroDivisionError:
            avg = 0
        gsprox.append(avg)

    sectionAreas['prox_avg'] = np.array(gsprox)
    return sectionAreas


def proxToSection(sectionAreas, greenSpaces):
    prox_avg = []
    print('Starting calculations for proximity index inside section areas')

    idx = index.Index()
    for pos, cell in enumerate(greenSpaces['geometry']):
        idx.insert(pos, cell.bounds)

    for section in sectionAreas['geometry']:
        total = 0
        num = 0
        greenInSection = [greenSpaces['proxIndex'][pos] for pos in idx.intersection(section.bounds)]
        for ind in greenInSection:
            total += ind
            num += 1

        try:
            prox = total / num
        except ZeroDivisionError:
            prox = 0
        prox_avg.append(prox)

    sectionAreas['prox_avg'] = np.array(prox_avg)
    return sectionAreas


if __name__ == '__main__':

    # Load ShapeFiles of green areas and section areas
    greenSpaces = loadShapeFile('data/greenSpaces.shp')
    sectionAreas = loadShapeFile('out/indexes.shp')
    tic = process_time()
    sect = proxToSection(sectionAreas, greenSpaces)
    toc = process_time()
    print('Time:' + str(toc-tic))
    #greenSpaces.to_file('data/greenSpaces.shp', driver='ESRI Shapefile')
