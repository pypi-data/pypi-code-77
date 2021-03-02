import numpy as np
from xrmreader.reader import read_txrm_iterable, read_metadata
from scipy.ndimage import shift


def divide_by_reference(projections, reference):
    '''Homogenizes the background using a reference projection without object.

    :param projections: projections
    :param reference: reference projection
    :return:
    '''
    projections = np.divide(projections, reference)
    return projections


def revert_shifts(projections, x_shifts, y_shifts):
    '''

    :param projections: projection data
    :param x_shifts: x shift parameter per projection
    :param y_shifts: y shift parameter per projection
    :return: shift corrected porjections
    '''
    num_projections, img_size_x, img_size_y = projections.shape
    shifts = np.zeros((num_projections, 2))
    shifts[:, 0] = x_shifts
    shifts[:, 1] = y_shifts

    # warp each projection
    for i in range(num_projections):
        # T = np.float32([[1, 0, shifts[i, 0]], [0, 1, shifts[i, 1]]])
        # projections[i, :, :] = cv2.warpAffine(projections[i, :, :], T, (img_size_x, img_size_y))

        # input is extended by repeating its last value to avoid zeros after cropping
        projections[i, :, :] = shift(projections[i, :, :], (shifts[i, 1], shifts[i, 0]), mode='nearest')
        if (projections[i, :, :] == 0).any():
            import matplotlib.pyplot as plt
            plt.imshow(np.squeeze(projections[i, :, :]))
            plt.show()

    return projections


def negative_logarithm(sinogram, epsilon=0.0001):
    ''' Conversion of sinogram to line integral domain.
    Needs to be done after shift correction.
    Type conversion to float might cause memory issues.

    :param epsilon: small number to make sure no zero or negative value occurs
    :param sinogram: sinogram as measured on detector
    :return: sinogram in line integral domain
    '''
    if (sinogram <= 0).any():
        sinogram[sinogram <= 0] = epsilon
    np.log(sinogram, out=sinogram)
    sinogram *= -1
    return sinogram


def downsample(projections, spatial_factor: int):
    '''

    :param projections: projections
    :param spatial_factor: factor for spatial downsampling
    :return: downsampled projections
    '''
    projections = projections[:, ::spatial_factor, ::spatial_factor]

    return projections


def truncation_correction(projections, extension_fraction=0.1):
    ''' Truncation correction on left/right detector side. Avoid bright rim at outer reco area.

    :param projections: projections
    :param extension_fraction: faction of image width to be added to both sides
    :return: extended projections
    '''
    # # todo: use simple numpy solution or implement https://pubmed.ncbi.nlm.nih.gov/10659736/ ??
    # # this is not noise-maintaining because no copy image content
    num_images, img_height, img_width = projections.shape
    n_ext = int(img_width * extension_fraction)
    projection = np.pad(projections, pad_width=((0, 0), (0, 0), (n_ext, n_ext)), mode='linear_ramp')
    return projection


def read_and_preprocess_txrm(projections_file, downsample_factor=1, do_truncation_correction=True,
                             extension_fraction=0.1, datatype=np.float32):
    '''Preprocess the raw images, i.e. remove shifts, transform into line integral domain.
    Projections are extended for truncation correction if needed.

    :param projections_file: Path to txrm projection file, images are loaded on-the-fly to avoid high memory consumption
    :param downsample_factor: factor by which the projections are downsampled spatially; 1 means no downsampling
    :param do_truncation_correction: whether or not truncation corrections should be applied to the projections
    :param extension_fraction: if truncation correction is applied -> which fraction of original image width is appended
    to both sides of the image
    :param datatype: numpy datatype to use for storing the projections; should be one of float16, float32, float64
    :return:
    '''
    metadata = read_metadata(str(projections_file))
    num_images = metadata['number_of_images']
    x_shifts = metadata['x-shifts']
    y_shifts = metadata['y-shifts']
    reference = metadata['reference']
    print('Preprocessing projections')
    if do_truncation_correction:
        projections = np.zeros((num_images,
                                int(np.ceil(float(metadata['image_height']) / downsample_factor)),
                                int(np.ceil(float(metadata['image_width']) / downsample_factor)) + 2 * int(
                                    np.ceil(float(metadata['image_width']) / downsample_factor) * extension_fraction)),
                               dtype=datatype)
    else:
        projections = np.zeros((num_images,
                                int(np.ceil(float(metadata['image_height']) / downsample_factor)),
                                int(np.ceil(float(metadata['image_width']) / downsample_factor))),
                               dtype=datatype)

    # todo: can this loop be parallelized without further memory consumption?
    for i, (projection, x_shift, y_shift) in enumerate(
            zip(read_txrm_iterable(str(projections_file)), x_shifts, y_shifts)):
        if i % 10 == 0:
            print(f'{i + 1} / {num_images}')
        projection = np.expand_dims(projection, 0)
        projection = divide_by_reference(projection, reference)
        projection = revert_shifts(projection, x_shift, y_shift)
        projection = downsample(projection, downsample_factor)
        projection = negative_logarithm(projection)
        if do_truncation_correction:
            projection = truncation_correction(projection, extension_fraction=extension_fraction)
        projections[i, :, :] = np.squeeze(projection)

    return projections
