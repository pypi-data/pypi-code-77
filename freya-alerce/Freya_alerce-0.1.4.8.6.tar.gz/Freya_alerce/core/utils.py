
from astropy.coordinates import SkyCoord

"""
This class represent the generic methods
"""
class Utils:

    def deg_to_hms(self,ra,dec):
        """
        Parameters
        ----------
        ra : float

        dec: float
        """
        coord_icrs = SkyCoord(ra=ra, dec=dec)
        return c.to_string('hmsdms')

    def hms_to_deg(self,hms):
        """
        Parameters
        ----------
        hms : string
        """
        coord = SkyCoord(hms,frame='icrs') #transform coord
        ra = coord.ra.degree
        dec = coord.dec.degree
        return ra,dec