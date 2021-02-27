import numpy as np

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

def R_2d(angle_in_degrees):
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