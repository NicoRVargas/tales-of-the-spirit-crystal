from collections import namedtuple
from random import randint
from time import sleep

game = namedtuple("State", "create_character create_enemy character_printer enemy_printer fight menu")


def create_game():
    game_state = {
        "main_party": {
            "characters": {}
        },
        "enemy_party": {
            "enemies": {}
        }
    }

    def menu(characters, enemies):
        def linha(tam=50):
            print("-=" * tam)

        def cabecalho(txt):
            linha()
            print(txt.center(100))
            linha()

        def template_menu():
            c = 0
            for character in range(characters):
                if c == 0:
                    hp_bar = f"{4 * ' '}HP:{character_open(character)['hp']}/{character_open(character)['hp_maximum']}{4 * ' '}"
                    ki_bar = f"KI:{character_open(character)['ki']}/{character_open(character)['ki_maximum']}{4 * ' '}"
                    level_bar = f"LVL:{character_open(character)['level']}"
                    txt_cabecalho = character + hp_bar + ki_bar + level_bar
                    cabecalho(txt_cabecalho)
                    c += 1
                else:
                    hp_bar = f"{4 * ' '}HP:{character_open(character)['hp']}/{character_open(character)['hp_maximum']}{4 * ' '}"
                    ki_bar = f"KI:{character_open(character)['ki']}/{character_open(character)['ki_maximum']}{4 * ' '}"
                    level_bar = f"LVL:{character_open(character)['level']}"
                    print(f"{character}{4 * ' '}{hp_bar}{4 * ' '}{ki_bar}{4 * ' '}{level_bar}")
            try:
                print(f"{5 * ' '}{enemies}{5 * ' '}HP:{enemy_open(enemies)['hp']}/{enemy_open(enemies)['hp_maximum']}"
                      f"{5 * ' '}LVL:{enemy_open(enemies)['level']}")
                print("")
                print(100 * "-")
                print(f"      [1] Ataque{15 * ' '}[2] Especial{15 * ' '}[3] Itens{15 * ' '}[4] ULTIMATE")
                print(100 * "-")
            except:
                pass

        template_menu()

        opcao = input("Qual sua ação: ")

        while opcao not in ('1', '2', '3', '4'):
            print('\n' * 50)
            template_menu()
            opcao = input("Qual sua ação: ")

        return int(opcao)

    def initiative(party, enemy_party, ):
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

            (camp_battle_speed[i], camp_battle_speed[major_index]) = (
                camp_battle_speed[major_index], camp_battle_speed[i])
            (camp_battle[i], camp_battle[major_index]) = (camp_battle[major_index], camp_battle[i])

        return camp_battle

    def create_character(new_character):
        game_state["main_party"]["characters"][new_character] = {
            "state": {
                "hp": 10,
                "hp_maximum": 10,
                "minimum_damage": 2,
                "maximum_damage": 7,
                "ki": 8,
                "speed": 10,
                "ki_maximum": 8,
                "level": 1
            },
            "actions": {
                "hit": hit_enemy
            }
        }

    def character_open(character):
        return game_state["main_party"]["characters"][character]['state']

    def enemy_open(enemy):
        return game_state["enemy_party"]["enemies"][enemy]['state']

    def create_enemy(new_enemy):
        hp = randint(4, 8)
        game_state["enemy_party"]["enemies"][new_enemy] = {
            "state": {
                "hp": hp,
                "hp_maximum": hp,
                "ki": 2,
                "ki_maximum": 2,
                "speed": 20,
                "minimum_damage": 10,
                "maximum_damage": 10,
                "level": 1
            },
            "actions": {
                "hit": hit_character
            }
        }

    def character_printer():
        if len(game_state["characters"].keys()) <= 0:
            print("[test_printer] -> Nao existem personagens")
            return

        for character_key in game_state["characters"]:
            print(character_key, "\n")

    def enemy_printer():
        if len(game_state["enemies"].keys()) <= 0:
            print("[test_printer] -> Nao existem inimigos")
            return

        for enemy_key in game_state["enemies"]:
            print(enemy_key, "\n")

    def delete_character(character):
        del game_state["main_party"]["characters"][character]

    def delete_enemy(enemy):
        del game_state["enemy_party"]["enemies"][enemy]

    def hit_enemy(character, target):
        minimum_damage = game_state["main_party"]["characters"][character]["state"]["minimum_damage"]
        maximum_damage = game_state["main_party"]["characters"][character]["state"]["maximum_damage"]
        true_damage = randint(minimum_damage, maximum_damage)

        game_state["enemy_party"]["enemies"][target]["state"]["hp"] -= true_damage

        print(f"{character} deu {true_damage} de dano, forte.")
        sleep(1)
        print(f'{target} agora tem {game_state["enemy_party"]["enemies"][target]["state"]["hp"]} de vida')
        print("")

    def hit_character(enemie, target):
        minimum_damage = game_state["enemy_party"]["enemies"][enemie]["state"]["minimum_damage"]
        maximum_damage = game_state["enemy_party"]["enemies"][enemie]["state"]["maximum_damage"]
        true_damage = randint(minimum_damage, maximum_damage)

        game_state["main_party"]["characters"][target]["state"]["hp"] -= true_damage

        print(f"{enemie} deu {true_damage} de dano, ouch.")
        sleep(1)
        print(f'{target} agora tem {game_state["main_party"]["characters"][target]["state"]["hp"]} de vida')
        print("")

    def fight(character, enemy):
        # battle_order = initiative(characters, enemies)
        battle_camp = [character, enemy]
        main_party = [character]
        party_enemy = [enemy]

        while len(main_party) > 0 and len(party_enemy) > 0:
            for fighter in range(len(battle_camp)):
                if battle_camp[fighter] in character:
                    opcao = menu(character, enemy)
                    if opcao == 1:
                        hit_enemy(battle_camp[fighter], enemy)
                        if enemy_open(enemy)["hp"] <= 0:
                            party_enemy.remove(enemy)
                            battle_camp.remove(enemy)
                            print(f"{enemy} foi derrotado por {character}!")
                            print(f"{character} recebeu 1 EXP")
                            delete_enemy(enemy)
                        sleep(2)
                        if character not in battle_camp:
                            print(f"{character} Morreu.")
                    if opcao == 2:
                        print("Você não tem especial ainda.")
                        sleep(1)
                    if opcao == 3:
                        print("Você não tem itens.")
                        sleep(1)
                    if opcao == 4:
                        print("Você não tem uma ULTIMATE.")
                        sleep(1)
                if battle_camp[fighter] in enemy:
                    hit_character(battle_camp[fighter], character)
                    if character_open(character)["hp"] <= 0:
                        main_party.remove(character)
                        battle_camp.remove(character)
                        print(f"{character} morreu...")
                        delete_character(character)
                    sleep(2)

        print("A luta acabou!")

    return game(
        create_character,
        create_enemy,
        character_printer,
        enemy_printer,
        fight,
        menu
    )
