import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def list_entry_urls():
    """
    Return dict where key is entry title and values is URL of entry
    """
    entries = list_entries()
    urls = [f"http://localhost:8000/entries/{entry}" for entry in entries]

    entries_urls_map = {}

    for entry, url in zip(entries, urls):
        entries_urls_map[entry] = url

    return entries_urls_map


def list_entries_contained_query(query):
    """
    Return dict with entry_title: url content,
    where entry contains given query
    """
    entries = list_entries()
    selected_entries = []

    for title in entries:
        content = get_entry(title)
        if query in content:
            selected_entries.append(title)

    urls = [f"http://localhost:8000/{entry}" for entry in selected_entries]

    entries_urls_map = {}

    for entry, url in zip(entries, urls):
        entries_urls_map[entry] = url

    return entries_urls_map
    


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
