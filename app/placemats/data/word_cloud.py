


def word_cloud(pmid_to_keywords: dict, keyword_to_pmids: dict, pmid_to_articles):
    word_cloud_result = []
    for each_keyword, pmids in keyword_to_pmids.items():
        count = len(pmids)
        min_year_result = get_earliest_year(pmids, pmid_to_articles)
        if min_year_result['year'] == 0:
            continue
        word_cloud_result.append({ 'count': count, 'term': each_keyword, 'publication_time': min_year_result['year'], 'id': min_year_result['pmid'] })
    return word_cloud_result


def get_earliest_year(pmids, pmid_to_articles):
    min_year = 0
    pmid = None
    for each_pmid in pmids:
        article_info = pmid_to_articles[each_pmid]
        if article_info is not None and article_info.date_of_publication is not None:
            if min_year == 0 or article_info.date_of_publication < min_year:
                min_year = article_info.date_of_publication
                pmid = each_pmid

    return ({ 'year' : min_year, 'pmid': pmid })