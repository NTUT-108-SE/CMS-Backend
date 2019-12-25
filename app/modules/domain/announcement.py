import graphene
from bson.objectid import ObjectId
from ..database import AnnouncementModel
from mongoengine import DoesNotExist


class Announcement:
    def __init__(self, id=None, announcement=None):
        try:
            if announcement != None:
                self._announcement = announcement
            elif id != None:
                self._announcement = AnnouncementModel.objects.get(id=ObjectId(id))
            else:
                raise AttributeError(
                    """
                    Require one of announcement, id
                """
                )
        except Exception:
            raise DoesNotExist("ID not valid!")

    @classmethod
    def create(cls, title, context, author, date):
        announcement = AnnouncementModel(title=title, context=context, author=author, date=date)
        announcement.save()
        announcement.reload()
        return cls(announcement=announcement)

    @staticmethod
    def get_all(offset=0, count=20):
        length = len(AnnouncementModel.objects)  # TOTAL

        _announcements = []

        if offset >= length or length == 0:
            _announcements = []
        elif offset + count >= length:
            _announcements = list(AnnouncementModel.objects().order_by('-id')[offset:])
        else:
            _announcements = list(AnnouncementModel.objects().order_by('-id')[offset:count])

        return {'total': length, 'entry': _announcements, 'offset': offset, 'count': count}

    def save(self):
        self._announcement.save()
        self._announcement.reload()

    def delete(self):
        self._announcement.delete()

    def get(self):
        return self._announcement

    def update(self, announcement):
        self._announcement.update(**announcement)
        self.save()

    @property
    def id(self):
        return str(self._announcement['id'])

    @property
    def title(self):
        return self._announcement['title']

    @title.setter
    def title(self, new_title):
        self._announcement['title'] = new_title

    @property
    def context(self):
        return self._announcement['context']

    @context.setter
    def context(self, new_context):
        self._announcement['context'] = new_context

    @property
    def author(self):
        return self._announcement['author']

    @author.setter
    def author(self, new_author):
        self._announcement['author'] = new_author

    @property
    def date(self):
        return self._announcement['date']

    @date.setter
    def date(self, new_date):
        self._announcement['date'] = new_date
