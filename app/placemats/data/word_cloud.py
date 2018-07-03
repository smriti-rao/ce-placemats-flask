from datetime import datetime


def word_cloud(pmid_to_keywords: dict, keyword_to_pmids: dict, pmid_to_articles):
    NUMBER_OF_KEYWORDS = 100
    word_cloud_result = []
    keyword_pmid_count = {}

    sorted_by_value = sorted(keyword_to_pmids.items(), key=lambda kv: len(kv[1]), reverse=True)

    for index in range(NUMBER_OF_KEYWORDS):
        each_keyword = sorted_by_value[index][0]
        pmids = keyword_to_pmids[each_keyword]
        year_word_cloud = {}
        keyword_pmid_count[each_keyword] = len(pmids)

        for each_pmid in pmids:
            article_info = pmid_to_articles[each_pmid]

            if article_info is None:
                continue

            article_pub_year = article_info.date_of_publication

            if not isinstance(article_pub_year, str):
                if article_pub_year is None:
                    continue
                else:
                    article_pub_year = str(article_pub_year)

            if article_pub_year in year_word_cloud:
                year_word_cloud[article_pub_year]['count'] = year_word_cloud[article_pub_year]['count'] + 1
            else:
                pub_time = datetime(year=int(article_pub_year), month=int(1), day=int(1))
                year_word_cloud[article_pub_year] = \
                    {'count': 1, 'term': each_keyword, 'publication_time': pub_time.isoformat(), 'id': article_pub_year}
                word_cloud_result.append(year_word_cloud[article_pub_year])

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