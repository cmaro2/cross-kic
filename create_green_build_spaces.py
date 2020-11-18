import pandas as pd
from read_shapeFile import loadShapeFile


def green_build_join(all_spaces, merge_green_spaces, merge_build_spaces):

    if all_spaces:
        nums = []
        buildSpaces = pd.DataFrame([])
        greenSpaces = pd.DataFrame([])

        for i in range(21):
            if i < 9:
                nums.append('D0' + str(i+1))
            else:
                nums.append('D' + str(i+1))
        print('Creating build spaces and green spaces from all the census areas')
        for folder in nums:
            is_green = 1
            is_build = 1
            const = []
            greens = []
            try:
                buildingsUnderConstruction_shp = loadShapeFile('data/carto2/' + folder + '/03_EDIFICIO_EN_CONSTRUCCION_P.shp')
                const.append(buildingsUnderConstruction_shp)
            except:
                is_build = 0

            try:
                buildings_shp = loadShapeFile('data/carto2/' + folder + '/03_EDIFICIO_P.shp')
                const.append(buildings_shp)
            except:
                is_build = 0

            try:
                undefinedBuildings_shp = loadShapeFile('data/carto2/' + folder + '/03_EDIFICIO_INDEFINIDO_P.shp')
                const.append(undefinedBuildings_shp)
            except:
                is_build = 0

            if buildSpaces.empty:
                buildSpaces = pd.concat([buildings_shp, buildingsUnderConstruction_shp, undefinedBuildings_shp])
            else:
                if is_build:
                    buildSpaces = pd.concat([buildSpaces, buildings_shp, buildingsUnderConstruction_shp, undefinedBuildings_shp])
                else:
                    for shp in const:
                        buildSpaces = pd.concat([buildSpaces, shp])


            try:
                urbanGardens_shp = loadShapeFile('data/carto2/' + folder + '/11_HUERTO_URBANO_P.shp')
                greens.append(urbanGardens_shp)
            except:
                is_green = 0

            try:
                gardenAreas_shp = loadShapeFile('data/carto2/' + folder + '/11_ZONA_AJARDINADA_P.shp')
                greens.append(gardenAreas_shp)
            except:
                is_green = 0

            try:
                gardenInPatios_shp = loadShapeFile('data/carto2/' + folder + '/11_ZONA_AJARDINADA_SOBRE_PATIO_P.shp')
                greens.append(gardenInPatios_shp)
            except:
                is_green = 0

            if greenSpaces.empty:
                greenSpaces = pd.concat([gardenAreas_shp, gardenInPatios_shp])
            else:
                if is_green:
                    greenSpaces = pd.concat([greenSpaces, gardenAreas_shp, urbanGardens_shp, gardenInPatios_shp])
                else:
                    for shp in greens:
                        greenSpaces = pd.concat([greenSpaces, shp])

        buildSpaces.to_file('data/buildSpaces.shp', driver='ESRI Shapefile')
        greenSpaces.to_file('data/greenSpaces.shp', driver='ESRI Shapefile')

    else:
        if merge_green_spaces:
            # Load shapefiles of green and constructed areas
            urbanGardens_shp = loadShapeFile('data/Carto_1000/11_HUERTO_URBANO_P.shp')
            gardenAreas_shp = loadShapeFile('data/Carto_1000/11_ZONA_AJARDINADA_P.shp')
            gardenInPatios_shp = loadShapeFile('data/Carto_1000/11_ZONA_AJARDINADA_SOBRE_PATIO_P.shp')
            greenSpaces = pd.concat([urbanGardens_shp, gardenAreas_shp, gardenInPatios_shp])
            greenSpaces.to_file('data/greenSpaces.shp', driver='ESRI Shapefile')

        if merge_build_spaces:
            buildings_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_EN_CONSTRUCCION_P.shp')
            buildingsUnderConstruction_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_INDEFINIDO_P.shp')
            undefinedBuildings_shp = loadShapeFile('data/Carto_1000/03_EDIFICIO_P.shp')
            buildSpaces = pd.concat([buildings_shp, buildingsUnderConstruction_shp, undefinedBuildings_shp])
            buildSpaces.to_file('data/buildSpaces.shp', driver='ESRI Shapefile')
