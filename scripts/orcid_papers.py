import requests
from scripts.utils import CustomLogger


def fetch_orcid_works(orcid):
    logger = CustomLogger("orcid_scraper").get_logger()

    url = f"https://pub.orcid.org/v3.0/{orcid}/works"

    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        works = response.json()

        papers = []
        for group in works.get('group', []):
            for work in group.get('work-summary', []):
                title = work.get('title', {}).get(
                    'title', {}).get('value', 'No Title')
                doi_url = ""
                for external_id in work.get('external-ids', {}).get('external-id', []):
                    if external_id.get('external-id-type') == 'doi':
                        doi_url = external_id.get(
                            'external-id-url', {}).get('value', '')

                publication_date = f"{work.get('publication-date', {}).get('year', {}).get('value', 'Unknown Year')}"
                journal_title = work.get('journal-title', {})
                if journal_title is not None:
                    journal_title = journal_title.get(
                        'value', 'No Journal Title')

                papers.append({
                    'title': title,
                    'doi_url': doi_url,
                    'publication_date': publication_date,
                    'journal_title': journal_title
                })

        return papers

    else:
        logger.error("fetching data", response.text)
        return []
