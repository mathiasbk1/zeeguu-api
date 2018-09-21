from datetime import datetime

from zeeguu import log
from zeeguu.model import Article, UserArticle
from zeeguu_api.api.utils.emailer import send_notification_article_liked


def distill_article_interactions(session, user, data):
    """

        extracts info from user_activity_data

    :param session:
    :param event:
    :param value:
    :param user:
    """

    event = data['event']
    value = data['value']
    article_id = int(data['article_id'])

    log(f'event is: {event}')

    if "UMR - OPEN ARTICLE" in event:
        article_opened(session, article_id, user)
    elif "UMR - LIKE ARTICLE" in event:
        article_liked(session, article_id, user, True)
    elif "UMR - UNLIKE ARTICLE" in event:
        article_liked(session, article_id, user, False)
    elif "UMR - USER FEEDBACK" in event:
        article_feedback(session, article_id, value)


def article_feedback(session, article_id, event_value):
    article = Article.query.filter_by(id=article_id).one()

    if "not_finished_for_broken" or "not_finished_for_incomplete" or "not_finished_for_other" in event_value:
        article.vote_broken()
        session.add(article)
        session.commit()


def article_liked(session, article_id, user, like_value):
    article = Article.query.filter_by(id=article_id).one()
    ua = UserArticle.find(user, article)
    ua.liked = like_value
    session.add(ua)
    session.commit()
    log(f"{ua}")
    send_notification_article_liked(user.name, article.title, article.url.as_string())

def article_opened(session, article_id, user):
    article = Article.query.filter_by(id=article_id).one()
    ua = UserArticle.find(user, article)
    if not ua:
        ua = UserArticle.find_or_create(session, user, article, opened=datetime.now())
    ua.opened = datetime.now()
    session.add(ua)
    session.commit()
    log(f"{ua}")
