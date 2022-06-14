def initiative(party, enemy_party):
    camp_battle = party + enemy_party
    camp_battle_speed = []

    for i in range(len(camp_battle)):

        if i < len(party):
            speed = game_state["main_party"]["characters"][camp_battle[i]]["state"]["speed"]
        else:
            speed = game_state["enemy_party"]["enemies"][camp_battle[i]]["state"]["speed"]

        camp_battle_speed.append(speed)

    for i in range(len(camp_battle)):
        major_index = i

        for j in range(i + 1, len(camp_battle)):
            if camp_battle_speed[j] > camp_battle_speed[major_index]:
                major_index = j

        (camp_battle_speed[i], camp_battle_speed[major_index]) = (camp_battle_speed[major_index], camp_battle_speed[i])
        (camp_battle[i], camp_battle[major_index]) = (camp_battle[major_index], camp_battle[i])

    return camp_battle


game_state = {
    "main_party": {
        "characters": {
            "Nikolal Legal": {
                "state": {
                    "speed": 10,
                    "atk": 2
                }
            },
            "Kawan": {
                "state": {
                    "speed": 8,
                    "atk": 2
                }
            }

        }
    },
    "enemy_party": {
        "enemies": {
            "Homem peixe": {
                "state": {
                    "speed": 9,
                    "atk": 2
                }
            },
            "Peixe Homem": {
                "state": {
                    "speed": 2,
                    "atk": 2
                }
            }
        }
    }
}

party_perso = ["Nikolal Legal", "Kawan"]
party_inimigo = ["Homem peixe", "Peixe Homem"]

print(initiative(party_perso, party_inimigo))
