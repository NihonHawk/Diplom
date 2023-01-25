from sqlalchemy import exists
from math import ceil
import json

from package.models import (session, Character, Character_ascension, Talent_ascension,
Weapon, Weapon_ascension, Material, Alchemy)


def initial(name, first, second):
    if session.query(exists().where(Character.name == name)).first()[0] == True and second <= 10:
        return talent(name, first, second)
    if session.query(exists().where(Character.name == name)).first()[0] == True and second >= 20:
        return character(name, first, second)
    if session.query(exists().where(Weapon.name == name)).first()[0] == True:
        return weapon(name, first, second)
    session.close()

def addition(result, massive, x):
    if result["table"] == "character":
        value = 20000
        result["book"] += ceil(massive[x][0]/value)
        result["mora"] += massive[x][1] + (massive[x+1][6] if x!=6 else 0)
        if x >= 1:
            result["local_material"]["value"] += massive[x][4]
        if x >=2:
            result["elemental_core"]["value"] += massive[x][3]
        match x:
            case 1:
                result["elemental_crystal"]["tier2"] += massive[x][2]
                result["common_material"]["tier1"] += massive[x][5]
            case 2:
                result["elemental_crystal"]["tier3"] += massive[x][2]
                result["common_material"]["tier1"] += massive[x][5]
            case 3:
                result["elemental_crystal"]["tier3"] += massive[x][2]
                result["common_material"]["tier2"] += massive[x][5]
            case 4:
                result["elemental_crystal"]["tier4"] += massive[x][2]
                result["common_material"]["tier2"] += massive[x][5]
            case 5:
                result["elemental_crystal"]["tier4"] += massive[x][2]
                result["common_material"]["tier3"] += massive[x][5]
            case 6:
                result["elemental_crystal"]["tier5"] += massive[x][2]
                result["common_material"]["tier3"] += massive[x][5]

    if result["table"] == "weapon":
        value = 10000
        result["ore"] += ceil(massive[x][0]/value)
        result["mora"] += massive[x][1] + (massive[x+1][5] if x!=6 else 0)
        match x:
            case 1:
                result["domain_material"]["tier2"] += massive[x][2]
                result["elite_material"]["tier2"] += massive[x][3]
                result["common_material"]["tier1"] += massive[x][4]
            case 2:
                result["domain_material"]["tier3"] += massive[x][2]
                result["elite_material"]["tier2"] += massive[x][3]
                result["common_material"]["tier1"] += massive[x][4]
            case 3:
                result["domain_material"]["tier3"] += massive[x][2]
                result["elite_material"]["tier3"] += massive[x][3]
                result["common_material"]["tier2"] += massive[x][4]
            case 4:
                result["domain_material"]["tier4"] += massive[x][2]
                result["elite_material"]["tier3"] += massive[x][3]
                result["common_material"]["tier2"] += massive[x][4]
            case 5:
                result["domain_material"]["tier4"] += massive[x][2]
                result["elite_material"]["tier4"] += massive[x][3]
                result["common_material"]["tier3"] += massive[x][4]
            case 6:
                result["domain_material"]["tier5"] += massive[x][2]
                result["elite_material"]["tier4"] += massive[x][3]
                result["common_material"]["tier3"] += massive[x][4]
        
    if result["table"] == "talent":
        result["mora"] += massive[x][0]
        match x:
            case 2:
                result["book"]["tier2"] += massive[x][1]
                result["common_material"]["tier1"] += massive[x][2]
            case 3:
                result["book"]["tier3"] += massive[x][1]
                result["common_material"]["tier2"] += massive[x][2]
            case 4:
                result["book"]["tier3"] += massive[x][1]
                result["common_material"]["tier2"] += massive[x][2]
            case 5:
                result["book"]["tier3"] += massive[x][1]
                result["common_material"]["tier2"] += massive[x][2]
            case 6:
                result["book"]["tier3"] += massive[x][1]
                result["common_material"]["tier2"] += massive[x][2]
            case 7:
                result["book"]["tier4"] += massive[x][1]
                result["common_material"]["tier3"] += massive[x][2]
                result["boss_material"]["value"] += massive[x][3]
            case 8:
                result["book"]["tier4"] += massive[x][1]
                result["common_material"]["tier3"] += massive[x][2]
                result["boss_material"]["value"] += massive[x][3]
            case 9:
                result["book"]["tier4"] += massive[x][1]
                result["common_material"]["tier3"] += massive[x][2]
                result["boss_material"]["value"] += massive[x][3]
            case 10:
                result["book"]["tier4"] += massive[x][1]
                result["common_material"]["tier3"] += massive[x][2]
                result["boss_material"]["value"] += massive[x][3]
                result["crown"] += 1


