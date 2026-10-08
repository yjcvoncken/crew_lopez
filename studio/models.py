from django.db import models
from django.core.validators import FileExtensionValidator

image_validator = FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp', 'gif', 'svg'])

class SiteSettings(models.Model):
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
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.FileField(upload_to='rooms/', blank=True, validators=[image_validator])
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'pk']
    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, blank=True)
    short = models.CharField(max_length=180)
    description = models.TextField()
    photo = models.FileField(upload_to='activities/', blank=True, validators=[image_validator])
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'pk']
    def __str__(self):
        return self.name

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
