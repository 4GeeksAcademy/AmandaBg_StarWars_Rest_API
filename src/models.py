from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People (db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    url = db.Column(db.String(200), unique=True, nullable=False)
    
    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "url": self.url
         }


class Favorite_People (db.Model):
    __tablename__ = 'favorite_people'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_people = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    user = db.relationship(User)
    people = db.relationship(People)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        return{
            "id_people": self.id_people
        }
    

class Planets (db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    url = db.Column(db.String(200), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Planet %r>' % self.name
        
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "url": self.url
        }


class Favorite_Planets (db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_planet = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    user = db.relationship(User)
    planet = db.relationship(Planets)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        return{
            "id_planet": self.id_planet
        }
    





    

