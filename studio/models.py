import re

from django.db import models
from django.core.validators import FileExtensionValidator

image_validator = FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp', 'gif', 'svg'])

class SiteImage(models.Model):
    name = models.CharField(max_length=150)
    key = models.CharField(max_length=200, unique=True)
    image = models.FileField(upload_to='site-images/', blank=True, validators=[image_validator], help_text='Upload a replacement. Leave empty to use the original site image.')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Photos(SiteImage):
    class Meta:
        proxy = True
        verbose_name_plural = 'Photos'


class SiteSettings(models.Model):
    villa_carousel_autoplay = models.BooleanField(default=True, help_text='Automatically rotate the Explore the Villa photos. Visitors can pause playback.')
    hero_title = models.CharField(max_length=160, default='Your people far from home')
    hero_description = models.TextField(default='Salty hair. Shared stories. A place to belong. Your next chapter starts in Lajares.')
    homepage_photo = models.FileField(upload_to='site/', blank=True, validators=[image_validator])
    graphic_element = models.FileField(upload_to='site/', blank=True, validators=[image_validator], help_text='Upload a brand illustration from the supplied graphics. It appears beside the welcome text.')
    booking_url = models.URLField(default='https://www.booking.com/Share-RfTbCF')
    business_name = models.CharField(max_length=200, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    business_address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    policies_approved = models.BooleanField(default=False, help_text='Only enable after the owner has reviewed the policies and completed the legal details.')
    privacy_text = models.TextField(blank=True, help_text='Optional owner-reviewed privacy policy. Plain text, with blank lines between paragraphs.')
    cookie_text = models.TextField(blank=True, help_text='Optional owner-reviewed cookie policy.')
    terms_text = models.TextField(blank=True, help_text='Optional owner-reviewed booking and site terms.')
    def __str__(self):
        return 'Website content & legal details'

class Room(models.Model):
    price = models.CharField(max_length=120, blank=True, help_text='For example: From €45 per person / night. Leave blank to hide.')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.FileField(upload_to='rooms/', blank=True, validators=[image_validator])
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'pk']
    def __str__(self):
        return self.name

class Activity(models.Model):
    price = models.CharField(max_length=120, blank=True, help_text='For example: €60 per session, or Included. Leave blank to hide.')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, blank=True)
    short = models.CharField(max_length=180)
    description = models.TextField()
    photo = models.FileField(upload_to='activities/', blank=True, validators=[image_validator])
    order = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['order', 'pk']
    def __str__(self):
        return self.name

    @property
    def display_price(self):
        price = self.price.strip()
        if '€' in price:
            return price
        return re.sub(r'\d', lambda match: '€' + match.group(), price, count=1)

class BlogPost(models.Model):
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=80, default='Island notes')
    summary = models.TextField()
    body = models.TextField()
    published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'pk']
    def __str__(self):
        return self.title


class VillaPhoto(models.Model):
    image = models.FileField(upload_to='villa/', validators=[image_validator])
    caption = models.CharField(max_length=200, blank=True, help_text='Description of the photo for accessibility.')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'pk']

    def __str__(self):
        return self.caption or f'Villa photo {self.pk or "new"}'


class RoomPhoto(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='gallery_photos')
    image = models.FileField(upload_to='rooms/', validators=[image_validator])
    caption = models.CharField(max_length=200, blank=True, help_text='Description of the photo for accessibility.')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'pk']

    def __str__(self):
        return self.caption or f'{self.room} photo'
