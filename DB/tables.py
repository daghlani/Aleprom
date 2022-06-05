from DB.engine import *
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, func, Boolean


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    bale_id = Column(Integer, unique=True)
    name = Column(String)
    username = Column(String, unique=True)
    info = Column(Boolean, default=False)
    warning = Column(Boolean, default=False)
    error = Column(Boolean, default=False)
    critical = Column(Boolean, default=False)
    is_valid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __unicode__(self):
        return '%s' % self.name

    def __repr__(self):
        return '<%s#%s>' % (self.__class__.__name__, self.id)

    def bool_ch(self, bol):
        if bol:
            return False
        else:
            return True

    def st_change(self, pr):
        if pr < 2:
            self.info = self.bool_ch(self.info)
        if pr < 3:
            self.warning = self.bool_ch(self.warning)
        if pr < 4:
            self.error = self.bool_ch(self.error)
        if pr < 5:
            self.critical = self.bool_ch(self.critical)
        return [self.info, self.warning, self.error, self.critical]


class AuthUsers(Base):
    __tablename__ = 'auth_users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<%s#%s>' % (self.__class__.__name__, self.id)

    def __str__(self):
        return self.username


Base.metadata.create_all(db)
