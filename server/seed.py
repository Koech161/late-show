import csv
from utilis import db
from models.episode import Episode
from models.appearance import Appearance
from models.guest import Guest
from datetime import datetime
from app import app


def seed_from_csv(csv_file):
    with app.app_context():
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['GoogleKnowlege_Occupation'] == 'NA':
                    continue
                guest = Guest(
                    name=row['Raw_Guest_List'].strip(),
                    occupation=row['GoogleKnowlege_Occupation'].strip()
                )
                db.session.add(guest)
                
                episode_date = datetime.strptime(row['Show'], '%m/%d/%y')
                episode_no = len(Episode.query.all()) + 1
                episode = Episode(
                    date=episode_date,
                    number=episode_no
                )
              
                db.session.add(episode)
                db.session.commit()
                appearance = Appearance(
                    rating=5,
                    episode_id = episode.id,
                    guest_id = guest.id
                )
                db.session.add(appearance)
            db.session.commit()    



if __name__ == '__main__':
    seed_from_csv('./data/seed.csv')
