import Bio.Entrez
import Bio.Medline
import logging
from app.placemats.util import *
from collections import defaultdict, namedtuple

logger = logging.getLogger(__name__)

API_KEY = None

MAX_PER_PAGE = 2000


def configure_client(email='adrien.guerard@gmail.com', api_key=None):
    """
    Must be called once before calling any of the other API's
    :param email:
    :param api_key:
    """
    Bio.Entrez.email = email
    global API_KEY
    API_KEY = api_key


def call(procedure, *args, **kwargs):
    """
    Wraps all our calls to Entrez API's. Acts as our 'http interceptor'.
    :type procedure: function
    :param procedure: Entrez function to invoke
    :param args:
    :param kwargs:
    :return:
    """
    logger.debug('Calling {} with args: {}, kwargs: {}'.format(procedure.__name__, args, kwargs))
    if API_KEY:
        kwargs['api_key'] = API_KEY
    handle = procedure(*args, **kwargs)
    if kwargs.get('rettype') == 'medline':
        output = Bio.Medline.parse(handle)
        output = list(output)
    else:
        output = Bio.Entrez.read(handle)
    handle.close()
    return output


def efetch(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    """
    return call(Bio.Entrez.efetch, *args, **kwargs)


def egquery(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    """
    return call(Bio.Entrez.egquery, *args, **kwargs)


def esearch(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    return call(Bio.Entrez.esearch, *args, **kwargs)


def pubmed_search(term, skip=0, limit=MAX_PER_PAGE, sort='relevance'):
    retmax = min(limit, MAX_PER_PAGE)
    out = esearch(db='pubmed', sort=sort, term=term, retstart=skip, retmax=retmax)
    logger.info('Pubmed search query: %s ; translation-set: %s', term, out['TranslationSet'])
    return out


def get_medline_infos(ids):
    infos = []
    for ids_chunk in chunks(ids, MAX_PER_PAGE):
        infos.extend(efetch(db='pubmed', id=ids_chunk, rettype='medline', retmode='text'))
    return infos


def get_pmids_for_term(term, limit):
    pmids = []
    current = pubmed_search(term)
    current_id_list = current['IdList']
    while len(pmids) < limit and current_id_list:
        pmids.extend(current_id_list)
        current = pubmed_search(term, skip=len(pmids))
        current_id_list = current['IdList']
    return pmids[:limit]


AuthorInfo = namedtuple('AuthorInfo', ['pmid_to_authors', 'author_to_pmids', 'pmid_to_articles'])
Article = namedtuple('Article', ['title', 'abstract'])


def author_info(term, limit=20_000):
    pmids = get_pmids_for_term(term, limit)
    pmid_to_authors = defaultdict(set)
    author_to_pmids = defaultdict(set)
    pmid_to_articles = {}
    medline_infos = get_medline_infos(pmids)
    for m_info in medline_infos:
        if not ('FAU' in m_info and 'PMID' in m_info):
            logger.warning('[author_info] PMID or author name not found for term: %s ; %s', term, m_info)
            continue
        pmid = m_info['PMID']
        for name in m_info['FAU']:
            author_to_pmids[name].add(pmid)
            pmid_to_authors[pmid].add(name)
            pmid_to_articles[pmid] = Article(m_info.get('TI'), m_info.get('AB'))
    return AuthorInfo(pmid_to_authors, author_to_pmids, pmid_to_articles)
