import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    fnames = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))
    return [get_title_from_filename(fname) for fname in fnames]


def list_entry_urls():
    """
    Return dict where key is entry title and values is URL of entry
    """
    entries = list_entries()
    entries_with_undescore = [entry.replace(" ", "_") for entry in entries]
    urls = [f"http://localhost:8000/entries/{entry}" for entry in entries_with_undescore]

    entries_urls_map = {}

    for entry, url in zip(entries, urls):
        entries_urls_map[entry] = url

    return entries_urls_map


def list_entries_contained_query(query):
    """
    Return dict with entry_title: url content,
    where entry contains given query
    """
    query = query.lower()

    entries = list_entries()
    selected_entries = []

    for title in entries:
        if query in title or query in title.lower():
            selected_entries.append(title)
        else:
            content = get_entry(title)
            if query in content:
                selected_entries.append(title)

    urls = [f"http://localhost:8000/entries/{entry.replace(' ', '_')}" for entry in selected_entries]

    entries_urls_map = {}

    for entry, url in zip(selected_entries, urls):
        entries_urls_map[entry] = url

    return entries_urls_map


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{process_entry_title(title)}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{process_entry_title(title)}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def process_entry_title(text: str) -> str:
    """
    Remove more than 1 space
    All spaces that left substitute to "_"
    """
    return re.sub(r"\s+", "_", text)


def get_title_from_filename(fname: str) -> str:
    """
    Substitue all "_" in filename to spaces
    """
    return fname.replace("_", " ")


def process_entry(entry: str):
    """
    Convert Markdown entry content to HTML
    """
    # TODO use implemented markdown converter
