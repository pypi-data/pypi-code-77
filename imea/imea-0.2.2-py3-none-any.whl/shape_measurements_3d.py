import numpy as np
import sys, os
import cv2
from skimage import measure, morphology, transform
from scipy import spatial, stats
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from pathlib import Path
from scipy.spatial import ConvexHull
from imea.shape_measurements_2d import calc_min_2d_bounding_box_based_on_bw, extract_shape_measurements_2d, calc_chords_2d, _shape_measurements_2d_single_object

def extract_shape_measurements_2d_and_3d(img_3d_org, threshold_3d_gv, spatial_resolution_xy_mm_per_px, spatial_resolution_z_mm_per_gv=1, dalpha=9, min_object_area_px=10, n_objects_to_extract_max=-1):
    """ Calculates all 2D and 3D shape measurements for all objects found in img_3d_org.
    
    Args:
        img_3d_org (np.ndarry, float): 3d image in grayscale representation.
        threshold_3d_gv (float): Threshold in grayvalues for segmentation of img_3d_org. 
            Pixels <= threshold_3d_gv are considered as background, pixels > threshold_3d_gv as object (foreground).
        spatial_resolution_xy_mm_per_px (float): Spatial resolution of img_3d in x and y direction in [mm/pixel]
            (assumes image is already calibrated, i.e. dx = dy)
        spatial_resolution_z_mm_per_gv (float, optional): Spatial resolution of img_3d in z-direction (height) in [mm/grayvalue].
            Default value of spatial_resolution_z_mm_per_gv=1 means image is already calibrated (1 grayvalue increment = 1 mm)
        dalpha (float, optional): Angle in degrees over which is iterated.
        min_object_area_px (int, optional): Min #pixels of a region to be considered as an object. Default is 0.
        n_objects_to_extract_max (int, optional): Max number of objects to be extracted.
            Use n_objects_to_extract_max=-1 to extract all objects.

    Returns:
        df_shape_measurements_2d (pandas.DataFrame): Pandas dataframe including all 2D shape measurements currently supported by imea.
        df_shape_measurements_3d (pandas.DataFrame): Pandas dataframe including all 3D shape measurements currently supported by imea.
    """
    assert type(img_3d_org) == np.ndarray, "img_3d_org should be an np.ndarray"
    assert len(img_3d_org.shape) == 2, "img_3d_org should be 2D array"
    assert len(img_3d_org.dtype) != 'bool', "img_3d_org is a boolean not numeric array. Please use imea.extract_shape_measurements_2d() for 2D shape measurements"

    imgs_3d, bws = extract_and_preprocess_3d_imgs(img_3d_org, threshold_3d_gv, min_object_area_px, n_objects_to_extract_max)
    dfs_shape_measurements_3d = []
    dfs_shape_measurements_2d = []
    
    for (img_3d, bw) in zip(imgs_3d, bws):
        df_shape_measurements_3d_single_object = _shape_measurements_3d_single_object(img_3d, spatial_resolution_xy_mm_per_px, spatial_resolution_z_mm_per_gv, dalpha)
        dfs_shape_measurements_3d.append(df_shape_measurements_3d_single_object)
        
        df_shape_measurements_2d_single_object, _, _ = _shape_measurements_2d_single_object(bw, spatial_resolution_xy_mm_per_px, dalpha)
        dfs_shape_measurements_2d.append(df_shape_measurements_2d_single_object)
        
    df_shape_measurements_3d = pd.DataFrame(dfs_shape_measurements_3d)
    df_shape_measurements_2d = pd.DataFrame(dfs_shape_measurements_2d)
       
    return df_shape_measurements_2d, df_shape_measurements_3d