def character(name, first, second):
    query = session.query(Character_ascension).where(Character_ascension.character == name).first()
    crystal = session.query(Material).where(Material.name.like(f"% {query.crystal}")).order_by(Material.tier.asc()).all()
    common = session.query(Alchemy).where(Alchemy.tierI == query.common).first()
    session.close()

    result = json.loads('''
    {
        "table" : "character",
        "name" : "",
        "book" : 0,
        "mora" : 0,
        "elemental_crystal" : {"tier2" : 0, "tier3" : 0,"tier4" : 0,"tier5" : 0},
        "elemental_core" : {"name" : "", "value" : 0},
        "local_material" : {"name" : "", "value" : 0},
        "common_material" : {"tier1" : 0, "tier2" : 0, "tier3" : 0}
    }
    ''')

    result["name"] = name
    result["elemental_core"]["name"] = query.elemental_core
    result["local_material"]["name"] = query.local

    massive = {
    # stage : [exp, moraforexp, em1, em2, local, common, price ]
        0 : [120175, 24035, 0, 0, 0, 0, 0, 0],
        1 : [578325, 115665, 1, 0, 3, 3, 20000],
        2 : [579100, 115820, 3, 2, 10, 15, 40000],
        3 : [854125, 170825, 6, 4, 20, 12, 60000],
        4 : [1195925, 239185, 3, 8, 30, 18, 80000],
        5 : [1611875, 322375, 6, 12, 45, 16, 100000],
        6 : [3423125, 684625, 6, 20, 60, 24, 120000]
    }

    while True:
        if first < second:
            if first in range(1,41):
                addition(result, massive, first//20)
                first += 20
            else:
                addition(result, massive, first//10-2)
                first += 10
        else:
            break

    x=0
    for k in list(result["elemental_crystal"].keys()):
        result["elemental_crystal"][crystal[x].name] = result["elemental_crystal"].pop(k)
        x+=1

    result["common_material"][common.tierI] = result["common_material"].pop("tier1")
    result["common_material"][common.tierII] = result["common_material"].pop("tier2")
    result["common_material"][common.tierIII] = result["common_material"].pop("tier3")

    return json.dumps(result, ensure_ascii=False)


def weapon(name, first, second):
    query = session.query(Weapon, Weapon_ascension).join(Weapon_ascension).where(Weapon.name == name).first()
    domain = session.query(Alchemy).where(Alchemy.tierII == query[1].domain_material).first()
    elite = session.query(Alchemy).where(Alchemy.tierII == query[1].elite_material).first()
    common = session.query(Alchemy).where(Alchemy.tierI == query[1].common_material).first()
    session.close()

    result = json.loads('''
    {
        "table" : "weapon",
        "name" : "",
        "ore" : 0,
        "mora" : 0,
        "domain_material" : {"tier2" : 0, "tier3" : 0, "tier4" : 0, "tier5" : 0},
        "elite_material" : {"tier2" : 0, "tier3" : 0, "tier4" : 0},
        "common_material" : {"tier1" : 0, "tier2" : 0, "tier3" : 0}
    }
    ''')

    if query[0].rare == 4:
        massive = {
        # stage : [exp, moraforexp, asc_material, com1, com2, price ]
            0 : [81000, 8100, 0, 0, 0, 0],
            1 : [415125, 41513, 3, 3, 2, 5000],
            2 : [418725, 41873, 3, 12, 8, 15000],
            3 : [618400, 61840, 6, 6, 6, 20000],
            4 : [866050, 86605, 3, 12, 9, 30000],
            5 : [1166875, 116688, 9, 9, 6, 35000],
            6 : [2476475, 247648, 4, 18, 12, 45000]
        }
    else:
        massive = {
        # stage : [exp, moraforexp, asc_material, com1, com2, price ]
            0 : [121550, 12155, 0, 0, 0, 0],
            1 : [622800, 62280, 5, 5, 3, 10000],
            2 : [628150, 62815, 5, 18, 12, 20000],
            3 : [927675, 92768, 9, 9, 9, 30000],
            4 : [1299125, 129913, 5, 18, 14, 45000],
            5 : [1750375, 175038, 9, 14, 9, 55000],
            6 : [3714775, 371478, 6, 27, 18, 65000]
        }

    while True:
        if first < second:
            if first in range(1,41):
                addition(result, massive, first//20)
                first += 20
            else:
                addition(result, massive, first//10-2)
                first += 10
        else:
            break
            
    result["name"] = query[0].name
    result["domain_material"][domain.tierII] = result["domain_material"].pop("tier2")
    result["domain_material"][domain.tierIII] = result["domain_material"].pop("tier3")
    result["domain_material"][domain.tierIV] = result["domain_material"].pop("tier4")
    result["domain_material"][domain.tierV] = result["domain_material"].pop("tier5")
    result["elite_material"][elite.tierII] = result["elite_material"].pop("tier2")
    result["elite_material"][elite.tierIII] = result["elite_material"].pop("tier3")
    result["elite_material"][elite.tierIV] = result["elite_material"].pop("tier4")
    result["common_material"][common.tierI] = result["common_material"].pop("tier1")
    result["common_material"][common.tierII] = result["common_material"].pop("tier2")
    result["common_material"][common.tierIII] = result["common_material"].pop("tier3")

    return json.dumps(result, ensure_ascii=False)


def talent(name, first, second):
    query = session.query(Talent_ascension).where(Talent_ascension.character == name).first()
    domain = session.query(Alchemy).where(Alchemy.tierII==query.domain_material).first()
    common = session.query(Alchemy).where(Alchemy.tierI==query.common).first()
    session.close()

    result = json.loads('''
    {
        "table" : "talent",
        "name" : "",
        "mora" : 0,
        "book" : {"tier2" : 0, "tier3" : 0,"tier4" : 0},
        "common_material" : {"tier1" : 0, "tier2" : 0, "tier3" : 0},
        "boss_material" : {"name" : "", "value" : 0},
        "crown" : 0
    }
    ''')

    massive = {
    # lvl : mora, tmaterial, com, boss
        2 : [12500, 3, 6, 0],
        3 : [17500, 2, 3, 0],
        4 : [25000, 4, 4, 0],
        5 : [30000, 6, 6, 0],
        6 : [37500, 9, 9, 0],
        7 : [120000, 4, 4, 1],
        8 : [260000, 6, 6, 1],
        9 : [450000, 12, 9, 2],
        10 : [700000, 16, 12, 2]
    }

    while first < second:
        addition(result, massive, first+1)
        first += 1

    result["name"] = query.character
    result["book"][domain.tierII] = result["book"].pop("tier2")
    result["book"][domain.tierIII] = result["book"].pop("tier3")
    result["book"][domain.tierIV] = result["book"].pop("tier4")
    result["common_material"][common.tierI] = result["common_material"].pop("tier1")
    result["common_material"][common.tierII] = result["common_material"].pop("tier2")
    result["common_material"][common.tierIII] = result["common_material"].pop("tier3")
    result["boss_material"]["name"] = query.world_boss

    return json.dumps(result, ensure_ascii=False)