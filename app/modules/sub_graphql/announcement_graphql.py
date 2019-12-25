import graphene
from ..database import AnnouncementModel
from ..domain.announcement import Announcement
from graphene_mongo import MongoengineObjectType


class AnnouncementMeta(MongoengineObjectType):
    class Meta:
        model = AnnouncementModel


class AnnouncementsMeta(graphene.ObjectType):
    total = graphene.Int()
    entry = graphene.List(AnnouncementMeta)
    offset = graphene.Int()
    count = graphene.Int()


class AnnouncementInput(graphene.InputObjectType):
    title = graphene.String()
    context = graphene.String()
    author = graphene.String()
    date = graphene.String()


class CreateAnnouncement(graphene.Mutation):
    class Arguments:
        announcement_data = AnnouncementInput(required=True)

    ok = graphene.Boolean()
    announcement = graphene.Field(AnnouncementMeta)

    @staticmethod
    def mutate(root, info, announcement_data):
        try:
            announcement = Announcement.create(**announcement_data)
            return CreateAnnouncement(announcement=announcement.get(), ok=True)

        except Exception:
            return CreateAnnouncement(announcement=None, ok=False)


class MutateAnnouncement(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        announcement_data = AnnouncementInput(required=True)

    ok = graphene.Boolean()
    announcement = graphene.Field(AnnouncementMeta)

    @staticmethod
    def mutate(root, info, id, announcement_data):
        try:
            announcement = Announcement(id=id)
            announcement.update(announcement_data)
            return MutateAnnouncement(announcement=announcement.get(), ok=True)

        except Exception:
            return MutateAnnouncement(announcement=None, ok=False)


class DeleteAnnouncement(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        try:
            announcement = Announcement(id=id)
            announcement.delete()
            return DeleteAnnouncement(ok=True)

        except Exception:
            return DeleteAnnouncement(ok=False)
