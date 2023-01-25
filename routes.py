from flask import render_template, request, redirect, url_for, flash

from start import app
from package.models import *
from package.daily import daily_material
from package.tracker import tracker, update
from package.parser import parser
from package.calculator import initial


@app.route('/')
def index():
    dungeon = session.query(Daily_material).all()
    weapon = session.query(Weapon).all()
    session.close()
    result = daily_material()
    return render_template('index.html', title="Today", result=result, dungeon=dungeon, weapon=weapon)

@app.route('/tracker')
def tracker_display():
    result = tracker()
    return render_template('tracker.html', title="Tracker", result=result)

@app.route('/tracker/update', methods=['POST'])
def tracker_update():
    update(request.get_json()["name"])
    return f"status was updated"

@app.route('/news')
def info():
    # get async
    news = parser.get_news()
    codes = parser.get_codes()
    return render_template('posts.html', title="News", news=news, codes=codes)
    
@app.route('/calculator', methods=['GET','POST'])
def calculator():
    characters = session.query(Character.name).all()
    weapons  = session.query(Weapon.name).all()
    session.close()
    return render_template('calculator.html', title="Calculator", characters=characters, weapons=weapons)

@app.route('/calculator/get', methods=['POST'])
def doit():
    get_post = request.get_json()
    result = initial(
        get_post['name'],
        get_post['first_level'], 
        get_post['second_level']
    )
    return result

@app.route('/db/characters')
def characters():
    result = session.query(Character, Character_ascension, Talent_ascension)\
                    .where(Character_ascension.character==Character.name, 
                           Talent_ascension.character==Character.name).order_by(Character.name.asc()).all()
    session.close()
    return render_template("tables/characters.html", title="Characters", result=result)

@app.route('/db/weapons/swords')
def swords():
    result = session.query(Weapon, Weapon_ascension)\
                    .where(Weapon_ascension.weapon==Weapon.name, Weapon.form == "Одноручное")\
                    .order_by( Weapon.rare.desc(),Weapon.name.asc()).all()
    session.close()
    return render_template("tables/weapons.html", title="Swords", result=result)

@app.route('/db/weapons/claymores')
def claymores():
    result = session.query(Weapon, Weapon_ascension)\
                    .where(Weapon_ascension.weapon==Weapon.name, Weapon.form == "Двуручное")\
                    .order_by( Weapon.rare.desc(),Weapon.name.asc()).all()
    session.close()
    return render_template("tables/weapons.html", title="Claymores", result=result)

@app.route('/db/weapons/polearms')
def polearms():
    result = session.query(Weapon, Weapon_ascension)\
                    .where(Weapon_ascension.weapon==Weapon.name, Weapon.form == "Древковое")\
                    .order_by( Weapon.rare.desc(),Weapon.name.asc()).all()
    session.close()
    return render_template("tables/weapons.html", title="Polearms", result=result)

@app.route('/db/weapons/bows')
def bows():
    result = session.query(Weapon, Weapon_ascension)\
                    .where(Weapon_ascension.weapon==Weapon.name, Weapon.form == "Стрелковое")\
                    .order_by( Weapon.rare.desc(),Weapon.name.asc()).all()
    session.close()
    return render_template("tables/weapons.html", title="Bows", result=result)

@app.route('/db/weapons/catalysts')
def catalysts():
    result = session.query(Weapon, Weapon_ascension)\
                    .where(Weapon_ascension.weapon==Weapon.name, Weapon.form == "Катализатор")\
                    .order_by( Weapon.rare.desc(),Weapon.name.asc()).all()
    session.close()
    return render_template("tables/weapons.html", title="Catalysts", result=result)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response
