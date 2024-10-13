from app import app, db
from models import Episode, Guest, Appearance
from faker import Faker
import random

# Initialize Faker
fake = Faker()

def seed_data():
    with app.app_context(): 
        # Create lists to track added guests and episodes
        guests = []
        episodes = []

        # Generate 10 random episodes
        for _ in range(10):
            episode_date = fake.date_this_year()
            episode_number = random.randint(1, 100)
            new_episode = Episode(date=episode_date, number=episode_number)
            db.session.add(new_episode)
            episodes.append(new_episode)

        # Generate 20 random guests
        for _ in range(20):
            guest_name = fake.name()
            occupation = fake.job()
            new_guest = Guest(name=guest_name, occupation=occupation)
            db.session.add(new_guest)
            guests.append(new_guest)

        # Commit episodes and guests to the database
        db.session.commit()

        # Create random appearances, linking guests to episodes
        for _ in range(50): 
            random_episode = random.choice(episodes)
            random_guest = random.choice(guests)
            rating = random.randint(1, 5)
            appearance = Appearance(rating=rating, episode_id=random_episode.id, guest_id=random_guest.id)
            db.session.add(appearance)

        # Commit all appearances
        db.session.commit()
        print("Database seeded successfully with random data.")

if __name__ == "__main__":
    seed_data()