def _shape_measurements_3d_single_object(img_3d, spatial_resolution_xy_mm_per_px, spatial_resolution_z_mm_per_gv, dalpha):
    """ Determines alll 3D shape measurements for a single object (represented by img_3d).
    
    Args:
        img_3d (np.ndarray, float): 3d image (as grayscale image).
        spatial_resolution_xy_mm_per_px (float): Spatial resolution of img_3d in x and y direction in [mm/pixel]
            (assumes image is already calibrated, i.e. dx = dy)
        spatial_resolution_z_mm_per_gv (float): Spatial resolution of img_3d in z-direction (height) in [mm/grayvalue].
            Default value of spatial_resolution_z_mm_per_gv=1 means image is already calibrated (1 grayvalue increment = 1 mm)
        dalpha (float): Angle in degrees over which is iterated.
        
    Returns:
        shape_measurements_3d (dict): 3D shape measurements.
        
    Notes:
        Assumes: only one object per binary image.
    """
    
    img_3d_equalspace, spatial_resolution = get_equalspace_3d_img(img_3d, spatial_resolution_xy_mm_per_px, spatial_resolution_z_mm_per_gv)
    ch_3d = calc_convexhull_from_3d_img(img_3d_equalspace)
    
    volume_3d_mm3 = calc_volume_3d(img_3d_equalspace, spatial_resolution)
    volume_convexhull_3d_mm3 = calc_volume_convexhull_3d(ch_3d, spatial_resolution)
    surf_area_3d_mm2 = calc_surfacearea_convexhull_3d(ch_3d, spatial_resolution)
    
    volume_equivalent_diameter_3d_mm = calc_volume_equivalent_diameter_3d(volume_3d_mm3)
    surfacearea_equivalent_diameter_3d_mm = calc_surfacearea_equivalent_diameter_3d(surf_area_3d_mm2)
    
    width_3d_bb_mm, length_3d_bb_mm, height_3d_bb_mm = calc_3d_bounding_box(img_3d_equalspace, spatial_resolution)

    max_feret_3d_mm, min_feret_3d_mm, x_max_3d_mm, y_max_3d_mm, z_max_3d_mm = calc_3d_feret_and_max_dimensions(ch_3d, spatial_resolution, dalpha)
    
    shape_measurements_3d = {
        "volume_3d_mm3": volume_3d_mm3,
        "volume_convexhull_3d_mm3": volume_convexhull_3d_mm3,
        "surf_area_3d_mm2": surf_area_3d_mm2,
        "volume_equivalent_diameter_3d_mm": volume_equivalent_diameter_3d_mm,
        "surfacearea_equivalent_diameter_3d_mm": surfacearea_equivalent_diameter_3d_mm,        
        "width_3d_bb_mm": width_3d_bb_mm,
        "length_3d_bb_mm": length_3d_bb_mm,
        "height_3d_bb_mm": height_3d_bb_mm,
        "max_feret_3d_mm": max_feret_3d_mm,
        "min_feret_3d_mm": min_feret_3d_mm,
        "x_max_3d_mm": x_max_3d_mm,
        "y_max_3d_mm": y_max_3d_mm,
        "z_max_3d_mm": z_max_3d_mm
    } 

    return shape_measurements_3d

def extract_and_preprocess_3d_imgs(img_3d_org, threshold_3d_gv, min_object_area_px=0, n_objects_to_extract_max=-1):
    """ Segments 3d image and returns list of 3d images and corresponding binary images for all objects.
        
    Args:
       img_3d_org (np.ndarry, float): 3d image in grayscale representation.
       threshold_3d_gv (float): Threshold in grayvalues for segmentation of img_3d_org. 
           Pixels <= threshold_3d_gv are considered as background, pixels > threshold_3d as object (foreground).
       min_object_area_px (int, optional): Min #pixels of a region to be considered as an object. Default is 0.
       n_objects_to_extract_max (int, optional): Max number of objects to be extracted.
           Use n_objects_to_extract_max=-1 to extract all objects.
           
    Returns:
       imgs_3d (list of np.ndarrays): Cropped 3d image of single objects. Non-object pixels (<= threshold_3d_gv) are set to zero. 
       bws (list of np.ndarray): Cropped binary image of single objects.
    """
    
    bw_org = img_3d_org > threshold_3d_gv
    df = pd.DataFrame(measure.regionprops_table(measure.label(bw_org), intensity_image=img_3d_org, properties=('area', 'bbox','image', 'intensity_image')))                  
    df = df[df['area'] > min_object_area_px]
    df = df.sort_values('area', ascending=False).reset_index(drop=True)
    
    n_objects_found = len(df)
    
    if n_objects_to_extract_max <= 0:
        n_objects_to_extract = n_objects_found
    else:
        n_objects_to_extract = min(n_objects_found, n_objects_to_extract_max)
        
    
    imgs_3d = []
    bws = []
    # single object
    for i in range(n_objects_to_extract):
        bw_cropped = df['image'][i]
        img_3d_cropped = df['intensity_image'][i]
        img_3d_cropped[~bw_cropped] = 0
        bws.append(bw_cropped)
        imgs_3d.append(img_3d_cropped)

    return imgs_3d, bws

