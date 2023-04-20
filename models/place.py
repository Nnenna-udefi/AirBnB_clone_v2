#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models
from sqlalchemy.ext.declarative import declarative_base


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float(0.0), nullable=True)
    longitude = Column(Float(0.0), nullable=True)
    amenity_ids = []


    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")
    else:
        @property
        def reviews(self):
            """ Returns list of reviews.id """
            var = models.storage.all()
            list_review = []
            result = []
            for key in var:
                review = key.replace('.', ' ')
                review = shlex.split(review)
                if (review[0] == 'Review'):
                    list_review.append(var[key])
            for obj in list_review:
                if (obj.place_id == self.id):
                    result.append(obj)
            return (result)
