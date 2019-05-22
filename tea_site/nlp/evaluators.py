from tea_site.nlp.utils import get_cosine_sim, lemmatized_text


def lemmatized_cosine(student_answer, teacher_answer):
    student_answer = lemmatized_text(student_answer)
    teacher_answer = lemmatized_text(teacher_answer)
    return get_cosine_sim(student_answer, teacher_answer)
