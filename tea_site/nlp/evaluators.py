from tea_site.nlp.utils import cosine_similarity, lemmatized_text


def lemmatized_cosine(student_answer, teacher_answer):
    student_answer = lemmatized_text(student_answer)
    teacher_answer = lemmatized_text(teacher_answer)
    return cosine_similarity(student_answer, teacher_answer)
