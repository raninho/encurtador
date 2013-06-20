from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from core.models import Url


class UsuarioViewTest(TestCase):

    def setUp(self):
        self.username = 'teste'
        self.email = 'teste@teste.com.br'
        self.password = 'teste'

    def criar_usuario(self, username, password, email=None):
        usuario = User.objects.create_user(
            username,
            email,
            password,
        )
        return usuario

    def test_registrar_novo_usuario(self):
        self.assertEqual(User.objects.count(), 0)
        self.client.post(
            reverse('core:registrar'),
            data={
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'password2': self.password,
            },
        )
        self.assertEqual(User.objects.count(), 1)

    def test_login_usuario(self):
        self.criar_usuario(username=self.username, password=self.password)
        response = self.client.login(
            username=self.username,
            password=self.password,
        )
        self.assertTrue(response)


class UrlViewTest(TestCase):

    def setUp(self):
        self.username = 'teste'
        self.password = 'teste'

    def criar_usuario(self, username, password, email=None):
        usuario = User.objects.create_user(
            username,
            email,
            password,
        )
        return usuario

    def test_encurtar_url_com_usuario_anonimo(self):
        self.assertEqual(Url.objects.count(), 0)
        self.client.post(
            reverse('core:encurtar'),
            data={'url': 'www.globo.com'},
        )
        self.assertEqual(Url.objects.count(), 1)

    def test_encurtar_url_com_usuario_logado(self):
        usuario = self.criar_usuario(
            username=self.username,
            password=self.password
        )
        self.assertEqual(Url.objects.filter(usuario=usuario).count(), 0)
        response = self.client.login(
            username=self.username,
            password=self.password,
        )
        self.assertTrue(response)
        response = self.client.post(
            reverse('core:encurtar'),
            data={'url': 'www.globo.com'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Url.objects.filter(usuario=usuario).count(), 1)

    def test_listar_todas_urls_do_usuario(self):
        usuario = self.criar_usuario(
            username=self.username,
            password=self.password
        )
        response = self.client.login(
            username=self.username,
            password=self.password,
        )
        self.assertTrue(response)
        self.assertEqual(Url.objects.filter(usuario=usuario).count(), 0)
        self.client.post(
            reverse('core:encurtar'),
            data={'url': 'www.globo.com'},
        )
        self.client.post(
            reverse('core:encurtar'),
            data={'url': 'www.g1.com'},
        )
        self.assertEqual(Url.objects.filter(usuario=usuario).count(), 2)
        response = self.client.get(
            reverse('core:listar'),
        )
        self.assertContains(response, 'www.globo.com')
        self.assertContains(response, 'www.g1.com')
        self.assertTemplateUsed(response, 'listar.html')

    def test_redirecionamento_pelo_token(self):
        self.client.post(
            reverse('core:encurtar'),
            data={'url': 'www.globo.com'},
        )
        url = Url.objects.get(url='www.globo.com')
        response = self.client.get(
            reverse(
                'core:redirecionar',
                kwargs={'token': url.token},
            )
        )
        self.assertRedirects(response, 'http://www.globo.com', status_code=302)
