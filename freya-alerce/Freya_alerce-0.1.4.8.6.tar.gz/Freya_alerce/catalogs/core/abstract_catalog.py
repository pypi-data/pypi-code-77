from abc import ABC, abstractmethod

class BaseCatalog(ABC):

    @abstractmethod
    def get_lc_deg():
        return ""

    @abstractmethod 
    def get_lc_hms():
        return ""