def get_equalspace_3d_img(img_3d, spatial_resolution_xy_mm_per_px, spatial_resolution_z_mm_per_gv=1):
    """ Creates a equalspace image, i. e. where dx = dy = dz.

    Args:
        img_3d (np.ndarray, float): 3d image (as grayscale image).
        spatial_resolution_xy_mm_per_px (float): Spatial resolution of img_3d in x and y direction in [mm/pixel]
            (assumes image is already calibrated, i.e. dx = dy).
        spatial_resolution_z_mm_per_gv (float, optional): Spatial resolution of img_3d in z-direction (height) in [mm/grayvalue].
            Default value of spatial_resolution_z_mm_per_gv=1 means image is already calibrated (1 grayvalue increment = 1 mm).
            
    Returns:
        img_3d_equalspace (np.ndarray, float): 3d image with dx = dy = dz.
        spatial_resolution (float): Spatial resolution of img_3d_equalspace.
        
    Note:
        spatial_resolution is set to spatial_resolution_xy_mm_per_px, as only heights are transformed.
    """
    
    img_3d_equalspace = img_3d / (spatial_resolution_xy_mm_per_px/spatial_resolution_z_mm_per_gv)
    spatial_resolution = spatial_resolution_xy_mm_per_px
    
    return img_3d_equalspace, spatial_resolution

def calc_volume_3d(img_3d_equalspace, spatial_resolution):
    """ Calculates the volumen of the 3d object.
    
    Args:
        img_3d_equalspace (np.ndarray shape (n_x, n_y), float): 3d grayscale image of single object with equal spacing, i.e. dx = dy = dy.
        Pixels not showing the pixel should be 0.
        spatial_resolution (float): Spatial resolution of img_3d_equalspace in [mm/Pixel] and [mm/Grayvalue].
            The following must be true: spatial_resolution == dx == dy == dz.
    Returns:
        volume_mm3 (float): The object volume in mm^3.
    """
    
    volume_mm3 = np.sum(img_3d_equalspace.ravel()) * spatial_resolution**3
    
    return volume_mm3


def calc_volume_equivalent_diameter_3d(volume_mm3):
    """ Calculates volume equivalent diameter.
    
    Args:
        volume_mm3 (float): 3D volume in [mm^3].
        
    Returns:
        volume_equivalent_diameter_3d_mm (float): Volume-equivalent diameter in [mm].
    """
    
    volume_equivalent_diameter_3d_mm = np.cbrt(6 * volume_mm3/np.pi)
    
    return volume_equivalent_diameter_3d_mm

def calc_surfacearea_equivalent_diameter_3d(surf_area_3d_mm2):
    """ Calculates surfacearea-equivalent diameter.
    
    Args:
        surf_area_3d_mm2 (float): Surface area in [mm^2].
        
    Returns:
        surfacearea_equivalent_diameter_3d_mm (float): Surfacearea-equivalent diameter in [mm].
    """
    
    surfacearea_equivalent_diameter_3d_mm = np.sqrt(surf_area_3d_mm2/np.pi)
    return surfacearea_equivalent_diameter_3d_mm
    

def calc_3d_bounding_box(img_3d_equalspace, spatial_resolution):
    """ Calculates the 3d bounding box.
    Note: width_3d_bb_mm and length_3d_bb_mm are identical to the 2d bounding box.
    height_3d_bb_mm is the maximum height in z-direction.
    
    Args:
        img_3d_equalspace (np.ndarray shape (n_x, n_y), float): 3d grayscale image of single object with equal spacing, i.e. dx = dy = dy.
        Pixels not showing the pixel should be 0.
        spatial_resolution (float): Spatial resolution of img_3d_equalspace in [mm/Pixel] and [mm/Grayvalue].
            The following must be true: spatial_resolution == dx == dy == dz.
    Returns:
        volume_mm3 (float): The object volume in mm^3.
    """
    
    bw = img_3d_equalspace > 0
    length_min_bb, width_min_bb, center_min_bb, cornerpoints_min_bb = calc_min_2d_bounding_box_based_on_bw(bw)
    height_3d_bb = np.max(img_3d_equalspace.ravel())

    width_3d_bb_mm = width_min_bb * spatial_resolution
    length_3d_bb_mm = length_min_bb * spatial_resolution
    height_3d_bb_mm = height_3d_bb * spatial_resolution

    return width_3d_bb_mm, length_3d_bb_mm, height_3d_bb_mm

