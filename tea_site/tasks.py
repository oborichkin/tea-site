from tea_site import celery
from tea_site.models import Answer


@celery.task
def eval_answer(answer_id):
    from time import sleep

    sleep(10)
    a = Answer.query.get(answer_id)
    answer.grade = 1
    return
