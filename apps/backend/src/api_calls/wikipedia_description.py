import wikipediaapi


def get_summary_wikipedia_api(title, lang='pl'):
    """Get summary of the place from Wikipedia API.

    :param title: title of the place
    :param lang: language of the place
    :return: summary of the place
    """

    wiki_wiki = wikipediaapi.Wikipedia(language=lang, user_agent='travel-app')
    page = wiki_wiki.page(title)

    if page.exists():
        return page.summary
    else:
        return "Strona nie istnieje."
