from DB.engine import *
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, func, Boolean


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    bale_id = Column(Integer, unique=True)
    name = Column(String)
    username = Column(String, unique=True)
    info_st = Column(Boolean, default=False)
    warning_st = Column(Boolean, default=False)
    error_st = Column(Boolean, default=False)
    critical_st = Column(Boolean, default=False)
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
            self.info_st = self.bool_ch(self.info_st)
        if pr < 3:
            self.warning_st = self.bool_ch(self.warning_st)
        if pr < 4:
            self.error_st = self.bool_ch(self.error_st)
        if pr < 5:
            self.critical_st = self.bool_ch(self.critical_st)
        return [self.info_st, self.warning_st, self.error_st, self.critical_st]




Base.metadata.create_all(db)
