import os
from osgeo import gdal
from tqdm import tqdm
from time import sleep


def _tiles_list(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + _tiles_list(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def _deleteFilesIn(dirName):
    import shutil
    dir_folder = dirName
    for filename in os.listdir(dir_folder):
        file_path = os.path.join(dir_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def IO(input_img, out_path, xsize, ysize, save_vrt=True):
    """
    :param input_img: Geographic raster data as input
    :param out_path: Output directory for tiles images
    :param xsize: Size of X dimension
    :param ysize: Size of Y dimension
    :param save_vrt: (optional) Save output tiles into VRT
    :return:
    """

    if xsize < 1 or ysize < 1:
        raise Exception(print("[ ERROR! ] width or height dimension should be more then 1px"))
    else:
        pass

    tile_size_x = xsize
    tile_size_y = ysize

    if not os.path.exists(out_path):
        os.mkdir(out_path)
    else:
        _deleteFilesIn(out_path)

    ds = gdal.Open(input_img)
    band = ds.GetRasterBand(1)
    x_size = band.XSize
    y_size = band.YSize

    # get only filename without extension
    output_filename = os.path.splitext(os.path.basename(input_img))[0]
    print(output_filename)

    count = 0
    for i in tqdm(range(0, x_size, tile_size_x), leave=False):
        for j in tqdm(range(0, y_size, tile_size_y), leave=False):
            count += 1
            translate_options = gdal.TranslateOptions(bandList=[1, 2, 3],
                                                      noData="none",
                                                      srcWin=[i, j,
                                                              tile_size_x,
                                                              tile_size_y])
            filename = os.path.join(out_path, str(output_filename) + "_" + str(count) + ".tif")
            gdal.Translate(filename, ds, options=translate_options)
            sleep(0.005)

    print(f'{count} tiles saved in {out_path}')

    if save_vrt:
        # Get the list of all files in directory tree at given path
        listOfFiles = _tiles_list(out_path)
        vrt_output = os.path.join(out_path, str(output_filename) + "_tiles_mosaic.vrt")
        vrt_opt = gdal.BuildVRTOptions(VRTNodata='none', srcNodata="NaN")
        gdal.BuildVRT(vrt_output, listOfFiles, options=vrt_opt)
