import requests
from scripts.utils import CustomLogger


def fetch_orcid_works(orcid):
    logger = CustomLogger("orcid_scraper")

    url = f"https://pub.orcid.org/v3.0/{orcid}/works"

    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    try:
        works = response.json()
        titles_seen = set()

        papers = []
        for group in works.get('group', []):
            for work in group.get('work-summary', []):
                title = work.get('title', {}).get(
                    'title', {}).get('value', 'No Title')

                if title in titles_seen:
                    continue
                titles_seen.add(title)

                url = work.get('url', {}).get('value', '')

                publication_date = f"{work.get('publication-date', {}).get('year', {}).get('value', 'Unknown Year')}"
                journal_title = work.get('journal-title', {})
                if journal_title is not None:
                    journal_title = journal_title.get(
                        'value', 'No Journal Title')

                papers.append({
                    'title': title,
                    'url': url,
                    'publication_date': publication_date,
                    'journal_title': journal_title
                })

        logger.info(f"data fetched successfully for {orcid}")
        logger.debug(papers)

        return papers

    except Exception as e:
        logger.error("fetching data", e)
        logger.debug(response.json())
        return []
