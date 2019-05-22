from tea_site import celery, db
from tea_site.models import Answer
from tea_site.nlp.evaluators import lemmatized_cosine


@celery.task
def eval_answer(answer_id):

    s = Answer.query.get(answer_id)
    t = Answer.query.filter_by(res_id=None, q_id=s.q_id).first()
    grade = lemmatized_cosine(s.text, t.text)
    s.grade = grade
    db.session.commit()
    return