def calc_convexhull_from_3d_img(img_3d_equalspace):
    """ Calculates 3d convex hull from 3d image.
    
    Args:
        img_3d_equalspace (np.ndarray shape (n_x, n_y), float): 3d grayscale image of single object with equal spacing, i.e. dx = dy = dy.
        Pixels not showing the object should be 0.
        
    Returns:
        ch_3d (scipy.spatial.ConvexHull): Convex hull.
    
    """
    
    bw = img_3d_equalspace > 0

    (x, y) = np.where(bw == True)
    z_top = img_3d_equalspace[x, y]
    z_bottom = np.zeros_like(x)
    x = np.concatenate([x]*2)
    y = np.concatenate([y]*2)
    z = np.concatenate([z_top,z_bottom], axis=0)
    
    # To transform the indexes from above into real coordinates we need to make the region + 0.5 greater in every direction
    # We do this by applying shift in every diagonal direction and then computing the 
    
    x_all = []
    y_all = []
    z_all = []
    shifts = np.array([[0.5,0.5],[-0.5,0.5],[0.5,-0.5],[-0.5,-0.5]])    
    for shift in shifts:
        x_shifted = x + shift[0]
        x_all.append(x_shifted)
        y_shifted = y + shift[1]
        y_all.append(y_shifted)
        z_all.append(z)
        
    x_all = np.concatenate(x_all)
    y_all = np.concatenate(y_all)
    z_all = np.concatenate(z_all)
    
    points_3d = np.column_stack([x_all,y_all,z_all])
    ch_3d = ConvexHull(points_3d)

    return ch_3d

def calc_volume_convexhull_3d(ch_3d, spatial_resolution):
    """ Calculates volume of convex hull.
    
    Args:
        ch_3d (scipy.spatial.ConvexHull): Convex Hull.
        spatial_resolution (float): Spatial resolution of ch in [mm/Pixel:Grayvalue].
    Returns:
        volume_convexhull_mm3 (float): 3D volume of convex hull in mm^3.    
    """
    
    volume_convexhull = ch_3d.volume
    volume_convexhull_mm3 = volume_convexhull * spatial_resolution**3
    return volume_convexhull_mm3

def calc_surfacearea_convexhull_3d(ch, spatial_resolution):
    """ Calculates surface area of convex hull.
    
    Args:
        ch (scipy.spatial.ConvexHull): Convex Hull.
        spatial_resolution (float): Spatial resolution of ch in [mm/Pixel:Grayvalue].
    Returns:
        surf_area_mm3 (float): 3D volume of convex hull in mm^3.    
    """
    
    surf_area = ch.area
    surf_area_mm2 = surf_area * spatial_resolution**2
    return surf_area_mm2

def calc_2dcaliper(pts_2d, axis=1):
    """ Calculates 2d caliper from pointcloud.
    
    Args:
        pts_2d (np.ndarry, shape=(n,2)): 2D pointcloud.
        axis (float, 0 or 1, optional): axis.
        
    Returns:
        caliper (float): Caliper distance.
    """
    
    
    caliper = np.max(pts_2d[:,axis]) - np.min(pts_2d[:,axis])
    return caliper

