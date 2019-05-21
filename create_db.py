from werkzeug.security import generate_password_hash

from tea_site import create_app, db
from tea_site.models import *


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(
            email="pavel@oborin.com",
            first_name="Pavel",
            last_name="Oborin",
            password=generate_password_hash("12345678"),
        )

        cat = Category(name="Физика")

        test = Test(name="Физика №1", category=cat, author=admin, draft=False)
        q1 = Question(author=admin, text="Первый вопрос")
        a1 = Answer(
            author=admin,
            question=q1,
            text="Ответ на первый вопрос",
            grade=1,
            reviewed=True,
        )
        q2 = Question(author=admin, text="Второй вопрос")
        a2 = Answer(
            author=admin,
            question=q2,
            text="Ответ на второй вопрос",
            grade=1,
            reviewed=True,
        )
        q3 = Question(author=admin, text="Третий вопрос")
        a3 = Answer(
            author=admin,
            question=q3,
            text="Ответ на третий вопрос",
            grade=1,
            reviewed=True,
        )
        test.questions.append(q1)
        test.questions.append(q2)
        test.questions.append(q3)

        db.session.add_all([admin, cat, test, q1, q2, q3, a1, a2, a3])
        db.session.commit()

