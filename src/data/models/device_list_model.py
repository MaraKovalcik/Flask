from datetime import datetime, timedelta

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, String, DateTime


from .user import User
from ..database import db
from ..mixins import CRUDModel
from ..util import generate_random_token


class Device_List(CRUDModel):
    __tablename__ = 'device_list'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)
    popisek = Column(String, nullable=False, index=False)
    value = Column(String, nullable=False, index=True)
    used = Column(Boolean(name="used"), default=False)
    insert_date = Column(DateTime)

    # Use custom constructor
    # pylint: disable=W0231
    def __init__(self, **kwargs):
        self.insert_date = datetime.utcnow()
        self.value = generate_random_token()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    @staticmethod
    def find_by_userid(userid):
        return db.session.query(Device_List).filter_by(user_id=userid).all()
