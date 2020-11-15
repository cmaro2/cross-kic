import numpy as np
from time import process_time


def indexes_calc(seccion, greenSpaces, buildSpaces):
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
            greenSpaceIndex.append(9999)

        try:
            greenSpaceDensity.append(green_space / seccion_polygon.area)
        except ZeroDivisionError:
            greenSpaceDensity.append(9999)

        try:
            greenSpaceBuiltSpaceRatio.append(green_space / built_space)
        except ZeroDivisionError:
            greenSpaceBuiltSpaceRatio.append(9999)

    # Add new columns to the ShapeFile containing the new calculated index
    seccion['GSIndex'] = np.array(greenSpaceIndex)
    seccion['GSDensity'] = np.array(greenSpaceDensity)
    seccion['GSBSRatio'] = np.array(greenSpaceBuiltSpaceRatio)
    return seccion


if __name__ == '__main__':
    print('fin')
