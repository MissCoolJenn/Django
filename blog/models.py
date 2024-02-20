from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=400)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE,)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
       return self.title
    # ^ добавляется метод для предоставления человекочитаемой версии модели в админку или оболочку Django

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})