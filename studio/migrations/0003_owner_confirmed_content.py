from django.db import migrations


def populate(apps, schema_editor):
    Room = apps.get_model('studio', 'Room')
    rooms = [
        ('Twin room', 'Two single beds, for up to 2 guests. Book privately for one person or a couple, or share with another traveller.'),
        ('Shared room', 'One single bed and one bunk bed in a shared room, for up to 3 guests.'),
        ('Dorm with private bathroom', 'Three bunk beds in a shared dorm, for up to 6 guests, with a private bathroom for the dorm.'),
    ]
    # Replace the original placeholders while retaining uploaded room photos.
    for order, (name, description) in enumerate(rooms, 1):
        room = Room.objects.filter(name=f'Room {order:02}').first()
        if room:
            room.name, room.description, room.order = name, description, order
            room.save()
        else:
            Room.objects.update_or_create(name=name, defaults={'description': description, 'order': order})
    Room.objects.filter(name='Room 04', description='Your place to rest, reset and feel at home.').delete()

    Activity = apps.get_model('studio', 'Activity')
    # Yoga belongs to the included stay rather than the activity catalogue.
    Activity.objects.filter(slug='yoga', short='Breathe. Stretch. Reset.').delete()
    activities = [
        ('Surf', 'surf', '≈', 'Find your wave.', 'Make time for the ocean. Ask the crew about surf options suited to your experience and the conditions.'),
        ('Hikes', 'hikes', '⌁', 'Explore on foot.', 'Discover the island on foot, from volcanic landscapes to wide-open trails. Ask the crew about routes for your pace.'),
        ('Snorkeling', 'snorkeling', '◌', 'A different kind of blue.', 'Explore beneath the surface. Ask the crew about snorkeling options, equipment and suitable conditions.'),
        ('Stargazing', 'stargazing', '✳', 'An evening under the stars.', 'Slow down beneath the island sky. Ask the crew about stargazing during your stay.'),
        ('Surf skate', 'surfskate', '〰', 'Take the flow to land.', 'Bring the feeling of surfing to dry land. Ask the crew about surf skate options and boards.'),
        ('Skate', 'skate', '↝', 'Find your rhythm on wheels.', 'Make room for a skate session between island adventures. Ask the crew about local spots and equipment.'),
        ('4×4 tour', 'four-by-four', '⌁', 'Discover hidden gems.', 'Explore the island’s hidden gems on a 4×4 tour. Ask the crew about routes, schedules and availability.'),
        ('Kite', 'kite', '↗', 'Follow the wind.', 'Discover kite activities on Fuerteventura. Ask the crew about options for your level, equipment and wind conditions.'),
    ]
    for order, (name, slug, icon, short, description) in enumerate(activities, 1):
        Activity.objects.update_or_create(slug=slug, defaults={'name': name, 'icon': icon, 'short': short, 'description': description, 'order': order})


class Migration(migrations.Migration):
    dependencies = [('studio', '0002_initial_content')]
    operations = [migrations.RunPython(populate, migrations.RunPython.noop)]
