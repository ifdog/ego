from datetime import datetime, timezone

from main import models,statics


def note_get(key: str):
    records = models.Note.objects.filter(key__exact=key)
    if records.count() > 0:
        return records[0]
    else:
        return None


def note_add(key: str,markdown :str,draft:str):
    _note = models.Note(key=key, markdown=markdown,markdown_time=datetime.now())
    if draft:
        _note.draft = draft
        _note.draft_time = datetime.now()
    _note.save()
    return _note


def tag_matches(name: str, limit: int = 10):
    records = models.Tag.objects.filter(name__icontains=name)
    return records[:limit]


def tag_get_or_create(name: str):
    query = models.Tag.objects.filter(name__exact=name)
    if query.count() > 0:
        return query[0]
    else:
        _tag = models.Tag(name=name)
        _tag.save()
        return _tag


def note_query_all(part_of_key: str):
    _notes = models.Note.objects.filter(key__icontains=part_of_key)
    return _notes


def note_query_public(part_of_key:str):
    _show_tag = models.Tag.objects.filter(name=statics.SHOW_PUBLIC_TAG)
    _notes = models.Note.objects.filter(key__icontains=part_of_key)
    _notes = _notes.filter(tags__in=_show_tag).distinct()
    return _notes


def contains_tag_attr(tags, name: str):
    records = tags.filter(name=name)
    return records.count() > 0


def update_markdown(note:models.Note, content:str):
    note.markdown = content
    note.markdown_time = datetime.now()
    note.save()

def update_draft(note:models.Note, content:str):
    note.draft = content
    note.draft_time = datetime.now()
    note.save()