def calc_3d_feret_and_max_dimensions(ch_3d, spatial_resolution, dalpha=9):
    """ Calculates 3D feret diameter (min, max) and max dimensions (x,y,z).
    
    Args:
        ch_3d (scipy.spatial.ConvexHull): 3D convex hull of object.
        spatial_resolution (float): Spatial resolution of ch_3d in [mm].
        dalpha (float, optional): Angle in degrees over which is iterated.
        
    Returns:
        max_feret_3d_mm (float): Max feret diameter in mm.
        min_feret_3d_mm (float): Min feret diameter in mm.
        x_max_3d_mm: x_max (equal to max feret) in mm.
        y_max_3d_mm: y_max (orthogonal to x_max) in mm.
        z_max_3d_mm: z_max (orthogonal to x_max and y_max) in mm.
    """
    
    p_3d = ch_3d.points[ch_3d.vertices]

    # feret diameters
    angles_x = np.arange(0,180,dalpha)
    angles_y = np.arange(0,180,dalpha)

    n_angles_x = len(angles_x)
    n_angles_y = len(angles_y)

    calipers = np.zeros((n_angles_x, n_angles_y))

    for i, a_x in enumerate(angles_x):
        p_3d_rot = _rotate(p_3d, _Rx(a_x))
        p_2d = _project_to_xz(p_3d_rot)
        for j, a_y in enumerate(angles_y):
            p_2d_rot = _rotate(p_2d, _R_2d(a_y))
            calipers[i,j] = calc_2dcaliper(p_2d_rot, axis=1)

    max_feret_3d = np.max(calipers.ravel())
    min_feret_3d = np.min(calipers.ravel())

    # x_max
    x_max = max_feret_3d

    # y_max
    # rotate, s.t. x_max is parallel to x-axis
    idxs_max_feret = np.where(calipers == max_feret_3d)
    angle_x_max_feret = angles_x[idxs_max_feret[0][0]]
    angle_y_max_feret = angles_y[idxs_max_feret[1][0]]

    p3d_ymax = np.copy(p_3d)
    p3d_ymax = _rotate(p3d_ymax, _Rx(angle_x_max_feret))
    p3d_ymax = _rotate(p3d_ymax, _Ry(angle_y_max_feret))

    angles_x_ymax = np.arange(0,180,dalpha)
    ymax_list = np.zeros_like(angles_x_ymax)

    for a_x in angles_x_ymax:
        p3d_ymax_rot = _rotate(p3d_ymax, _Rx(a_x))
        p2d_ymax_rot = _project_to_xz(p3d_ymax_rot)
        ymax_list[i] = calc_max_chord_2d_from_2d_pointcloud(p2d_ymax_rot, axis=0)

    y_max = np.max(ymax_list)
    idx = np.argmax(ymax_list)
    angle_x_ymax = angles_x_ymax[idx]

    # z_max
    p3d_zmax = np.copy(_rotate(p3d_ymax, _Rx(angle_x_ymax)))
    p2d_zmax = _project_to_yz(p3d_zmax)
    z_max = calc_max_chord_2d_from_2d_pointcloud(p2d_zmax, axis=0)
    
    
    if y_max < z_max:
        y_max, z_max = z_max, y_max

    max_feret_3d_mm = max_feret_3d * spatial_resolution
    min_feret_3d_mm = min_feret_3d * spatial_resolution

    x_max_3d_mm = x_max * spatial_resolution
    y_max_3d_mm = y_max * spatial_resolution
    z_max_3d_mm = z_max * spatial_resolution

    return max_feret_3d_mm, min_feret_3d_mm, x_max_3d_mm, y_max_3d_mm, z_max_3d_mm

def calc_max_chord_2d_from_2d_pointcloud(p2d, axis=0):
    """ Calculate maximum 2d chord from 2d pointcloud based on convex hull.
    
    Args:
        p2d (np.ndarray, shape=(n,2)): 2D pointcloud representing object.
        axis (int, 0 or 1, optional): Axis in which max chord is measured.
        
    Returns:
        max_chord_2d (int): Max chord of p2d in measurement direction.    
    """
    
    if axis == 0:
        # Rotate by 90 degrees, since chords are measurement in 2D y not 2D x-direction (see function calc_chords_2d)
        p2d = _rotate(p2d, _R_2d(90))
    
    # Get 2D convex hull
    ch2d = ConvexHull(p2d)
    p_ch_2d = ch2d.points[ch2d.vertices]

    # determine chords
    bw_ch_2d = calc_2d_bw_of_2d_convexhull(p_ch_2d)
    chord_length_2d, _ = calc_chords_2d(bw_ch_2d)
    max_chord_2d = np.max(chord_length_2d)

    return max_chord_2d

def calc_2d_bw_of_2d_convexhull(p_ch_2d):
    """ Transforms 2d convexhull into a binary image.
    
    Args:
        p_ch_2d (np.ndarray, shape=(n,2)): Vertices of 2d convex hull.
        
    Returns:
        bw_ch_2d (np.ndarray, bool): Binary image of 2d convex hull.   
    """
    
    # move points to intervall [0, inf]
    min_values = np.min(p_ch_2d, axis=0)
    x = np.array([min_values, np.zeros_like(min_values)])
    min_values = np.min(x, axis=0)
    min_values_abs = np.abs(min_values)
    p_ch_2d = p_ch_2d + min_values_abs

    # transform to binary image
    gridsize = np.ceil(np.max(p_ch_2d, axis=0)).astype('int')
    bw_ch_2d = measure.grid_points_in_poly(gridsize, p_ch_2d)
    return bw_ch_2d


