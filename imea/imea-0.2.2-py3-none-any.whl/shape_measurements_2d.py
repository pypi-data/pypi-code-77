import numpy as np
import cv2
from skimage import measure, morphology, transform
from scipy import spatial, stats
import matplotlib.pyplot as plt
import pandas as pd


def extract_shape_measurements_2d(bw, spatial_resolution_xy_mm_per_px, dalpha=9, return_statistical_lengths_distributions=False, return_all_chords=False):
    """ Calculates 2D shape measurements of objects in a binary image.
    
        Args:
            bw (ndarry, bool): Binary image.
            spatial_resolution_xy_mm_per_px (float): Spatial resolution of image in [mm/pixel] to return values in [mm]. 
            dalpha (int/float, optional): Angle in degree [°] to turn bw each iteration. Should be a fraction of 180° (180°/``n``), 
                where ``n`` is a natural number.
            return_statistical_lengths_distributions (boolean, optional): If True then the statistical length are returned.
                Default is False.
            return_all_chords (boolean, optional): If True then all found chords are returned.
                Default is False.
        
        Returns:
            df_shape_measurements (Pandas Dataframe): Pandas dataframe including all 2D shape measurements currently supported by imea.
            dfs_statistical_lengths_distributions (list of Pandas Dataframes): A list of ``n`` pandas dataframes, where each
                panda dataframe includes the statistical lengths (columns) for all iterated angles (0°:dalpha:180°).
                Only returned if ``return_statistical_lengths_distributions`` is True.
            return_all_chords (ndarray): A numpy array of with all found chords for all angles.
                Only returned if ``return_all_chords`` is True.
    """
    
    assert type(bw) == np.ndarray, "bw should be an np.ndarray"
    assert len(bw.shape) == 2, "bw should be 2D array"
    assert bw.dtype == 'bool', "bw should be binary image"
    
    # Initialize results
    all_chords = np.array([])
    dfs_shape_measurements = []
    dfs_statistical_lengths_distributions = []
    
    # Label binary image to extract single objects
    labels, n_objects = measure.label(bw, return_num=True)    
    # Iterate over all objects
    for i in range(1,n_objects+1):
        bw_single = np.zeros(bw.shape)
        bw_single[labels == i] = True
        df_shape_measurements_single_object, df_statistical_lengths_distributions_single_object, all_chords_single_object = _shape_measurements_2d_single_object(bw_single, spatial_resolution_xy_mm_per_px, dalpha)
        dfs_shape_measurements.append(df_shape_measurements_single_object)
        dfs_statistical_lengths_distributions.append(df_statistical_lengths_distributions_single_object)
        all_chords = np.append(all_chords, all_chords_single_object)

    df_shape_measurements = pd.DataFrame(dfs_shape_measurements)
    
    # Return depending on settings
    if return_statistical_lengths_distributions == False and return_all_chords == False:
        return df_shape_measurements
    elif return_statistical_lengths_distributions == True and return_all_chords == False:
        return df_shape_measurements, dfs_statistical_lengths_distributions
    elif return_statistical_lengths_distributions == False and return_all_chords == True:
        return df_shape_measurements, all_chords
    else:
        return df_shape_measurements, dfs_statistical_lengths_distributions, all_chords


