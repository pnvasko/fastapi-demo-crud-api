from sqlmodel import SQLModel


class Base(SQLModel):
    def modelToDict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d