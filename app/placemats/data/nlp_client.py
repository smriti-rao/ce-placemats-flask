import logging
import rake_nltk

logger = logging.getLogger(__name__)


def get_keywords(text, cutoff_score=None, limit=None):
    rake = rake_nltk.Rake()
    rake.extract_keywords_from_text(text)
    score_words = rake.get_ranked_phrases_with_scores()
    if limit is not None:
        score_words = score_words[:limit]
    if cutoff_score is not None:
        score_words = filter(lambda score_word: score_word[0] >= cutoff_score, score_words)
    return [score_word[1] for score_word in score_words]
