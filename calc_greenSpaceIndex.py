import numpy as np
from time import process_time
from read_shapeFile import loadShapeFile
from get_seccions import get_secciones_censales
from rtree import index


def indexes_calc2(seccion, greenSpaces, buildSpaces):
    # Crete arrays for the different calculated index
    greenSpaceIndex = []
    greenSpaceDensity = []
    greenSpaceBuiltSpaceRatio = []
    tic = process_time()

    # Loop to calcaulate the different indexes for each census area
    for i in range(len(seccion.index)):
        # Calcualte process time
        if (i + 1) % round(len(seccion.index) / 10) == 0:
            toc = process_time()
            print('Done with ' + str(i + 1) + '/' + str(
                len(seccion.index)) + ' census. Time in this cicle: ' + str(toc - tic))
            tic = process_time()

        seccion_polygon = seccion['geometry'][i]
        green_space = 0
        built_space = 0

        # Calculate the area of green and build space for each census
        for idx, greenSpaces_polygon in enumerate(greenSpaces['geometry']):
            try:
                if greenSpaces_polygon.intersects(seccion_polygon):
                    green_space += seccion_polygon.intersection(greenSpaces_polygon).area
            except:
                print('Ignored error in census number: ' + str(i) + ' and geometry number:' + str(idx))

        for id2, buildSpaces_polygon in enumerate(buildSpaces['geometry']):
            try:
                if buildSpaces_polygon.intersects(seccion_polygon):
                    built_space += seccion_polygon.intersection(buildSpaces_polygon).area
            except:
                print('Ignored error in census number: ' + str(i) + ' and geometry number:' + str(id2))

        # Make the calculations for each index, if there is any division by 0, 9999 will be added instead of the division
        try:
            greenSpaceIndex.append(green_space / seccion['Inhabitants'][i])
        except ZeroDivisionError:
            greenSpaceIndex.append(100)

        try:
            greenSpaceDensity.append(green_space / seccion_polygon.area)
        except ZeroDivisionError:
            greenSpaceDensity.append(100)

        try:
            greenSpaceBuiltSpaceRatio.append(green_space / built_space)
        except ZeroDivisionError:
            greenSpaceBuiltSpaceRatio.append(100)

    # Add new columns to the ShapeFile containing the new calculated index
    seccion['GSIndex'] = np.array(greenSpaceIndex)
    seccion['GSDensity'] = np.array(greenSpaceDensity)
    seccion['GSBSRatio'] = np.array(greenSpaceBuiltSpaceRatio)
    return seccion

def indexes_calc(section, greenSpaces, buildSpaces):
    # Crete arrays for the different calculated index
    greenSpaceIndex = []
    greenSpaceDensity = []
    greenSpaceBuiltSpaceRatio = []
    tic = process_time()
    idxGreen = index.Index()
    idxBuild = index.Index()

    # Populate R-tree index with greenSpaces and buildSpaces

    for pos, cell in enumerate(greenSpaces['geometry']):
        idxGreen.insert(pos, cell.bounds)

    for pos, cell in enumerate(buildSpaces['geometry']):
        idxBuild.insert(pos, cell.bounds)

    # Loop to calcaulate the different indexes for each census area
    for i, sectionPolygon in enumerate(section['geometry']):
        # Calcualte process time
        if (i + 1) % round(len(section.index) / 10) == 0:
            toc = process_time()
            print('Done with ' + str(i + 1) + '/' + str(
                len(section.index)) + ' census. Time in this cicle: ' + str(toc - tic))
            tic = process_time()

        green_space = 0
        built_space = 0
        sub_green = [greenSpaces['geometry'][pos] for pos in idxGreen.intersection(sectionPolygon.bounds)]
        sub_build = [buildSpaces['geometry'][pos] for pos in idxBuild.intersection(sectionPolygon.bounds)]
        # Calculate the area of green and build space for each census
        for gs in sub_green:
            green_space += sectionPolygon.intersection(gs.buffer(0)).area


        for bs in sub_build:
            built_space += sectionPolygon.intersection(bs.buffer(0)).area

        try:
            greenSpaceIndex.append(green_space / section['Inhabitants'][i])
        except ZeroDivisionError:
            greenSpaceIndex.append(100)

        try:
            greenSpaceDensity.append(green_space / sectionPolygon.area)
        except ZeroDivisionError:
            greenSpaceDensity.append(100)

        try:
            greenSpaceBuiltSpaceRatio.append(green_space / built_space)
        except ZeroDivisionError:
            greenSpaceBuiltSpaceRatio.append(100)

    # Add new columns to the ShapeFile containing the new calculated index
    section['GSIndex'] = np.array(greenSpaceIndex)
    section['GSDensity'] = np.array(greenSpaceDensity)
    section['GSBSRatio'] = np.array(greenSpaceBuiltSpaceRatio)
    return section


if __name__ == '__main__':
    greenSpaces = loadShapeFile('data/greenSpaces.shp')
    buildSpaces = loadShapeFile('data/buildSpaces.shp')
    sectionAreas = get_secciones_censales()
    sect = indexes_calc2(sectionAreas, greenSpaces, buildSpaces)

