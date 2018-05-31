from sqlalchemy.ext.declarative import declared_attr

class CustomMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}