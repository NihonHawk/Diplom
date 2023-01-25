from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, Text, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///data/genshindb.sqlite')
Session = sessionmaker(engine)
session = Session()


class Character(Base):
    __tablename__ = "character"

    name = Column(String, primary_key=True)
    rare = Column(Integer)
    weapon = Column(String)
    element = Column(String)
    const = Column(String)

class Character_info(Base):
    __tablename__ = "character_info"

    name = Column(String, ForeignKey(Character.name), primary_key=True)
    bio = Column(Text)
    gender = Column(CHAR)
    group = Column(String)
    birth = Column(String)
    
class Character_constellation(Base):
    __tablename__ = "character_constellation"

    name = Column(String, primary_key=True)
    level = Column(Integer)
    description = Column(Text)
    const = Column(ForeignKey(Character.const))

class Character_talent(Base):
    __tablename__ = "character_talent"

    name = Column(String, primary_key=True)
    description = Column(Text)
    character = Column(ForeignKey(Character.name))

class Weapon(Base):
    __tablename__ = "weapon"

    name = Column(String, primary_key=True)
    form = Column(String)
    rare = Column(Integer) 
    atk = Column(Integer)
    sub_stat = Column(String)
    value = Column(Float)
            
class Weapon_info(Base):
    __tablename__ = "weapon_info"

    name = Column(String, ForeignKey(Weapon.name), primary_key=True)
    description = Column(String)
    skill_name = Column(String) 
    skill_desc = Column(Text)

class Material(Base):
    __tablename__ = "material"

    name = Column(String, primary_key=True)
    form = Column(String)
    tier = Column(Integer) 
    description = Column(Text) 
    obtained = Column(Text) 

class Domain(Base):
    __tablename__ = "domain"

    name = Column(String, primary_key=True)
    region = Column(String)
    description = Column(Text)

class Artifact(Base):
    __tablename__ = "artifact"

    name = Column(String, primary_key=True)
    two = Column(Text)
    four = Column(Text)
    domain = Column(ForeignKey(Domain.name)) 

class Artifact_description(Base):
    __tablename__ = "artifact_description"

    name = Column(String, ForeignKey(Artifact.name), primary_key=True)
    flower = Column(Text)
    plume = Column(Text)
    goblet = Column(Text) 
    sand = Column(Text) 
    circlet = Column(Text) 

class Daily_material(Base):
    __tablename__ = "daily_material"

    name = Column(String, ForeignKey(Material.name), primary_key=True)
    form = Column(String)
    day = Column(Integer)
    domain = Column(ForeignKey(Domain.name)) 

class Weapon_ascension(Base):
    __tablename__ = "weapon_ascension"

    weapon = Column(String, ForeignKey(Weapon.name), primary_key=True)
    domain_material = Column(ForeignKey(Daily_material.name))
    elite_material = Column(String)
    common_material = Column(String) 

class Character_ascension(Base):
    __tablename__ = "character_ascension"

    character = Column(String, ForeignKey(Character.name), primary_key=True)
    crystal = Column(String)
    elemental_core = Column(String)
    local = Column(String) 
    common = Column(String) 

class Talent_ascension(Base):
    __tablename__ = "talent_ascension"

    character = Column(String, ForeignKey(Character.name), primary_key=True)
    domain_material = Column(ForeignKey(Daily_material.name))
    world_boss = Column(String) 
    common = Column(String) 

class Alchemy(Base):
    __tablename__ = "alchemy"

    name = Column(String, primary_key=True)
    tierI = Column(String)
    tierII = Column(String)
    tierIII = Column(String)
    tierIV = Column(String)
    tierV = Column(String)


Base.metadata.create_all(engine)