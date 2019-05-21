from tea_site import celery, db
from tea_site.models import Answer


@celery.task
def eval_answer(answer_id):
    from time import sleep

    sleep(10)
    a = Answer.query.get(answer_id)
    a.grade = 1
    db.session.commit()
    return
