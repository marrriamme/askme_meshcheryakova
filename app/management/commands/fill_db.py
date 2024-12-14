from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.utils.crypto import get_random_string
import random
from django.db import transaction

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio to determine the number of entities to generate.')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        
        with transaction.atomic():
            # Создаем пользователей и профили
            self.stdout.write(self.style.SUCCESS('Creating users and profiles...'))
            users = []
            profiles = []
            for i in range(ratio):
                username = f'user_{i}'
                user = User(username=username, password='password')
                users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Creating {len(users)} users'))
            User.objects.bulk_create(users)

            for user in User.objects.all():
                profiles.append(Profile(user=user))
            self.stdout.write(self.style.SUCCESS(f'Creating {len(profiles)} profiles'))
            Profile.objects.bulk_create(profiles)

            # Создаем тэги
            self.stdout.write(self.style.SUCCESS('Creating tags...'))
            tags = [Tag(name=f'tag_{i}') for i in range(ratio)]
            self.stdout.write(self.style.SUCCESS(f'Creating {len(tags)} tags'))
            Tag.objects.bulk_create(tags)

            tags = list(Tag.objects.all())
            self.stdout.write(self.style.SUCCESS(f'{len(tags)} tags created'))

            # Создаем вопросы
            self.stdout.write(self.style.SUCCESS('Creating questions...'))
            questions = []
            for i in range(ratio * 10):
                author = random.choice(profiles)
                questions.append(Question(
                    title=f'Question {i}',
                    text=f'This is the text for question {i}',
                    author=author
                ))
            self.stdout.write(self.style.SUCCESS(f'Creating {len(questions)} questions'))
            Question.objects.bulk_create(questions)

            # Привязываем теги к вопросам
            self.stdout.write(self.style.SUCCESS('Attaching tags to questions...'))
            for question in Question.objects.all():
                question.tags.add(*random.sample(tags, k=min(3, len(tags))))
            self.stdout.write(self.style.SUCCESS('Tags attached to questions'))

            # Создаем ответы
            self.stdout.write(self.style.SUCCESS('Creating answers...'))
            answers = []
            for question in questions:
                # Случайное количество неправильных ответов (например, от 1 до 5)
                num_incorrect_answers = random.randint(1, 30)
                
                # Создаем неправильные ответы
                incorrect_answers = [
                    Answer(
                        question=question,
                        text=f'This is the incorrect answer to question {question.id}',
                        author=random.choice(profiles),
                        is_correct=False
                    )
                    for _ in range(num_incorrect_answers)
                ]
                
                # Создаем один правильный ответ
                correct_answer = Answer(
                    question=question,
                    text=f'This is the correct answer to question {question.id}',
                    author=random.choice(profiles),
                    is_correct=True
                )
                
                # Вставляем правильный ответ случайным образом в список
                incorrect_answers.insert(random.randint(0, num_incorrect_answers), correct_answer)
                
                # Добавляем все ответы в общий список
                answers.extend(incorrect_answers)

            self.stdout.write(self.style.SUCCESS(f'Creating {len(answers)} answers'))
            Answer.objects.bulk_create(answers)


            # Создаем уникальные оценки пользователей к вопросам
            self.stdout.write(self.style.SUCCESS('Creating question likes...'))
            question_likes = set()  # Используем set для уникальных значений
            for i in range(ratio * 200):
                user = random.choice(profiles)
                question = random.choice(questions)
                question_likes.add((user.id, question.id))  # Добавляем уникальную пару (user_id, question_id)

            self.stdout.write(self.style.SUCCESS(f'Creating {len(question_likes)} unique question likes'))
            # Преобразуем в объекты и создаем их
            QuestionLike.objects.bulk_create(
                [QuestionLike(user_id=user_id, question_id=question_id) for user_id, question_id in question_likes]
            )

            # Создаем уникальные оценки пользователей к ответам
            self.stdout.write(self.style.SUCCESS('Creating answer likes...'))
            answer_likes = set()  # Используем set для уникальных значений
            for i in range(ratio * 200):
                user = random.choice(profiles)
                answer = random.choice(answers)
                answer_likes.add((user.id, answer.id))  # Добавляем уникальную пару (user_id, answer_id)

            self.stdout.write(self.style.SUCCESS(f'Creating {len(answer_likes)} unique answer likes'))
            # Преобразуем в объекты и создаем их
            AnswerLike.objects.bulk_create(
                [AnswerLike(user_id=user_id, answer_id=answer_id) for user_id, answer_id in answer_likes]
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully filled the database with ratio {ratio}.'))