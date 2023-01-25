from datetime import datetime as date

from package.models import Daily_material, Talent_ascension, Weapon_ascension, Character, Weapon, session


def daily_material():
    today = date.today().isoweekday()
    if 0 <= int(date.now().strftime("%H")) < 5:
        today -= 1

    match today:
        case 1|4:
            talent = session.query(Daily_material).where(
                Daily_material.day == "Пн Чт", 
                Daily_material.form == "Повышение талантов" 
            )
            weapon = session.query(Daily_material).where(
                Daily_material.day == "Пн Чт", 
                Daily_material.form== "Возвышение оружия" 
            )
        case 2|5:
            talent = session.query(Daily_material).where(
                Daily_material.day == "Вт Пт", 
                Daily_material.form == "Повышение талантов" 
            )
            weapon = session.query(Daily_material).where(
                Daily_material.day == "Вт Пт", 
                Daily_material.form== "Возвышение оружия" 
            )
        case 3|6:
            talent = session.query(Daily_material).where(
                Daily_material.day == "Ср Сб", 
                Daily_material.form == "Повышение талантов" 
            )
            weapon = session.query(Daily_material).where(
                Daily_material.day == "Ср Сб", 
                Daily_material.form == "Возвышение оружия" 
            )
        case 7:
            talent = session.query(Daily_material).where(Daily_material.form == "Повышение талантов")
            weapon = session.query(Daily_material).where(Daily_material.form == "Возвышение оружия")

    result = {}

    for items in talent:
        query = session.query(Talent_ascension.character, Character.rare)\
            .join(Character, Talent_ascension.character == Character.name)\
            .where(Talent_ascension.domain_material == items.name)\
            .order_by(Character.rare.desc())
        result.update({items.name : []})
        for x in query:
            result[items.name].append(x.character)

    for items in weapon:
        query = session.query(Weapon_ascension.weapon, Weapon.rare)\
            .join(Weapon, Weapon_ascension.weapon == Weapon.name)\
            .where(Weapon_ascension.domain_material == items.name)\
            .order_by(Weapon.rare.desc())
            # .limit(6)
        result.update({items.name : []})
        for x in query:
            result[items.name].append(x.weapon)

    session.close()
    return result
