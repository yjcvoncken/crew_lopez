from django.db import migrations

def populate(apps, schema_editor):
    Settings = apps.get_model('studio', 'SiteSettings')
    Settings.objects.get_or_create(pk=1)
    Room = apps.get_model('studio', 'Room')
    for n in range(1, 5):
        Room.objects.get_or_create(order=n, defaults={'name': f'Room {n:02}', 'description': 'Your place to rest, reset and feel at home.'})
    Activity = apps.get_model('studio', 'Activity')
    activities = [
        ('Surf', 'surf', '≈', 'Find your wave.', 'First wave or a familiar feeling, make time for the ocean. Ask the crew about local surf lessons, equipment and options for your level.'),
        ('Yoga', 'yoga', '☼', 'Breathe. Stretch. Reset.', 'Slow down and reconnect with your body. Ask about yoga options during your stay, from a gentle stretch to movement between surf sessions.'),
        ('Surfskate', 'surfskate', '〰', 'Take the flow to land.', 'Explore the feeling of carving on dry land. Ask about surfskate sessions, boards and a suitable place to get started.'),
        ('Snorkeling', 'snorkeling', '◌', 'A different kind of blue.', 'Discover what lies beneath the surface. Ask about local snorkeling trips and equipment. Conditions decide when and where to enter the water.'),
        ('Four by four', 'four-by-four', '⌁', 'Follow a new road.', 'Head out to see more of the island with a local provider. Ask about guided four-by-four trips, routes and availability.'),
        ('Stargazing', 'stargazing', '✳', 'Look a little further.', 'Trade the screen for the night sky. Ask the crew about a stargazing evening and local guided options. Clear skies set the scene.'),
    ]
    for n, (name, slug, icon, short, description) in enumerate(activities, 1):
        Activity.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon, 'short': short, 'description': description, 'order': n})
    Post = apps.get_model('studio', 'BlogPost')
    entries = [
        ('Your first day with the crew', 'Community', 'Drop your bags. Pull up a chair. Let the island set the pace.', 'Start by settling into the house and saying hello to the people around you. Find the shared kitchen, choose a spot for your morning coffee and ask the crew what is happening during your stay.\n\nDinner together is an easy way to get to know your fellow guests. Bring a story, listen to someone else’s and see where the conversation takes you.'),
        ('A little preparation for your surf trip', 'Surf life', 'Pack light, bring curiosity and leave room for the unexpected.', 'Bring comfortable layers, sun protection, a reusable water bottle and something warm for the evening. Ask your activity provider about boards, wetsuits and anything else you need before booking a session.\n\nBe honest about your experience. A suitable lesson and good local advice make a better start than chasing the biggest wave. Follow your instructor and give yourself time to learn.'),
        ('Take the slow way', 'Island life', 'Some of the best days have very little on the schedule.', 'Make room for an unplanned morning. Walk into the village, stop for coffee and ask someone at the house about their favourite place to spend an afternoon.\n\nYou do not need to fit everything into one visit. Pick one thing you want to do, leave time to rest and enjoy the people you meet along the way.'),
    ]
    for n, (title, category, summary, body) in enumerate(entries, 1):
        Post.objects.get_or_create(title=title, defaults={'category': category, 'summary': summary, 'body': body, 'order': n})

class Migration(migrations.Migration):
    dependencies = [('studio', '0001_initial')]
    operations = [migrations.RunPython(populate, migrations.RunPython.noop)]
