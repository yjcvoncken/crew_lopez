from django.shortcuts import render
from .models import Room, Activity, BlogPost

PAGES = {
    "villa": {"title":"Explore the Villa", "kicker":"Your island base", "intro":"A slow home for salty days.", "copy":"White walls, volcanic stone, shared tables and plenty of corners to disappear into. Crew Lopez is designed for the good rhythm: surf early, eat well, stretch out, repeat.", "items":[("The garden","Take your coffee outside and find a quiet corner."),("The kitchen","A generous shared kitchen and long table made for unhurried breakfasts and family dinners."),("The hangout","Soft seats, strong Wi-Fi, books, games and a place to plan tomorrow’s waves."),("The terrace","Fresh air, island light and somewhere to plan your next adventure.")]},
    "rooms": {"title":"Rest easy. Stay connected.", "kicker":"Your island stay", "intro":"A bed for the night. A crew for the journey.", "copy":"Our shared accommodation brings independent travellers together. Settle into the rhythm of the house, meet your neighbours and make yourself at home. Check the current room descriptions, facilities and availability on Booking.com before reserving.", "items":[("Shared stays","A single bed in a shared dormitory, with room to rest after an island day."),("Your bathroom options","Bathroom arrangements vary by accommodation. Find the details for your chosen bed on Booking.com."),("Breakfast together","Start the day with breakfast and a little conversation. Check your selected rate for what’s included."),("Plan your visit","Check-in is from 14:00 to 22:00. Check-out is by 11:00. Review current terms when booking.")]},
    "activities": {"title":"Activities", "kicker":"Beyond the house", "intro":"Follow the swell. Find your pace.", "copy":"Fuerteventura gives you room to move. From the water to the volcanic trails, find inspiration for your island days. Ask about local options and availability before planning an activity.", "items":[("Surf coaching","Looking for your first wave? Ask about local coaching options matched to your experience."),("Surf guiding","Local knowledge for independent surfers who want to spend less time searching."),("Yoga & mobility","Take time to stretch, breathe and recover. Ask about local classes during your stay."),("Island days","Volcano walks, hidden beaches, local food and wide-open roads.")]},
    "story": {"title":"Our Story", "kicker":"Meet the crew", "intro":"A house built around the feeling of belonging.", "copy":"Crew Lopez began with a simple idea: create the surf stay we always wanted to find, personal, design-minded, relaxed and genuinely connected to its island home. Not a packed camp. Not an anonymous hotel. A place where names are remembered and plans happen around the breakfast table.", "items":[("Small by nature","Fewer guests means more attention, more space and a better atmosphere."),("Local by choice","We work with island-based teachers, makers and guides."),("Surf at the centre","Conditions lead the day, with room for every level and appetite."),("Come as you are","Solo, together, first wave or five hundredth, you are part of the crew.")]},
    "blog": {"title":"Island Notes", "kicker":"The Crew Lopez journal", "intro":"Stories for the road and the water.", "copy":"Useful guides, honest island recommendations and a little inspiration for your next Atlantic escape.", "items":[("When to surf Fuerteventura","A season-by-season guide to swell, wind and what to pack."),("A slow day in the north","Coffee, volcanoes, local lunch and a sunset swim."),("Your first surf trip","What to expect, how to prepare and why nobody starts out looking graceful."),("Lajares, our home","The quiet northern village that keeps us close to everything.")]},
}

def home(request):
    return render(request, "studio/home.html", {"rooms": Room.objects.all(), "activities": Activity.objects.all()})

def detail(request, slug):
    page = PAGES[slug]
    template = {"villa": "studio/villa.html", "rooms": "studio/rooms.html", "activities": "studio/activities.html", "blog": "studio/blog.html"}.get(slug, "studio/detail.html")
    return render(request, template, {"page": page, "slug": slug, "rooms": Room.objects.all(), "activities": Activity.objects.all(), "posts": BlogPost.objects.filter(published=True)})

def contact(request):
    return render(request, "studio/contact.html")

def policy(request, kind):
    titles = {'cookie': 'Cookie policy', 'privacy': 'Privacy policy', 'terms': 'Terms & conditions'}
    return render(request, 'studio/policy.html', {'kind': kind, 'policy_title': titles[kind]})
