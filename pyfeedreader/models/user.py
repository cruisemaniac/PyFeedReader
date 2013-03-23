from sqlalchemy.orm import relationship
from pyfeedreader.models.entry import Entry
from pyfeedreader.models.feed import Feed

__author__ = 'sis13'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String, Text, desc
from pyfeedreader.models.directory import Directory
from pyfeedreader.models.userfeeds import UserFeeds

class User(Model):
    __tablename__ = "user"
    id = Column('id', Integer, primary_key=True)
    email = Column(String(256))
    password = Column(Text)
    current_login = Column(Integer)
    last_login = Column(Integer)
    username = Column(String(100))
    dirs = relationship("Directory")
    feeds = relationship("UserFeeds")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def q_dirs(self, session):
        for dir in self.dirs:
            dir.get_feeds(session)

    def feed_entities(self, session):
        ids = []
        for feed in self.feeds:
            ids.append(feed.feed_id)

        self.entries = session.query(Entry).filter(Entry.feed_id.in_(ids)).order_by(desc(Entry.updated)).all()

    def __repr__(self):
        return '<User %r>' % self.username