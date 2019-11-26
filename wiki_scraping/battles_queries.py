import pandas as pd

# ********************
# Populate db
# ********************
battle_csv = pd.read_csv('battles/battles.csv')
envolved = []
for i in range(battle_csv.shape[0]):
    for key in ['attacker_1', 'attacker_2', 'attacker_3', 'attacker_4', 'defender_1', 'defender_2', 'defender_3', 'defender_4']:
        if type(battle_csv.loc[i, key]) == str:
            envolved.append((battle_csv.loc[i, 'battle_number'], battle_csv.loc[i, key]))


# BATTLE
battle = [{'id_battle': battle_csv.loc[i, 'battle_number'],
           'name_battle': battle_csv.loc[i, 'name'],
           'place_battle': battle_csv.loc[i, 'location']} for i in range(battle_csv.shape[0])]
# HOUSE_BATTLE
house_battle = [{'battle': bt, 'house': 'House ' + hs} for bt, hs in envolved]

print('BATTLE')
for dic in battle:
    print(dic)

print('HOUSE_BATTLE')
for dic in house_battle:
    print(dic)