def _rotate(pts, R):
    """ Applies rotation matrix ``R`` to pointcloud ``pts``.
    
    Args:
        pts (np.ndarray): Points to be rotated of shape ``(n,d)``, where ``n`` is the number of points and ``d`` the number of dimensions.
        R (np.ndarray): Rotation matrix of shape ``(d,d)``.
        
    Returns:
        pts_rot (np.ndarray): Rotated points.
    """   
    
    pts_rot = np.dot(pts, R)
    
    return pts_rot


def _Rx(angle_in_degrees):
    """ Returns 3D rotation matrix for rotating around x-axis.
    
    Args:
        angle_in_degrees (float): Rotation angle around x-axis in degrees.
        
    Returns:
        Rx (np.ndarray): 3D Rotation matrix.
    """
    
    angle_in_rad = angle_in_degrees/180 * np.pi
    Rx = np.array([[1,0,0],[0,np.cos(angle_in_rad),-np.sin(angle_in_rad)],[0,np.sin(angle_in_rad),np.cos(angle_in_rad)]])
    
    return Rx

def _Ry(angle_in_degrees):
    """ Returns 3D rotation matrix for rotating around y-axis.
    
    Args:
        angle_in_degrees (float): Rotation angle around y-axis in degrees.
        
    Returns:
        Ry (np.ndarray): 3D Rotation matrix.
    """
    
    angle_in_rad = angle_in_degrees/180 * np.pi
    Ry = np.array([[np.cos(angle_in_rad), 0, np.sin(angle_in_rad)],[0, 1, 0],[-np.sin(angle_in_rad), 0, np.cos(angle_in_rad)]])
    
    return Ry

def _Rz(angle_in_degrees):
    """ Returns 3D rotation matrix for rotating around z-axis.
    
    Args:
        angle_in_degrees (float): Rotation angle around z-axis in degrees.
        
    Returns:
        Rz (np.ndarray): 3D Rotation matrix.
    """
    
    angle_in_rad = angle_in_degrees/180 * np.pi
    Rz = np.array([[np.cos(angle_in_rad), -np.sin(angle_in_rad), 0],[np.sin(angle_in_rad), np.cos(angle_in_rad), 0], [0, 0, 1]])
    
    return Rz 

def _R_2d(angle_in_degrees):
    """ Returns 2D rotation matrix.
    
    Args:
        angle_in_degrees (float): Rotation angle in degrees.
        
    Returns:
        R (np.ndarray): 2D Rotation matrix.
    """
    
    angle_in_rad = angle_in_degrees/180 * np.pi
    R = np.array([[np.cos(angle_in_rad), -np.sin(angle_in_rad)],[np.sin(angle_in_rad), np.cos(angle_in_rad)]])
    
    return R

def _project_to_xy(p_3d):
    """ Projects 3D points to xy plane.
    
    Args:
        p_3d (np.ndarray): 3D pointcloud in shape ``(n,3)``, where ``n`` is the number of points.
        
    Returns:
        p_2d (np.ndarray): Projected pointcloud in shape ``(n,2)``, where ``n`` is the number of points.
    """
    
    p_2d = p_3d[:,[0,1]]
    
    return p_2d

def _project_to_xz(p_3d):
    """ Projects 3D points to xy plane.
    
    Args:
        p_3d (np.ndarray): 3D pointcloud in shape ``(n,3)``, where ``n`` is the number of points.
        
    Returns:
        p_2d (np.ndarray): Projected pointcloud in shape ``(n,2)``, where ``n`` is the number of points.
    """
    
    p_2d = p_3d[:,[0,2]]
    
    return p_2d

def _project_to_yz(p_3d):
    """ Projects 3D points to xy plane.
    
    Args:
        p_3d (np.ndarray): 3D pointcloud in shape ``(n,3)``, where ``n`` is the number of points.
        
    Returns:
        p_2d (np.ndarray): Projected pointcloud in shape ``(n,2)``, where ``n`` is the number of points.
    """
    
    p_2d = p_3d[:,[1,2]]
    
    return p_2d