def _shape_measurements_2d_single_object(bw, spatial_resolution_xy_mm_per_px, dalpha):
    """ Calculates 2D rotation and translation invariant shape measurements of a binary image, containing one object.
    
    Args:
        bw (ndarray, bool): Binary image.
        spatial_resolution_xy_mm_per_px (float): Spatial resolution of image in [mm/pixel].
        dalpha (int/float): Angle in degree [°] to turn bw each iteration. Should be a fraction of 180° (180°/``n``), where ``n``
                is a natural number.
    Returns:
    
        df_shape_measurements_single_object_2d (Pandas Dataframe): Pandas dataframe with one row with shape measurements.
        df_statistical_lengths_distributions_single_object_2d (Pandas Dataframe): Pandas dataframe with statistical length at their
            measured angle.
        all_chords_single_object_2d (ndarray): Array of all found choords (for all rotations).
        
    Notes:
        Assumes: only one object per binary image.
    """

    ##### MARCRO DESCRIPTORS ##### 
    perimeter_2d, area_2d, filled_area_2d, convex_area_2d, major_axis_length_2d, minor_axis_length_2d, centroid_2d, coords_2d, bw_cropped , bw_convex_cropped = calc_skimage_measurements_2d(bw)

    # Contour (for further processing)
    contour_2d, contour_cv2_2d = calc_contour_list_2d(bw)

    # Circles
    max_inclosing_circle_center_2d, max_inclosing_circle_radius_2d = calc_max_inclosing_circle_2d(bw)
    min_enclosing_circle_center_2d, min_enclosing_circle_radius_2d = calc_min_enclosing_circle_2d(contour_2d)
    circumscribing_circle_radius_2d, inscribing_circle_radius_2d = calc_circumscribing_and_inscribing_circle_2d(centroid_2d, contour_2d)
    
    # use diameters instead of radii:
    max_inclosing_circle_diameter_2d = 2 * max_inclosing_circle_radius_2d
    min_enclosing_circle_diameter_2d = 2 * min_enclosing_circle_radius_2d
    circumscribing_circle_diameter_2d = 2 * circumscribing_circle_radius_2d
    inscribing_circle_diameter_2d = 2 * inscribing_circle_radius_2d

    # Statistical length
    # distributions
    feret_diameters_2d, martin_diameters_2d, nassenstein_diameters_2d, max_chords_2d, all_chords_2d, measured_angles_2d  = calc_statistical_length_distribution(bw_cropped, daplha=dalpha)
    # distribution parameters
    max_feret_2d, min_feret_2d, median_feret_2d, mean_feret_2d, mode_feret_2d, std_feret_2d = calc_distribution_parameters(feret_diameters_2d)
    max_martin_2d, min_martin_2d, median_martin_2d, mean_martin_2d, mode_martin_2d, std_martin_2d = calc_distribution_parameters(martin_diameters_2d)
    max_nassenstein_2d, min_nassenstein_2d, median_nassenstein_2d, mean_nassenstein_2d, mode_nassenstein_2d, std_nassenstein_2d = calc_distribution_parameters(nassenstein_diameters_2d)
    max_max_chords_2d, min_max_chords_2d, median_max_chords_2d, mean_max_chords_2d, mode_max_chords_2d, std_max_chords_2d = calc_distribution_parameters(max_chords_2d)
    max_all_chords_2d, min_all_chords_2d, median_all_chords_2d, mean_all_chords_2d, mode_all_chords_2d, std_all_chords_2d = calc_distribution_parameters(all_chords_2d)

    # Main and maximum dimensions
    x_max_2d, y_max_2d = calc_max_dimensions_2d(max_chords_2d, measured_angles_2d)
    width_min_bb_2d, length_min_bb_2d, center_bb_2d, cornerpoints_min_bb_2d = calc_min_2d_bounding_box_based_on_contour(contour_cv2_2d)

    # Equal diameters
    area_equal_diameter_2d = calc_area_equal_diameter_2d(area_2d)
    perimeter_equal_diameter_2d = calc_perimeter_equal_diameter_2d(perimeter_2d)

    # Geodatic length and thickness
    geodeticlength_2d, thickness_2d = calc_geodeticlength_and_thickness_2d(area_2d, perimeter_2d)


    ##### MESODESCRIPTORS ##### 
    convex_perimeter_2d = calc_convex_perimeter_2d(bw_convex_cropped)

    # Measurements based on erosion
    n_erosions_binary_image_2d = calc_n_erosions_to_erase_binary_img_2d(bw_cropped)
    n_erosions_complement_2d = calc_n_erosions_to_erase_binary_complement_2d(bw_cropped, bw_convex_cropped)


    ##### MICRODESCRIPTORS ##### 
    fractal_dimension_boxcounting_method_2d = calc_fractal_dimension_boxcounting_method_2d(bw_cropped)
    fractal_dimension_perimeter_method_2d = calc_fractal_dimension_perimeter_method_2d(contour_2d, max_feret_2d)

    shape_measurements_2d_mm = {
        "perimeter_2d_mm": perimeter_2d * spatial_resolution_xy_mm_per_px,
        "convex_perimeter_2d_mm": convex_perimeter_2d * spatial_resolution_xy_mm_per_px,
        "area_2d_mm2": area_2d * spatial_resolution_xy_mm_per_px**2,
        "filled_area_2d_mm2": filled_area_2d * spatial_resolution_xy_mm_per_px**2,
        "convex_area_2d_mm2": convex_area_2d * spatial_resolution_xy_mm_per_px**2,
        "major_axis_length_2d_mm": major_axis_length_2d * spatial_resolution_xy_mm_per_px,
        "minor_axis_length_2d_mm": minor_axis_length_2d * spatial_resolution_xy_mm_per_px,
        "max_inclosing_circle_diameter_2d_mm": max_inclosing_circle_diameter_2d * spatial_resolution_xy_mm_per_px,
        "min_enclosing_circle_diameter_2d_mm": min_enclosing_circle_diameter_2d * spatial_resolution_xy_mm_per_px,
        "circumscribing_circle_diameter_2d_mm": circumscribing_circle_diameter_2d * spatial_resolution_xy_mm_per_px,
        "inscribing_circle_diameter_2d_mm": inscribing_circle_diameter_2d * spatial_resolution_xy_mm_per_px,
        "x_max_2d_mm": x_max_2d * spatial_resolution_xy_mm_per_px,
        "y_max_2d_mm": y_max_2d * spatial_resolution_xy_mm_per_px,
        "width_min_bb_2d_mm": width_min_bb_2d * spatial_resolution_xy_mm_per_px,
        "length_min_bb_2d_mm": length_min_bb_2d * spatial_resolution_xy_mm_per_px,
        "area_equal_diameter_2d_mm": area_equal_diameter_2d * spatial_resolution_xy_mm_per_px, 
        "perimeter_equal_diameter_2d_mm": perimeter_equal_diameter_2d * spatial_resolution_xy_mm_per_px,
        "geodeticlength_2d_mm": geodeticlength_2d * spatial_resolution_xy_mm_per_px,
        "thickness_2d_mm": thickness_2d * spatial_resolution_xy_mm_per_px,
        "n_erosions_binary_image_2d": n_erosions_binary_image_2d,
        "n_erosions_complement_2d": n_erosions_complement_2d,
        "fractal_dimension_boxcounting_method_2d": fractal_dimension_boxcounting_method_2d,
        "fractal_dimension_perimeter_method_2d": fractal_dimension_perimeter_method_2d,    
        "max_feret_2d_mm": max_feret_2d * spatial_resolution_xy_mm_per_px,
        "min_feret_2d_mm_2d_mm": min_feret_2d * spatial_resolution_xy_mm_per_px,
        "median_feret": median_feret_2d * spatial_resolution_xy_mm_per_px,
        "mean_feret_2d_mm": mean_feret_2d * spatial_resolution_xy_mm_per_px,
        "mode_feret_2d_mm": mode_feret_2d * spatial_resolution_xy_mm_per_px,
        "std_feret_2d": std_feret_2d,
        "max_martin_2d_mm": max_martin_2d * spatial_resolution_xy_mm_per_px,
        "min_martin_2d_mm": min_martin_2d * spatial_resolution_xy_mm_per_px,
        "median_martin_2d_mm": median_martin_2d * spatial_resolution_xy_mm_per_px,
        "mean_martin_2d_mm": mean_martin_2d * spatial_resolution_xy_mm_per_px,
        "mode_martin_2d_mm": mode_martin_2d * spatial_resolution_xy_mm_per_px,
        "std_martin_2d": std_martin_2d,
        "max_nassenstein_2d_mm": max_nassenstein_2d * spatial_resolution_xy_mm_per_px,
        "min_nassenstein_2d_mm": min_nassenstein_2d * spatial_resolution_xy_mm_per_px,
        "median_nassenstein_2d_mm": median_nassenstein_2d * spatial_resolution_xy_mm_per_px,
        "mean_nassenstein_2d_mm": mean_nassenstein_2d * spatial_resolution_xy_mm_per_px,
        "mode_nassenstein_2d_mm": mode_nassenstein_2d * spatial_resolution_xy_mm_per_px,
        "std_nassenstein_2d": std_nassenstein_2d,
        "max_max_chords_2d_mm": max_max_chords_2d * spatial_resolution_xy_mm_per_px,
        "min_max_chords_2d_mm": min_max_chords_2d * spatial_resolution_xy_mm_per_px,
        "median_max_chords_2d_mm": median_max_chords_2d * spatial_resolution_xy_mm_per_px,
        "mean_max_chords_2d_mm": mean_max_chords_2d * spatial_resolution_xy_mm_per_px,
        "mode_max_chords_2d_mm": mode_max_chords_2d * spatial_resolution_xy_mm_per_px,
        "std_max_chords": std_max_chords_2d,
        "max_all_chords_2d_mm": max_all_chords_2d * spatial_resolution_xy_mm_per_px,
        "min_all_chords_2d_mm": min_all_chords_2d * spatial_resolution_xy_mm_per_px,
        "median_all_chords_2d_mm": median_all_chords_2d * spatial_resolution_xy_mm_per_px,
        "mean_all_chords_2d_mm": mean_all_chords_2d * spatial_resolution_xy_mm_per_px,
        "mode_all_chords_2d_mm": mode_all_chords_2d * spatial_resolution_xy_mm_per_px,
        "std_all_chords_2d": std_all_chords_2d 
    }

    statistical_lengths_distributions_2d_mm = {
        "measured_angles": measured_angles_2d,
        "feret_diameter_2d_mm": feret_diameters_2d * spatial_resolution_xy_mm_per_px,
        "martin_diameter_2d_mm": martin_diameters_2d * spatial_resolution_xy_mm_per_px,
        "nassenstein_diameter_2d_mm": nassenstein_diameters_2d * spatial_resolution_xy_mm_per_px,
        "max_chord_2d_mm": max_chords_2d * spatial_resolution_xy_mm_per_px
    }
    
    all_chords_single_object_2d_mm = all_chords_2d * spatial_resolution_xy_mm_per_px

    return shape_measurements_2d_mm, statistical_lengths_distributions_2d_mm, all_chords_single_object_2d_mm


