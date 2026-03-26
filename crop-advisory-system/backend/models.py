"""
Database Models for Crop Advisory System
Uses SQLAlchemy ORM with SQLite
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Crop(db.Model):
    """Model representing a crop."""
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    name_hi = db.Column(db.String(100))
    name_kn = db.Column(db.String(100))
    scientific_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    description_hi = db.Column(db.Text)
    description_kn = db.Column(db.Text)
    season = db.Column(db.String(100))
    season_hi = db.Column(db.String(100))
    season_kn = db.Column(db.String(100))
    image_url = db.Column(db.String(500))

    diseases = db.relationship('Disease', backref='crop', lazy=True)
    pests = db.relationship('Pest', backref='crop', lazy=True)

    def get_name(self, lang='en'):
        if lang == 'hi' and self.name_hi:
            return self.name_hi
        if lang == 'kn' and self.name_kn:
            return self.name_kn
        return self.name

    def to_dict(self, lang='en'):
        return {
            'id': self.id,
            'name': self.get_name(lang),
            'scientific_name': self.scientific_name,
            'description': (self.description_hi if lang == 'hi' and self.description_hi else self.description_kn if lang == 'kn' and self.description_kn else self.description),
            'season': (self.season_hi if lang == 'hi' and self.season_hi else self.season_kn if lang == 'kn' and self.season_kn else self.season),
            'image_url': self.image_url,
            'diseases': [d.to_dict(lang) for d in self.diseases],
            'pests': [p.to_dict(lang) for p in self.pests]
        }

    def to_summary(self, lang='en'):
        return {
            'id': self.id,
            'name': self.get_name(lang),
            'scientific_name': self.scientific_name,
            'season': (self.season_hi if lang == 'hi' and self.season_hi else self.season_kn if lang == 'kn' and self.season_kn else self.season),
            'image_url': self.image_url,
            'disease_count': len(self.diseases),
            'pest_count': len(self.pests)
        }


class Disease(db.Model):
    """Model representing a crop disease."""
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_hi = db.Column(db.String(200))
    name_kn = db.Column(db.String(200))
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    symptoms_hi = db.Column(db.Text)
    symptoms_kn = db.Column(db.Text)
    cause = db.Column(db.String(300))
    cause_hi = db.Column(db.Text)
    cause_kn = db.Column(db.Text)
    prevention = db.Column(db.Text)
    prevention_hi = db.Column(db.Text)
    prevention_kn = db.Column(db.Text)
    organic_treatment = db.Column(db.Text)
    organic_treatment_hi = db.Column(db.Text)
    organic_treatment_kn = db.Column(db.Text)
    chemical_treatment = db.Column(db.Text)
    chemical_treatment_hi = db.Column(db.Text)
    chemical_treatment_kn = db.Column(db.Text)
    chemical_composition = db.Column(db.Text)
    chemical_composition_hi = db.Column(db.Text)
    chemical_composition_kn = db.Column(db.Text)
    severity = db.Column(db.String(50))  # Low, Medium, High
    image_url = db.Column(db.String(500))

    def _l(self, field, lang):
        if lang == 'hi':
            return getattr(self, field + '_hi', None) or getattr(self, field)
        if lang == 'kn':
            return getattr(self, field + '_kn', None) or getattr(self, field)
        return getattr(self, field)

    def get_name(self, lang='en'):
        if lang == 'hi' and self.name_hi:
            return self.name_hi
        if lang == 'kn' and self.name_kn:
            return self.name_kn
        return self.name

    def to_dict(self, lang='en'):
        return {
            'id': self.id,
            'name': self.get_name(lang),
            'crop_id': self.crop_id,
            'crop_name': self.crop.get_name(lang) if self.crop else None,
            'symptoms': self._l('symptoms', lang),
            'cause': self._l('cause', lang),
            'prevention': self._l('prevention', lang),
            'organic_treatment': self._l('organic_treatment', lang),
            'chemical_treatment': self._l('chemical_treatment', lang),
            'chemical_composition': self._l('chemical_composition', lang),
            'severity': self.severity,
            'image_url': self.image_url
        }


class Pest(db.Model):
    """Model representing a crop pest."""
    __tablename__ = 'pests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_hi = db.Column(db.String(200))
    name_kn = db.Column(db.String(200))
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    scientific_name = db.Column(db.String(200))
    symptoms = db.Column(db.Text, nullable=False)
    symptoms_hi = db.Column(db.Text)
    symptoms_kn = db.Column(db.Text)
    damage_type = db.Column(db.String(200))
    damage_type_hi = db.Column(db.String(300))
    damage_type_kn = db.Column(db.String(300))
    prevention = db.Column(db.Text)
    prevention_hi = db.Column(db.Text)
    prevention_kn = db.Column(db.Text)
    organic_treatment = db.Column(db.Text)
    organic_treatment_hi = db.Column(db.Text)
    organic_treatment_kn = db.Column(db.Text)
    chemical_treatment = db.Column(db.Text)
    chemical_treatment_hi = db.Column(db.Text)
    chemical_treatment_kn = db.Column(db.Text)
    chemical_composition = db.Column(db.Text)
    chemical_composition_hi = db.Column(db.Text)
    chemical_composition_kn = db.Column(db.Text)
    severity = db.Column(db.String(50))
    active_season = db.Column(db.String(100))
    active_season_hi = db.Column(db.String(100))
    active_season_kn = db.Column(db.String(100))
    image_url = db.Column(db.String(500))

    def _l(self, field, lang):
        if lang == 'hi':
            return getattr(self, field + '_hi', None) or getattr(self, field)
        if lang == 'kn':
            return getattr(self, field + '_kn', None) or getattr(self, field)
        return getattr(self, field)

    def get_name(self, lang='en'):
        if lang == 'hi' and self.name_hi:
            return self.name_hi
        if lang == 'kn' and self.name_kn:
            return self.name_kn
        return self.name

    def to_dict(self, lang='en'):
        return {
            'id': self.id,
            'name': self.get_name(lang),
            'crop_id': self.crop_id,
            'crop_name': self.crop.get_name(lang) if self.crop else None,
            'scientific_name': self.scientific_name,
            'symptoms': self._l('symptoms', lang),
            'damage_type': self._l('damage_type', lang),
            'prevention': self._l('prevention', lang),
            'organic_treatment': self._l('organic_treatment', lang),
            'chemical_treatment': self._l('chemical_treatment', lang),
            'chemical_composition': self._l('chemical_composition', lang),
            'severity': self.severity,
            'active_season': self._l('active_season', lang),
            'image_url': self.image_url
        }
