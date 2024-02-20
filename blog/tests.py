from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

# для теста создается пустая БД и её нужно наполнить тестовыми данными
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls): # "def setUpTestData(cls):" - Load initial data for the TestCase.
        cls.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret'
        )
#        ^ создание нового уникального пользователя для прохождения теста

        cls.post = Post.objects.create(
            title = 'good title',
            body = 'somebody',
            author = cls.user
        )
#        ^ создание нового поста для теста

    def test_post_model(self):
        self.assertEqual(self.post.title, 'good title')
#        ^ проверить что title поста совпадает с - 'good title'
        self.assertEqual(self.post.body, 'somebody')
#        ^ проверить что body поста совпадает с - 'somebody'
        self.assertEqual(self.post.author.username, 'testuser')
#        ^ проверить что автор поста testuser
        self.assertEqual(str(self.post), 'good title')
#        ^ 
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')
#        ^ проверить ссылка на пост совпадает с указаной

    def test_url_homepage_listview(self):
        responce = self.client.get('/')
#        ^ ссылка на страницу которая будет тестироваться
        self.assertEqual(responce.status_code, 200)
#        ^ проверить что указаная страница отвечает (код 200 - страница нормально открылась и нормально рабоает)
        self.assertTemplateUsed(responce, 'home.html')
#        ^ указаная страница использует темплейт 'home.html'
        self.assertTemplateUsed(responce, 'base.html')
#        ^ указаная страница использует темплейт 'base.html'

    def test_url_post_detail_detailview(self):
        responce = self.client.get('/post/1/')
#        ^ ссылка на страницу которая будет тестироваться
        self.assertEqual(responce.status_code, 200)
#        ^ проверить что указаная страница отвечает (код 200 - страница нормально открылась)
        self.assertTemplateUsed(responce, 'post_detail.html')
#        ^ указаная страница использует темплейт 'post_detail.html'
        self.assertTemplateUsed(responce, 'base.html')
#        ^ указаная страница использует темплейт 'base.html'
        self.assertContains(responce, 'good title')
#        ^ на странице есть текст 'good title'

    def test_responce_at_name_home_listview(self):
        responce = self.client.get(reverse('home'))
#        ^ имя страницы которая будет тетироваться
        self.assertEqual(responce.status_code, 200)
#        ^ проверить что указаная страница отвечает (код 200 - страница нормально открылась)
        self.assertContains(responce, 'somebody')
#        ^ на странице есть текст 'somebody'

    def test_responce_at_name_post_detail_detailview(self):
        responce = self.client.get(reverse('post_detail', kwargs={"pk": self.post.pk}))
#        ^ ссылка на страницу которая будет тестироваться, сложно потому что ссылка динамичесская
        self.assertEqual(responce.status_code, 200)
#        ^ проверить что указаная страница отвечает (код 200 - страница нормально открылась)

        no_response = self.client.get("/post/100000/")
#        ^ ссылка на фейк страницу которая будет тестироваться
        self.assertEqual(no_response.status_code, 404)
#        ^ проверить что указаная страница отвечает (код 404 - страница не отвечает)

    def test_post_createview(self):
        responce = self.client.post(
            reverse('post_new'),
            {
            'title': 'New title',
            'body': 'New Text',
            'author': self.user.id,
            }
#               ^ переход на страницу создания поста и собственно создание поста
        )
        self.assertEqual(responce.status_code, 302)
#           ^ после завершения работы на странице она отвечает кодом 302 и перенаправляет пользователя на другую страницу
        self.assertEqual(Post.objects.last().title, 'New title')
#           ^ последний пост в БД имеет заголовок 'New title'
        self.assertEqual(Post.objects.last().body, 'New Text')
#           ^ последний пост в БД имеет тело 'New Text'
    
    def test_post_updateview(self):
        responce = self.client.post(
            reverse('post_edit', args='1'),
            {
                'title': 'Updated title',
                'body': 'Updated body',
            }
#               ^ редактировать пост номер "1" где 'title': 'Updated title' и 'body': 'Updated body'
        )
        self.assertEqual(responce.status_code, 302)
#           ^ после завершения работы на странице она отвечает кодом 302 и перенаправляет пользователя на другую страницу
        self.assertEqual(Post.objects.last().title, 'Updated title')
#           ^ последний пост в БД имеет заголовок 'Updated title'
        self.assertEqual(Post.objects.last().body, 'Updated body')
#           ^ последний пост в БД имеет тело 'Updated body'

    def test_post_deleteview(self):
        responce = self.client.post(reverse('post_delete', args='1'))
#           ^ перейти на страницу удаления поста и удалить пост с id 1
        self.assertEqual(responce.status_code, 302)
#           ^ после завершения работы на странице она отвечает кодом 302 и перенаправляет пользователя на другую страницу