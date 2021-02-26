from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Boolean, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Animal(Base):
    __tablename__ = "animals"

    id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String)
    status = Column(String)
    organization_id = Column(String)
    species = Column(String)
    age = Column(String)
    gender = Column(String)
    size = Column(String)
    coat = Column(String)
    published_at = Column(String)  # FIXME
    status_changed_at = Column(String)  # FIXME
    breed_primary = Column(String)
    breed_secondary = Column(String)
    breed_mixed = Column(Boolean)
    breed_unknown = Column(Boolean)
    color_primary = Column(String)
    color_secondary = Column(String)
    color_tertiary = Column(String)
    spayed_neutered = Column(Boolean)
    house_trained = Column(Boolean)
    special_needs = Column(Boolean)
    shots_current = Column(Boolean)
    declawed = Column(Boolean)
    good_with_children = Column(Boolean)
    good_with_dogs = Column(Boolean)
    good_with_cats = Column(Boolean)
    description = Column(String)
    url = Column(String, nullable=False)
    number_of_photos = Column(Integer, nullable=False)
    contact_email = Column(String)
    contact_phone = Column(String)
    contact_address1 = Column(String)
    contact_address2 = Column(String)
    contact_city = Column(String)
    contact_state = Column(String)
    contact_postcode = Column(String)
    contact_country = Column(String)
    primary_photo_small = Column(String)
    primary_photo_medium = Column(String)
    primary_photo_large = Column(String)
    primary_photo_full = Column(String)


if __name__ == "__main__":
    db_file = "/Users/phillipdupuis/databases/petfinder/sqlite.db"

    engine = create_engine(f"sqlite:///{db_file}", echo=True)
    Session = sessionmaker(bind=engine)

    sesh = Session()
    blap = sesh.query(Animal)

    cat = 'hi'