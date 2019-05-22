from werkzeug.security import generate_password_hash
import pandas as pd

from tea_site import create_app, db
from tea_site.models import *
from tea_site.config import ProdConfig


app = create_app(ProdConfig)

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

        cat1 = Category(
            name="Физика", image="1.jpg", description="Базовые вопросы по физике"
        )
        cat2 = Category(
            name="Зарубежная литература",
            image="2.jpg",
            description="Вопросы по зарубежной литературе",
        )
        cat3 = Category(name="Алгебра", image="3.jpg", description="Вопросы по алгебре")
        cat4 = Category(
            name="Философия", image="4.jpg", description="Вопросы по философии"
        )

        idx = 1
        que_per_test = 5
        questions = []
        df = pd.read_csv("que.csv", sep="|")
        for _, row in df.iterrows():
            q = Question(author=admin, text=row["QUESTION"])
            a = Answer(
                author=admin,
                question=q,
                text=row["TEACHER_ANSWER"],
                grade=1,
                reviewed=True,
            )
            db.session.add(a)
            questions.append(q)
            if que_per_test == 0:
                test = Test(
                    name=f"Физика №{idx}", category=cat1, author=admin, draft=False
                )
                idx += 1
                for q in questions:
                    test.questions.append(q)
                questions.append(test)
                db.session.add_all(questions)
                questions = []
                que_per_test = 6
            que_per_test -= 1

        db.session.add_all([admin, cat1, cat2, cat3, cat4])
        db.session.commit()

