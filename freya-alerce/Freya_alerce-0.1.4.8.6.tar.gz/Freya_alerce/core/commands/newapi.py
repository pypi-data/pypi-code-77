from Freya_alerce.core.base import Base


class NewAPI(Base):
    """
    Created new FreyaAPI.
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_new_api()