from django.contrib.auth.models import User
from django.test import TestCase
from .models import ContentPage, ContentText


class PageTextTests(TestCase):
    def test_defaults_preserve_existing_heading_formatting(self):
        response = self.client.get('/')
        self.assertContains(response, 'A little less hotel.<br>A little more <em>home.</em>')

    def test_text_edit_is_live_plain_text_and_supports_line_breaks(self):
        item = ContentText.objects.get(page__key='home', text__startswith='A little less hotel.')
        item.text = 'New heading\n<script>alert(1)</script>'
        item.save()
        response = self.client.get('/')
        self.assertContains(response, 'New heading<br>&lt;script&gt;alert(1)&lt;/script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')
        item.text = ''
        item.save()
        self.assertNotContains(self.client.get('/'), 'A little less hotel.')

    def test_about_view_copy_is_editable(self):
        item = ContentText.objects.get(key='about.title')
        item.text = 'Meet Roberto and the crew'
        item.save()
        self.assertContains(self.client.get('/about/'), item.text)
        self.assertContains(self.client.get('/our-story/'), item.text)

    def test_admin_can_save_page_copy(self):
        user = User.objects.create_superuser('editor', password='test')
        self.client.force_login(user)
        page = ContentPage.objects.get(key='booking')
        blocks = list(page.texts.all())
        data = {'texts-TOTAL_FORMS': len(blocks), 'texts-INITIAL_FORMS': len(blocks),
                'texts-MIN_NUM_FORMS': 0, 'texts-MAX_NUM_FORMS': 1000}
        for i, block in enumerate(blocks):
            data.update({f'texts-{i}-id': block.pk, f'texts-{i}-page': page.pk,
                         f'texts-{i}-text': 'Book your island escape' if i == 0 else block.text})
        response = self.client.post(f'/admin/studio/contentpage/{page.pk}/change/', data)
        self.assertEqual(response.status_code, 302)
        self.assertContains(self.client.get('/book/'), 'Book your island escape')

    def test_all_pages_render(self):
        for path in ['/', '/villa/', '/rooms/', '/activities/', '/about/', '/contact/', '/book/', '/cookie-policy/', '/privacy-policy/', '/terms-and-conditions/']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