def calc_skimage_measurements_2d(bw):
    """ Calculates object shape measurements based on ``skimage.measure.regionprops``.
    
    Args:
        bw (ndarray, boolean): Binary image describing an object shape. (True = object, False = background)
        
    Returns:
        area_2d (float): The 2D area of object.
        perimeter_2d (float): The 2D perimeter of object.
        convex_area_2d (float): The 2D convex area of object.
        major_axis_length_2d (float): The 2D major axis length of object.
        minor_axis_length_2d (float): The 2D minor axis length of object.
        centroid_2d (ndarray): The 2D centroid of object in shape ``[x, y]``.
        coords_2d (ndarray): A list of 2D coordinates of objects (indexes of binary images)
            in shape ``[[x0, y0], [x1, y1], ...]``.
    """
    
    labels = measure.label(bw)
    props = measure.regionprops_table(labels, properties=('area', 'filled_area', 'convex_area', 'major_axis_length', 'minor_axis_length', 'perimeter',
                                                          'coords', 'centroid', 'convex_image', 'image'))
    
    perimeter_2d = props['perimeter'][0]
    
    area_2d = props['area'][0]
    filled_area_2d = props['filled_area'][0]
    convex_area_2d = props['convex_area'][0]
    
    major_axis_length_2d = props['major_axis_length'][0]
    minor_axis_length_2d = props['minor_axis_length'][0] 
    
    centroid_2d = np.zeros((2,))
    centroid_2d[0], centroid_2d[1] = props['centroid-0'][0], props['centroid-1'][0]
    
    coords_2d = props['coords'][0]
    
    bw_cropped = props['image'][0]
    bw_convex_cropped = props['convex_image'][0]
    
    return perimeter_2d, area_2d, filled_area_2d, convex_area_2d, major_axis_length_2d, minor_axis_length_2d, centroid_2d, coords_2d, bw_cropped, bw_convex_cropped 


