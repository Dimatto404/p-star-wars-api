from src.models import db, User, Character, Planet, Favorite
from src.app import app

def load_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        user1 = User(email="luke@skywalker.com", password="123456", is_active=True)
        user2 = User(email="leia@organa.com", password="654321", is_active=True)
        db.session.add(user1)
        db.session.add(user2)

        character1 = Character(name="Luke Skywalker", height="172", mass="77", hair_color="blond", skin_color="fair", eye_color="blue", birth_year="19BBY", gender="male")
        character2 = Character(name="Leia Organa", height="150", mass="49", hair_color="brown", skin_color="light", eye_color="brown", birth_year="19BBY", gender="female")
        db.session.add(character1)
        db.session.add(character2)

        planet1 = Planet(name="Tatooine", climate="arid", terrain="desert", population="200000")
        planet2 = Planet(name="Alderaan", climate="temperate", terrain="grasslands, mountains", population="2000000000")
        db.session.add(planet1)
        db.session.add(planet2)

        favorite1 = Favorite(user_id=1, planet_id=1)
        favorite2 = Favorite(user_id=1, people_id=2)
        favorite3 = Favorite(user_id=2, planet_id=2)
        db.session.add(favorite1)
        db.session.add(favorite2)
        db.session.add(favorite3)

        db.session.commit()
        print("Datos de carga insertados exitosamente.")


if __name__ == "__main__":
    load_data()