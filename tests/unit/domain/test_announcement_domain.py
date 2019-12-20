from app.modules.domain.announcement import Announcement


def test_create(db):
    announcement = Announcement.create(
        title="test title", context="test context", author="test author", date="2010-10-10"
    )
    assert announcement.title == "test title"
    assert announcement.context == "test context"
    assert announcement.author == "test author"
    assert announcement.date.strftime("%Y-%m-%d") == "2010-10-10"


def test_get_all(db):
    Announcement.create(
        title="test title", context="test context", author="test author", date="2010-10-10"
    )
    Announcement.create(
        title="test title", context="test context", author="test author", date="2010-10-10"
    )

    assert 2 == len(Announcement.get_all()['entry'])

    assert 1 == len(Announcement.get_all(0, 1)['entry'])


def test_delete(db):
    announcement = Announcement.create(
        title="test title", context="test context", author="test author", date="2010-10-10"
    )
    assert 1 == len(Announcement.get_all()['entry'])

    announcement.delete()

    assert 0 == len(Announcement.get_all()['entry'])


def test_get(db):
    announcement = Announcement.create(
        title="test title", context="test context", author="test author", date="2010-10-10"
    )
    assert announcement.title == "test title"
    assert announcement.context == "test context"
    assert announcement.author == "test author"
    assert announcement.date.strftime("%Y-%m-%d") == "2010-10-10"
    assert announcement._announcement == announcement.get()


def test_update(db):
    announcement = Announcement.create(
        title="test title", context="test context", author="test author", date="2010-10-10"
    )

    data = {"title": "title", "context": "context"}

    announcement.update(data)

    assert announcement.title == "title"
    assert announcement.context == "context"
    assert announcement.author == "test author"
    assert announcement.date.strftime("%Y-%m-%d") == "2010-10-10"