def calc_contour_list_2d(bw):
    """ Returns a list of **external** contour points of an object shape.
    
    Args:
        bw (ndarray, boolean): A binary image of the object shape.
        
    Returns:
        contour_2d (ndarray, int): A list of indexes of the contourpoints of object
            in the shape ``[[x0, y0], [x1, y1], [x2, y2]]``.
        contour_cv2_2d (list): Contour given is specific cv2 format for further processing.
    """
    
    # find contour
    # the try/except case handles different versions of cv2 (some return 2 some return 3 values)
    try:
        contour_cv2_2d, hierarchy = cv2.findContours(bw.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    except:
        try:
            _, contour_cv2_2d, hierarchy = cv2.findContours(bw.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        except:
            print("ERROR with cv2.findContours.")
    
    # transform list of contour points and change coordinate system to (x,y)
    contour_cv2_2d_reshaped = np.copy(contour_cv2_2d[0].reshape((-1,2)))
    contour_2d = np.zeros(contour_cv2_2d_reshaped.shape)
    contour_2d[:,0], contour_2d[:,1] = contour_cv2_2d_reshaped[:,1], contour_cv2_2d_reshaped[:,0]
    
    return contour_2d, contour_cv2_2d


def calc_max_inclosing_circle_2d(bw, pad_width=2):
    """ Calculates the maximum inclosing circle of an object shape.
    
    Args:
        bw (ndarray, boolean): Binary image of object (True = object, False = background).
        pad_width (int, optional): Padding width. Default is 2.
    Returns:
        center_2d (ndarray, float): center position of the maximum inclosing circle in shape ``[x, y]``.
        radius_2d (float): Radius of the maximum inclosing circle. 
    """
    
    # Apply padding
    bw = np.pad(bw, pad_width=pad_width, mode='constant', constant_values=False)
    
    distance_map = cv2.distanceTransform(bw.astype('uint8'), cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    radius_2d = np.amax(distance_map)
    idx_max_distance = np.where(distance_map==radius_2d)
    center_2d = np.zeros((2,))
    center_2d[0], center_2d[1] = idx_max_distance[0][0] - 1, idx_max_distance[1][0] - 1
    
    return center_2d, radius_2d


def calc_min_enclosing_circle_2d(contour_2d):
    """ Calculates the minimum enclosing circle of an object based on its list of coordinates.
    
    Args:
        contour_2d (ndarray, int/float): List of contour points describing an object in the shape ``[[x0, y0], [x1, y1], ...]``.
              Note: If float => converted to int.
    Returns:
        center_2d (ndarray, float): The center of the minium enclosing circle.
        radius_2d (float): The radius of the minium enclosing circle.    
    """
    
    # transform coordinates to cv2 representation:
    coords_cv2_2d = np.zeros(contour_2d.shape)
    coords_cv2_2d[:,0] = contour_2d[:,1]
    coords_cv2_2d[:,1] = contour_2d[:,0]
    
    coords_cv2_2d = (coords_cv2_2d.reshape((-1,2,1))).astype('int32')
    
    # find min enclosing circle
    center_cv2_2d, radius_2d = cv2.minEnclosingCircle(coords_cv2_2d)
    
    # convert to numpy array and transform to (x,y) coordinate system
    center_2d = np.zeros((2,))
    center_2d[0], center_2d[1] = center_cv2_2d[1], center_cv2_2d[0]
    
    return center_2d, radius_2d


def calc_circumscribing_and_inscribing_circle_2d(centroid_2d, contour_2d):
    """ Calculates the circumscribing and inscribing circle of an object shape.
    
    Args:
        centroid_2d (ndarray): Centroid of object in the shape ``[x,y]``.
        contour_2d (ndarray): Array describing the contour of object. Contour must have shape ``(n_contourpoints``,2)``.
    
    Returns:
        circumscribing_circle_radius_2d (float): The radius of the circumscribing circle.
            The circumscribing circle touches the contour from the outside, has the same centroid as the contour and minimum area.
        inscribing_circle_radius_2d (float): The radius of the inscribing circle.
            The circumscribing circle touches the contour from the inside, has the same centroid as the contour and maximum area.
            
    Notes:
        Uses ``scipy.spatial.distance.cdist`` to calculate distances.
    """
    
    distances = spatial.distance.cdist(centroid_2d.reshape((-1,2)), contour_2d, 'euclidean')
    distances = distances.reshape((-1))
    circumscribing_circle_radius_2d = max(distances)
    inscribing_circle_radius_2d = min(distances)
    
    # adjust borderline definition:
    inscribing_circle_radius_2d += 1
    
    return circumscribing_circle_radius_2d, inscribing_circle_radius_2d


def calc_area_equal_diameter_2d(area_2d):
    """ Calculates the areaequal diameter of an object.
    
    Args:
        area_2d (float): 2D Area of object.
        
    Returns:
        area_equal_diameter_2d (float): 2D Areaequal diameter of object.
    """
    
    return np.sqrt(4*area_2d/np.pi)


def calc_perimeter_equal_diameter_2d(perimeter_2d):
    """ Calculates the perimeter equal diameter of an object.
    
    Args:
        perimeter_2d (float): 2D perimeter of object.
        
    Returns:
        perimeter_equal_diameter_2d (float): 2D perimeterequal diameter of object.
    """
    return perimeter_2d/np.pi


def calc_geodeticlength_and_thickness_2d(area_2d, perimeter_2d):
    """ Calculates the geodeticlength and thickness of a shape based on its area and diameter.
    
    Args:
        area_2d (float): The 2D area of object.
        perimeter_2d (float): The 2D perimeter of object.
        
    Returns:
        geodeticlength_2d (float): The 2D geodetic length of object.
        thickness_2d (float): The 2D thickness of object.
        
    Notes:
        Calculation according to DIN ISO 9276-6: The geodetic lengths and thickness are approximated by an rectangle
        with the same area and perimeter:
        ``area_2d = geodeticlength_2d * thickness_2d``
        ``perimeter_2d = 2 * (geodeticlength_2d + thickness_2d)`` 
    
    """
    # helping variable: value under square root (see below)
    v = (perimeter_2d/4)**2 - area_2d
    
    # make sure value under squareroot is > 0
    v = max(v, 0)
    
    geodeticlength_2d = perimeter_2d/4 + np.sqrt(v)
    thickness_2d = perimeter_2d/2 - geodeticlength_2d
    
    return geodeticlength_2d, thickness_2d
    
    
def calc_min_2d_bounding_box_based_on_bw(bw): 
    """ Calculates the minimal bounding box of an image based on contours.
    
    Args:
        bw (ndarray): Binary image.
        
    Returns:
        width_min_bb_2d (float): The 2D width of the minimal bounding box.
        length_min_bb_2d (float): The 2D length of the minimal bounding box.
            (``length_min_bb_2d`` >= ``width_min_bb_2d``, ``length_min_bb_2d`` orthogonal to ``width_min_bb_2d``)
        center_bb_2d (ndarray, float): 2D Center of the minimal bounding box in shape ``[x,y]``.
        cornerpoints_min_bb_2d (ndarray, float): A list of the four cornerpoints of the minimal bounding box.
            In shape: ``[[x0, y0], [x1, y1], [x2, y2], [x3, y3]]``.
    
    """
    contour_2d, contour_cv2_2d = calc_contour_list_2d(bw)
    length_min_bb_2d, width_min_bb_2d, center_min_bb_2d, cornerpoints_min_bb_2d = calc_min_2d_bounding_box_based_on_contour(contour_cv2_2d)
    
    return length_min_bb_2d, width_min_bb_2d, center_min_bb_2d, cornerpoints_min_bb_2d  
    
def calc_min_2d_bounding_box_based_on_contour(contour_cv2_2d):    
    """ Calculates the minimal bounding box of an image based on contours.
    
    Args:
        contour_cv2 (ndarray): Contour as returned by ``cv2.findContours``.
        
    Returns:
        width_min_bb_2d (float): The width of the minimal 2D bounding box.
        length_min_bb_2d (float): The length of the minimal 2D bounding box.
            (``length_min_bb_2d`` >= ``width_min_bb_2d``, ``length_min_bb_2d`` orthogonal to ``width_min_bb_2d``)
        center_bb_2d (ndarray, float): Center of the minimal 2D bounding box in shape ``[x,y]``.
        cornerpoints_min_bb_2d (ndarray, float): A list of the four cornerpoints of the minimal bounding box.
            In shape: ``[[x0, y0], [x1, y1], [x2, y2], [x3, y3]]``.
    """
    
    # find minimal bounding box
    min_bb_rect_2d = cv2.minAreaRect(contour_cv2_2d[0])
    
    # extract width, length and center
    (center_bb_y_2d,center_bb_x_2d), (length_min_bb_2d, width_min_bb_2d), alpha_bb_2d = min_bb_rect_2d
    center_min_bb_2d = np.zeros((2,))
    center_min_bb_2d[0], center_min_bb_2d[1] = center_bb_x_2d, center_bb_y_2d
    
    # extract corner points
    box_cv2_2d = cv2.boxPoints(min_bb_rect_2d)
    cornerpoints_min_bb_2d = np.zeros((4,2))
    cornerpoints_min_bb_2d[:,0], cornerpoints_min_bb_2d[:,1] = box_cv2_2d[:,1], box_cv2_2d[:,0]
    
    # adjust borderline definition
    length_min_bb_2d += 1
    width_min_bb_2d += 1
    
    return length_min_bb_2d, width_min_bb_2d, center_min_bb_2d, cornerpoints_min_bb_2d   

def calc_convex_perimeter_2d(bw_convex):
    """ Calculates the 2D perimeter of the convex hull based on an binary image of the convex hull.
    
    Args:
        bw_convex (ndarray, boolean): Binary image of the convex hull.
        
    Returns:
        convex_perimeter_2d (float): 2D Perimeter of the convex hull.
    """
    labels = measure.label(bw_convex)
    props = measure.regionprops_table(measure.label(bw_convex), properties=('label','perimeter'))
    convex_perimeter_2d = props['perimeter'][0]
    return convex_perimeter_2d

def calc_n_erosions_to_erase_binary_img_2d(bw, pad_width=1, selem=None, return_list=False):
    """ Determines the number of erosions that are necessary to fully erase all True elements in a binary image.
    
    Args:
        bw (ndarray, boolean): Binary image.
        pad_width (int, optional): Number of False pixels to pad around the image. Default is 1.
            (If outer pixels are not False, this effects the number of erosions (depending on the neighborhood))
        selem (ndarray, optional): The neighborhood expressed as a 2-D array of ones and zeros.
            If None, use a cross-shaped structuring element (connectivity=1). Default is None.
            (this parameter is directly passed to skimage.morphology.binary_erosion)
        return_list(boolean, optional): If True, a list with the number of True pixels for each iteration is passed,
            if False, only the number of erosion (length of list) is returned. Default is False.
            
    Returns:
        n_erosions_2d (int) [if return_list == True]: Number of erosions to fully erase True pixels from image.
        n_true_pixels_list_2d (list) [if return_list == False]: a list with the number of True pixels for each iteration.    
    """
    
    # Apply padding
    bw_eroded = np.pad(bw, pad_width=pad_width, mode='constant', constant_values=False)
    
    n_true_pixels_list_2d = []
    n_true_pixels_list_2d.append(np.count_nonzero(bw_eroded))

    while n_true_pixels_list_2d[-1] > 0:
        bw_eroded = morphology.binary_erosion(bw_eroded)
        n_true_pixels_list_2d.append(np.count_nonzero(bw_eroded))
        
    n_erosions_2d = len(n_true_pixels_list_2d)
        
    if return_list == True:
        return n_true_pixels_list_2d
    else:
        return n_erosions_2d
    
    
def calc_n_erosions_to_erase_binary_complement_2d(bw_cropped, bw_convex_cropped, pad_width=1, selem=None, return_list=False):
    """ Number of erosions that are necessary to erase all pixels from the complement between the binary image of
        an object and the binary image of its convex hull.
        
    Args:
        bw (ndarray, boolean): Binary image of object.
        bw_convex_hull (ndarray, boolean): Binary image of the convex hull of object.
        pad_width (int, optional): Number of False pixels to pad around the image. Default is 1.
            (If outer pixels are not False, this effects the number of erosions (depneing on the neighborhood)).
        selem (ndarray, optional): The neighborhood expressed as a 2-D array of ones and zeros.
            If None, use a cross-shaped structuring element (``connectivity=1``). Default is None.
            (this parameter is directly passed to ``skimage.morphology.binary_erosion``).
        return_list(boolean, optional): If True, a list with the number of True pixels for each iteration is passed,
            if False, only the number of erosion (length of list) is returned. Default is False.
        
    Returns:
        n_erosions_2d (int) [if return_list == True]: Number of erosions to fully erase True pixels from image.
        n_true_pixels_list_2d (list) [if return_list == False]: a list with the number of True pixels for each iteration.    
    """
    assert bw_cropped.shape == bw_convex_cropped.shape, "Binary image and complement should have same shape, but have shape bw: {} and shape bw_complement: {}".format(bw.shape, bw_convex_hull.shape)
    
    bw_non_object = np.logical_not(bw_cropped)
    bw_complement = np.logical_and(bw_convex_cropped, bw_non_object)

    result = calc_n_erosions_to_erase_binary_img_2d(bw_complement, pad_width=pad_width, selem=selem, return_list=return_list)
    return result


def calc_statistical_length_distribution(bw, daplha):
    """ Calculates the statistical length (Feret-, Martin-, Nassenstein-diameter, chords and max chord) for a
        binary image in daplha degree steps.
        
    Args:
        bw (ndarray, bool): Binary image.
        dalpha (int/float): Rotation stepsize in degree (0 - 180°).

    Returns:
        feret_diameters (ndarray, int): Array of Feret diameters for each rotation.
        martin_diameters (ndarray, int): Array of Martin diameters for each rotation.
        nassenstein_diameters (ndarray, int): Array of Nassenstein diameters for each rotation.
        max_chords (ndarray, int): Array of maximum chord for each rotation.
        all_chords (ndarray, int): Array of all chords for each rotation.
        measured_angles (ndarray, float): Array of the rotated angles determinated by ``daplha``.
    """

    angles = np.arange(0,180,daplha)
    # introduce empty arrays
    feret_diameters_2d = np.zeros(angles.shape, dtype='int64')
    martin_diameters_2d = np.zeros(angles.shape, dtype='int64')
    nassenstein_diameters_2d = np.zeros(angles.shape, dtype='int64')
    max_chords_2d = np.zeros(angles.shape, dtype='int64')
    all_chords_2d = np.array([])

    # iterate over all angles
    for i, angle in enumerate(angles):
        # rotate image
        bw_rotated = transform.rotate(bw, angle, resize=True)
        # important: skimage.transform.rotate returns a greyscale image with values between 0 and 1 
        # => use simple thresholding to transform back to binary image
        bw_rotated = bw_rotated > 0.5

        # Feret diameter
        feret_diameters_2d[i], _ = calc_feret_diameter_2d(bw_rotated)

        # Martin diameter
        martin_diameters_2d[i], _ = calc_martin_diameter_2d(bw_rotated)

        # Nassenstein diameter
        nassenstein_diameters_2d[i], _ = calc_nassenstein_diameter_2d(bw_rotated)

        # Chords
        chords_2d, _ = calc_chords_2d(bw_rotated)
        max_chords_2d[i] = chords_2d.max()
        all_chords_2d = np.append(all_chords_2d, chords_2d)
        
        measured_angles_2d = angles
    return feret_diameters_2d, martin_diameters_2d, nassenstein_diameters_2d, max_chords_2d, all_chords_2d, measured_angles_2d 


def calc_distribution_parameters(distribution):
    """ Calculates characteristics of a distribution.
        
    Args: 
        distribution (ndarray): An array.
    Returns:
        max_value: max value in distribution.
        min_value: min value in distribution.
        median_value: median value in distribution.
        mean_value: mean value in distribution.
        mode: mode value in distribution (value that appears the most often in distribution).
        std: standard deviation of distribution.
    """
    distribution = distribution.ravel()    
    
    max_value = distribution.max()
    min_value = distribution.min()
    median_value = np.median(distribution)
    mean_value = np.median(distribution)
    mode, counts = stats.mode(distribution)
    mode = mode[0]
    std = np.std(distribution)
    
    return max_value, min_value, median_value, mean_value, mode, std
    

def calc_feret_diameter_2d(bw):
    """ Calculates the Feret diameter of an object (orthogonal to y-direction).

    Args:
        bw (ndarray, bool): Binary image.
        
    Returns:
        feret_diameter_2d (int): 2D Feret diameter.
        x_idx_2d (ndarray, int): x-coordinates of the two Feret calipers [x0, x1].
    """
    
    n_pixels_in_xdirection  = bw.shape[0]
    
    # "squeeze" bw in y-direction into one column
    n_true_pixels_in_ydirection = np.count_nonzero(bw, axis=1)
    
    # caliper from top    
    idx_first_nonzero_pixel = _first_nonzero(n_true_pixels_in_ydirection, axis=0)
    if idx_first_nonzero_pixel == -1:
        # no element found
        return 0
    
    # caliper from bottom
    n_true_pixels_y_reversed = n_true_pixels_in_ydirection[::-1]
    idx_first_nonzero_pixel_from_bottom = _first_nonzero(n_true_pixels_y_reversed, axis=0)
    idx_last_nonzero_pixel = n_pixels_in_xdirection - idx_first_nonzero_pixel_from_bottom
    
    # feret diameter
    feret_diameter_2d = idx_last_nonzero_pixel - idx_first_nonzero_pixel
    x_idx_2d = np.zeros((2,))
    x_idx_2d[0] = idx_first_nonzero_pixel
    x_idx_2d[1] = idx_last_nonzero_pixel
    return feret_diameter_2d, x_idx_2d


def calc_martin_diameter_2d(bw, area_share_from_bottom=0.5):
    """ Calculates the Martin diameter of an object (in y-direction).

    Args:
        bw (ndarray, bool): Binary image.
        area_share_from_bottom (float, optional): area share, where the Martin diameter is measured.
            Default is 0.5, the original definition of the Martin diameter.
        
    Returns:
        martin_diameter_2d (int): 2D Martin diameter.
        idx (ndarray, int): Indexes of the start (0) and endpoint (1) of the Martin diameter in shape ``[[x0,y0], [x1,y1]]``.
        
    Notes:
        The original Martin diameter is is measured at the x-position, where the object is split into 50% / 50% area share.
        However, we can also calculate a diameter at a flexible area share. This is given by ``area_share_from_bottom``:
        ``area_share_from_bottom = 1 - area_share_from_top``
    """
    if area_share_from_bottom == 0 or area_share_from_bottom == 1:
        return 0
    elif area_share_from_bottom < 0 or area_share_from_bottom > 1:
        print("Invalid area share.")
        return None    
    
    area_share_from_top = 1 - area_share_from_bottom
    
    # calculate the number of True pixels in ydirection
    n_true_pixels_in_ydirection = np.count_nonzero(bw, axis=1)
    # get the index where the area_share is reached (from top)
    cum_area = np.cumsum(n_true_pixels_in_ydirection)
    area = cum_area[-1]
    if area == 0:
        print("No object found.")
        return 0
    greater_than_area_share = cum_area > (area_share_from_top * area)
    x_split = greater_than_area_share.argmax()

    # extract row of this position
    row_split = bw[x_split,:]
    
    # calculate the martin diameter of this dimension
    n_pixels = row_split.shape[0]

    first_y_idx = row_split.argmax()
    row_split_reversed = row_split[::-1]
    last_y_idx = n_pixels - row_split_reversed.argmax()

    martin_diameter_2d = last_y_idx - first_y_idx
        
    idx = np.zeros((2,2))
    idx[0,0], idx[0,1] = x_split, first_y_idx
    idx[1,0], idx[1,1] = x_split, last_y_idx
    
    return martin_diameter_2d, idx


def calc_longest_chord_2d(bw):
    """ Calculates the maximum chords of an object shape in y-direction.
    
    Args:
        bw (ndarray, bool): Binary image.
        
    Returns:
        max_chord_2d (int): 2D Max chord.
        line_max_chord_2d (ndarray, int): Start (a) and endpoint (b) of max chord in shape ``[[xa,ya],[xb,yb]]``.
    """
    
    all_chords_2d, all_edgepoints_2d = calc_chords_2d(bw)
    max_chord_2d, line_max_chord_2d = _determine_max_chord_2d(all_chords_2d, all_edgepoints_2d)
    
    return max_chord_2d, line_max_chord_2d


def _determine_max_chord_2d(all_chords_2d, all_edgepoints_2d):
    """ Determines the maximum of all chords.
    
    Args:
        all_chords_2d (ndarray, int): Array of several chords in shape ``[c0, c1, ...]``.
        all_edgepoints_2d (ndarray, int): List of edgepoints referrring to the chords
            in shape ``[[x0a,y0a],[x0b,y0b],[x1a,y1a],[x1b,y1b],...]``, where a is the start
            and b is the endpoint of the corresponding edge.
            
    Returns:
        max_chord_2d (int): Max chord.
        line_max_chord_2d (ndarray, int): Start (a) and endpoint (b) of max chord in shape ``[[xa,ya],[xb,yb]]``.
    """
    max_chord_2d = all_chords_2d.max()
    idx = all_chords_2d.argmax()
    idx_points = 2 * idx
    
    line_max_chord_2d = all_edgepoints_2d[idx_points:idx_points+2, :]
    
    # make borderline definition consistent
    line_max_chord_2d[:,1] = line_max_chord_2d[:,1] + 1
    
    return max_chord_2d, line_max_chord_2d


def calc_chords_2d(bw):
    """ Calculates all chords of an object shape in y-direction.
    
    Args:
        bw (ndarray, bool): Binary image.
        
    Returns:
        chords_2d (ndarray, int): An array with length of all found chords in y-direction.
    """
    
    assert bw.dtype == 'bool', "bw should be boolean"
        
    # Initialize array to store found chords
    # Note: There may be none or several (> 1) choords per row (this is why we use append command)
    all_chords_2d = np.array([], dtype='int64')
    all_edgepoints_2d = np.zeros((0,2), dtype='int64')

    # Find points where values changes in y-direction (horizontal)
    # So from False to True or True to False (i.e. two neighbor pixels in y-direction have different values)
    # Background pixels are False and Object Pixels are True. To make sure we find also the first and last
    # changing points, we add a false padding to the first and last column

    # padding
    bw_pad = np.pad(bw, pad_width=1, mode='constant', constant_values=False)
    bw_rep = np.repeat(bw_pad, repeats=1, axis=1)
    # find changing points in y-direction
    idx_points_with_changes = np.array(np.where(bw_rep[:,:-1] != bw_rep[:,1:]))

    # Reshape the results
    x_idx = idx_points_with_changes[0,:]
    y_idx = idx_points_with_changes[1,:]
    points = np.column_stack((x_idx, y_idx))

    # we are only interested in the rows, where changes accur => get indexes of these rows
    unique_x_positions = np.unique(x_idx)
    
    
    for u in unique_x_positions:
        # extract points of this row
        points_this_row = points[np.where(points[:,0]==u)]

        # to calculate the chords we now need to determine the distance between pairs of changepoints in y-direction
        y_coords_this_row = points_this_row[:,1]
        
        # since the leftest row is always filled with False pixels (see padding above), we know that the first point
        # will be a changing point from False to True, the next point then will be a changing point from True to
        # False and so on. More generally: If we sort the y-coordinates of all changing-points in ascending order and or
        # indexes start at zero, then: All changing points with even indexes (0, 2, ...) are starting points
        # and all ending points with uneven indexes (1, 3, ...) are ending points

        # as promised: sort y_coordinates in ascending order
        y_coords_this_row_sorted = np.sort(y_coords_this_row)        
         
        # starting points have even indexes
        starting_points_this_row = y_coords_this_row_sorted[0::2]

        # ending points have uneven indexes
        end_points_this_row = y_coords_this_row_sorted[1::2]

        # The choords are the distance between the corresponding starting and ending points
        chords_this_row = end_points_this_row - starting_points_this_row
        # add found choords to result list
        all_chords_2d = np.append(all_chords_2d, chords_this_row)
        
        # undo padding for idx
        points_this_row = points_this_row - 1
        
        all_edgepoints_2d = np.concatenate((all_edgepoints_2d, points_this_row))
        
    return all_chords_2d, all_edgepoints_2d


def calc_nassenstein_diameter_2d(bw):
    """ Calculates the Nassenstein diameter of an object shape.
   
    
    Args:
        bw (ndarray, bool): Binary image.
        
    Returns:
        nassenstein_diameter_2d (int): 2D Nassenstein diameter.
        idx (ndarray, int): Indexes of the start (0) and endpoint (1) of the Nassenstein diameter in shape ``[[x0,y0], [x1,y1]]``.
        
    Notes: There might be several touching points in the lowest row.
        In this implementation we will evaluate the Nassenstein Durchmesser at the middle
        of the continuous first contact surface from left.
    """
    

    # padding
    bw_pad = np.pad(bw, pad_width=1, mode='constant', constant_values=False)
    
    # find lowest row
    n_pixels_xdirection = bw_pad.shape[0]
    
    n_true_pixels_in_ydirection = np.count_nonzero(bw_pad, axis=1)
    n_true_pixels_in_ydirection_from_bottom = n_true_pixels_in_ydirection[::-1]
    idx_lowest_row = n_pixels_xdirection - _first_nonzero(n_true_pixels_in_ydirection_from_bottom,axis=0) - 1
    lowest_row = bw_pad[idx_lowest_row, :]
    # obtain first touching surface by finding the first two changing points:
    changing_points_row = np.where(lowest_row[:-1] != lowest_row[1:])[0]
    changing_points_row = np.sort(changing_points_row)

    start_idx_first_contact = changing_points_row[0]
    end_idx_first_contact = changing_points_row[1]
 
    # column, we want to evaluate
    # Note: np.ceil is essential: If we only have one touching point (e.g. at index 3 and 4) then we need to round up to 4, to extract
    # the correct column (refers to the definition of changing idx from above)
    evaluation_idx = int(np.ceil((start_idx_first_contact + end_idx_first_contact)/2))

    # extract the column at evaluation idx:
    nassenstein_column = bw_pad[:,evaluation_idx]
    
    # we measure starting from bottom
    nassenstein_column_from_bottom = nassenstein_column[::-1]
    # again we consider the changing points to determine the Nassenstein diameter
    changing_idx_nassenstein_column = np.where(nassenstein_column_from_bottom[:-1] != nassenstein_column_from_bottom[1:])[0]
    changing_idx_nassenstein_column = np.sort(changing_idx_nassenstein_column)
    
    

    # since we started counting from bottom, we have to transform the indexes to the coordinate system from top         
    measurement_point_bottom = n_pixels_xdirection - changing_idx_nassenstein_column[0]
    measurement_point_top = n_pixels_xdirection - changing_idx_nassenstein_column[1]

    nassenstein_diameter_2d = measurement_point_bottom - measurement_point_top
    
    # get indexes and undo padding shift
    idx = np.zeros((2,2), dtype=('int64'))
    idx[0,0], idx[0,1] = measurement_point_top - 2, evaluation_idx
    idx[1,0], idx[1,1] = measurement_point_bottom  - 2, evaluation_idx

    return nassenstein_diameter_2d, idx

def calc_max_dimensions_2d(max_chords_2d, angles_2d):
    """ Calculates the max dimensions of an object shape.
    
    x_max is the overall max chord of the object in all possible orientations. y_max is the longest chord orthogonal to
    y_max.

    Args:
        max_chords (ndarray, int/float): Array of max_chords of an object at different angles in shape ``[c0, c1, c2, ...]``.
        angles (ndarray, int/float): The respective angles to the max chords in ascending order.
    
    Returns:
        x_max (int/float): Larger max dimension of object (definition see above).
        y_max (int/float): Smaller max dimension of object (definition see above).
    """
    
    assert max_chords_2d.shape == angles_2d.shape, "max_chords and angles should have the same shape."
    
    
    x_max_2d = max_chords_2d.max()
    idx_x_max_2d = max_chords_2d.argmax()
    angle_x_max_2d = angles_2d[idx_x_max_2d]
    
    angle_y_max_2d = (angle_x_max_2d + 90) % 180
    idx_y_max_2d = (np.abs(angles_2d - angle_y_max_2d)).argmin()
    y_max_2d = max_chords_2d[idx_y_max_2d]
    
    return x_max_2d, y_max_2d 


def calc_fractal_dimension_perimeter_method_2d(contour, max_feret, n_stepsizes=10, step_size_min=2):
    """ Approximates the fractal dimension based on the perimeter method.
            Note: Stepsizes range from step_size_min to step_size_max in a log2 grid.
            step_size_max is set to 0.3 * max_feret according to DIN ISO 9276-6.
            
    Args:
        contour (ndarray, int/float): Array of contourpoints describing the shape contour
            in shape ``[[x0, y0], [x1, y1], [x2, y2]]``
        max_feret (float): Max feret diameter of object shape for norming the perimeters.
        n_stepsizes (int): Number of different stepsizes to take. Default is 10.
        step_size_min (float): Minimum stepsize to walk. Default is 2. (Definition of max stepsize see above)


    Returns:
        fractal_dimension (float): Approximated fractal dimension.
    """
    

    step_size_max = 0.3 * max_feret
    step_sizes = np.logspace(np.log2(step_size_min), np.log2(step_size_max), num=n_stepsizes, endpoint=True, base=2)

    perimeters = _uniformly_structured_gait(contour, step_sizes)
    
    if np.sum(perimeters) == 0:
        # only a point --> fractal dimension is zero
        fractal_dimension = 0
    else:
        # Normalize by maximum feret diameter
        perimeters_normed = perimeters/max_feret
        fractal_dimension = _approximate_fractal_dimension_by_slope(perimeters_normed, step_sizes)
        
    return fractal_dimension


def calc_fractal_dimension_boxcounting_method_2d(bw, pad_width=1):
    """ Approxiamte the fractal dimension of a binary image by the boxcounting method.
    
    Args:
        bw (ndarray, bool): Binary image.
        pad_width (int, optional): Width of applied zero-padding around the image. Default is 1.
        
    Returns:
        fractal_dimension (float): The approximated fractal dimension.
    
    """
    bw = np.pad(bw, pad_width=pad_width, mode='constant', constant_values=False)
    
    n_true_pixels = np.sum(bw.ravel())
    if n_true_pixels <= 1:
        # only a point --> fractal dimension is zero
        fractal_dimension = 0
    else:
        number_of_boxes, box_sizes = _box_counting(bw)
    
        if len(box_sizes) <= 1 or len(number_of_boxes) <= 1:
            # only a point --> fractal dimension is zero
            fractal_dimension = 0  
        else:
            fractal_dimension = _approximate_fractal_dimension_by_slope(number_of_boxes, box_sizes)
    
    return fractal_dimension


def _approximate_fractal_dimension_by_slope(measurements, step_sizes):
    """ Approximates fractal dimension meaurements and step_sizes by slope the log/log Richardson plot.
    
    Args:
        measurements (ndarray, float): Array of measured length of corresponding step_sizes.
        step_sizes (ndarray, float/int): Correspong step_sizes. Must have same shape as measurements.

    Returns:
        fractal_dimension (float): Approximated fractal dimension.

    Notes:
        Slope is approximate by linear regression of the curve in the log/log Richardson plot.
    """
    
    assert measurements.shape == step_sizes.shape, "Measurements and step size must have same shape."

    # remove entries where measurements is zero
    measurements_org = measurements.copy()
    measurements = measurements[measurements_org != 0]
    step_sizes = step_sizes[measurements_org != 0]
    
    measurements_log2 = np.log2(measurements)
    step_sizes_log2 = np.log2(step_sizes)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(step_sizes_log2, measurements_log2)
    
    if slope == 0:
        fractal_dimension = 0
    else:
        fractal_dimension = 1 - slope
    
    return fractal_dimension


def _uniformly_structured_gait(contour, step_sizes):
    """ Performs a uniformly structured gait of different stepsizes and returns the walked perimeter.
    
    Args:
        contour (ndarray, int/float): Array of contourpoints describing the shape contour
            in shape ``[[x0, y0], [x1, y1], [x2, y2]]``.
        step_sizes (ndarray, float): Array of the different step sizes to take.
            
    Returns:
        perimeters(ndarray, float): Array of walked perimeters in shape ``[p0, p1, p2, ...]``.
    """

    perimeters = np.zeros(step_sizes.shape)

    all_idx_list = []

    for j, step_size in enumerate(step_sizes):
        idx_list = [0]
        distance_list = []

        start_point = contour[0]
        i = 1
        while i < len(contour):
            end_point = contour[i]
            dist = spatial.distance.euclidean(start_point, end_point)
            if dist >= step_size:
                idx_list.append(i)
                distance_list.append(dist)
                start_point = contour[i]
                i = i + 1

            i = i + 1

        all_idx_list.append(idx_list)

        perimeters[j] = sum(distance_list)
    
    return perimeters

    

def _box_counting(bw, min_box_size=2):
    """ Counts the number of non-zero and non-full boxes of and binary image at different box sizes.
    
    Args:
        bw (ndarray, bool): Binary image.
        min_box_size (int, optional): Minimum investigated box size. Default is 2. Must be representable as ``2**n``, where 
            ``n`` is a natural number. Default is 2.

    Returns:
        number_of_boxes (ndarray, int): Array if the numbers of found non-zero and non-full boxes for the corresponding box size.
        box_sizes (ndarray, int): Array of corresponding box sizes.
    """

    # make bw shape (2**n, 2**n)
    bw_pad = _zeropad_bw_to_shape_of_power_two(bw)

    # create box sizes
    bw_size = bw_pad.shape[0]
    max_box_size = bw_size/2
    exp_max_box, exp_min_box = int(np.log2(max_box_size)), int(np.log2(min_box_size))
    n_steps = exp_max_box - exp_min_box + 1
    box_sizes = np.logspace(exp_min_box, exp_max_box, num=n_steps, base=2, dtype='int', endpoint=True)
    
    # initialize array for solutions
    number_of_boxes = np.zeros(box_sizes.shape, dtype='int64')

    # determine number of boxes for different box sizes
    for i, box_size in enumerate(box_sizes):
        number_of_boxes[i] = _boxcount_single_boxsize(bw_pad, box_size)
        
    return number_of_boxes, box_sizes


def _zeropad_bw_to_shape_of_power_two(bw):
    """ Transform a binary image into shape ``(2**n, 2**n)`` (where ``n`` is a natural number) by placing it on
        a black background.
        
    Args:
        bw (ndarray, bool): Binary image.

    Returns:
        bw_pad (ndarray, bool): Padded binary image of shape ``(2**n, 2**n)``, where n is a natural number.
    """

    max_bw_shape = max(bw.shape)

    # determine shape of the padded image
    exponent_bw_shape = int(np.ceil(np.log2(max_bw_shape)))
    padded_bw_size = 2**exponent_bw_shape
    padded_bw_shape = (padded_bw_size, padded_bw_size)

    # initialize the padded image
    bw_pad = np.zeros(padded_bw_shape, dtype='bool')

    # determine shift, s.t. bw is inserted in the center of bw_pad
    shift_x, shift_y = int((padded_bw_size - bw.shape[0])/2), int((padded_bw_size - bw.shape[1])/2)

    # insert bw
    bw_pad[shift_x:bw.shape[0]+shift_x, shift_y:bw.shape[1]+shift_y] = bw
    
    return bw_pad


def _boxcount_single_boxsize(bw, box_size):
    """ Calculates the number of boxes of shape (``box_size``, ``box_size``) that are non-empty and non-full in an image.

    Args:
        bw (ndarray, bool): Binary image.
        box_size (int): Size of the boxes. Boxes a value of 2**``n`` (``n`` in natural numbers)

    Returns:
        n_boxes (int): The number of found boxes.
    """

    # From [https://github.com/rougier/numpy-100 (#87)] cited from [https://gist.github.com/viveksck/1110dfca01e4ec2c608515f0d5a5b1d1]
    # create boxes of shape (box_size,box_size) and store results in a matrix
    # an efficient implementation of this procedere is:
    S = np.add.reduceat(np.add.reduceat(bw, np.arange(0, bw.shape[0], box_size), axis=0),
                        np.arange(0, bw.shape[1], box_size), axis=1)

    # count non-empty (0) and non-full boxes (box_sizes*box_size)
    n_boxes = len(np.where((S > 0) & (S < box_size*box_size))[0])
    return n_boxes

def _first_nonzero(arr, axis, invalid_val=-1):
    """ Calculates index of first nonzero entry of ``arr`` along ``axis``.
    
    Args:
        arr (np.ndarray): Array.
        axis (int): Axis along which is measured.
        invalid_val (int, optional): Value that is returned, if no nonzero-entry is found. Default is -1.
    Returns:
        first_nonzero_idx (int): Index of first nonzero entry of ``arr`` along ``axis``.
    """
    mask = arr!=0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)
