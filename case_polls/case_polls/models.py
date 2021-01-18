from django.db import models


# После создания поле "дата старта" у опроса менять нельзя
# - добавление/изменение/удаление вопросов в опросе.??


class Polls(models.Model):
    title = models.CharField("Название опроса", max_length=30, db_index=True)
    description = models.CharField("Описание", max_length=300, default="")
    date_start = models.DateTimeField("Дата старта", auto_now=True)
    date_finish = models.DateTimeField("Дата окончания", auto_now=True)
    answers = models.ForeignKey("PollAnswers", on_delete=models.CASCADE, related_name="polls",
                                verbose_name='Варианты ответов')

    class Meta:
        db_table = 'polls'
        ordering = ['title']

    def __str__(self):
        return self.title


class PollAnswers(models.Model):
    answer = models.CharField(max_length=100)

    class Meta:
        db_table = 'poll_answers'
        ordering = ['answer']

    def __str__(self):
        return self.answer
