from tea_site import celery


@celery.task
def eval_answer(answer_id):
    from time import sleep

    sleep(10)
    return
