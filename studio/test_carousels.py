from django.contrib.auth.models import User
from django.test import TestCase
from .models import Activity, Room, RoomPhoto, SiteSettings, VillaPhoto


class CarouselTests(TestCase):
    def test_room_price_wording_is_added_without_duplicates(self):
        for entered, expected in [('45', 'From €45 per person'),
                                  ('From €45 per person / night', 'From €45 per person'),
                                  ('25,50', 'From €25,50 per person'), ('', ''), ('Included', 'Included')]:
            with self.subTest(price=entered):
                self.assertEqual(Room(price=entered).display_price, expected)

    def test_activity_prices_add_euros_and_render_below_description(self):
        for entered, expected in [('60', 'From €60'), ('From 45 per session', 'From €45'),
                                  ('€60 per session', 'From €60'), ('Included', 'Included'),
                                  ('', ''), (' 25,50 ', 'From €25,50')]:
            with self.subTest(price=entered):
                self.assertEqual(Activity(price=entered).display_price, expected)
        activity = Activity.objects.first()
        activity.price = '60 per session'
        activity.save()
        for page in ['/', '/activities/']:
            self.assertContains(self.client.get(page), '<p class="item-price">From €60</p>', html=True)

    def test_villa_photo_order_and_autoplay_setting(self):
        VillaPhoto.objects.create(image='villa/second.png', order=2)
        VillaPhoto.objects.create(image='villa/first.png', order=1, caption='Garden')
        response = self.client.get('/villa/')
        self.assertContains(response, 'data-autoplay="true"')
        html = response.content.decode()
        self.assertLess(html.index('villa/first.png'), html.index('villa/second.png'))
        site = SiteSettings.objects.first()
        site.villa_carousel_autoplay = False
        site.save()
        self.assertContains(self.client.get('/villa/'), 'data-autoplay="false"')

    def test_room_gallery_is_manual_and_prices_are_visible(self):
        room = Room.objects.first()
        room.photo = 'rooms/main.png'
        room.price = 'From €45 per night'
        room.save()
        RoomPhoto.objects.create(room=room, image='rooms/extra.png', caption='Room terrace')
        response = self.client.get('/rooms/')
        self.assertContains(response, 'data-autoplay="false"')
        self.assertNotContains(response, 'data-autoplay="true"')
        self.assertContains(response, 'rooms/main.png')
        self.assertContains(response, 'rooms/extra.png')
        self.assertContains(response, 'Room terrace')
        self.assertContains(response, room.display_price)
        self.assertContains(response, 'aria-label="Next photo"')
        activity = Activity.objects.first()
        activity.price = '€60 per session'
        activity.save()
        self.assertContains(self.client.get('/activities/'), activity.display_price)
        home = self.client.get('/')
        self.assertContains(home, room.display_price)
        self.assertContains(home, activity.display_price)

    def test_admin_exposes_gallery_and_prices(self):
        self.client.force_login(User.objects.create_superuser('owner', password='test'))
        room = Room.objects.first()
        response = self.client.get(f'/admin/studio/room/{room.pk}/change/')
        self.assertContains(response, 'name="price"')
        self.assertContains(response, 'gallery_photos-0-image')
        self.assertEqual(self.client.get('/admin/studio/villaphoto/add/').status_code, 200)
