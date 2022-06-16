from collections import namedtuple
from random import randint
from time import sleep
from util.input import *
from characters.specs_enemies_area1 import enemies
from characters.specs_characters import characters

game = namedtuple("State", "create_character create_enemy character_printer enemy_printer fight menu target")


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

        def party_text(name, txt):
            print(f"{name}{txt}", end=' ')

        def template_menu():
            hp_bar = f"{4 * ' '}HP:{character_open(characters[0])['hp']}/{character_open(characters[0])['hp_maximum']}{4 * ' '}"
            ki_bar = f"KI:{character_open(characters[0])['ki']}/{character_open(characters[0])['ki_maximum']}{4 * ' '}"
            level_bar = f"LVL:{character_open(characters[0])['level']}"
            txt_cabecalho = characters[0] + hp_bar + ki_bar + level_bar
            cabecalho(txt_cabecalho)

            maior = []
            menor = []

            if len(characters) > len(enemies):
                maior = characters
                menor = enemies
            if len(characters) == len(enemies):
                igual = len(characters)
            if len(characters) < len(enemies):
                maior = enemies
                menor = characters

            c = 0

            for i in range(1, len(menor)):
                hp_bar = f"{(30 - len(menor[i])) * ' '}HP:{character_open(characters[i])['hp']}/{character_open(characters[i])['hp_maximum']}    "
                ki_bar = f"KI:{character_open(characters[i])['ki']}/{character_open(characters[i])['ki_maximum']}    "
                level_bar = f"LVL:{character_open(characters[i])['level']}"
                txt_party = hp_bar + ki_bar + level_bar
                party_text(characters[i], txt_party)

                print(
                    f"{'':>30}{enemies[c]}{(30 - len(maior[c])) * ' '}HP:{enemy_open(enemies[c])['hp']}/{enemy_open(enemies[c])['hp_maximum']}"
                    f"{5 * ' '}LVL:{enemy_open(enemies[c])['level']}")

                c += 1

            if len(characters) > len(enemies):
                for i in range(len(menor), len(maior)):
                    hp_bar = f"{(30 - len(menor[i]))}HP:{character_open(characters[i])['hp']}/{character_open(characters[i])['hp_maximum']}{4 * ' '}"
                    ki_bar = f"KI:{character_open(characters[i])['ki']}/{character_open(characters[i])['ki_maximum']}{4 * ' '}"
                    level_bar = f"LVL:{character_open(characters[i])['level']}"
                    txt_party = hp_bar + ki_bar + level_bar
                    party_text(characters[i], txt_party)

            if len(characters) < len(enemies):
                for i in range(len(menor), len(maior)):
                    print(
                        f"{'':>88}{enemies[i]}{(30 - len(maior[i])) * ' '}HP:{enemy_open(enemies[i])['hp']}/{enemy_open(enemies[i])['hp_maximum']}"
                        f"{5 * ' '}LVL:{enemy_open(enemies[i])['level']}")

            if len(characters) == len(enemies):
                for i in range(len(menor), len(maior)):
                    print(
                        f"{'':>88}{enemies[i]}{(30 - len(maior[i])) * ' '}HP:{enemy_open(enemies[i])['hp']}/{enemy_open(enemies[i])['hp_maximum']}"
                        f"{5 * ' '}LVL:{enemy_open(enemies[i])['level']}")

            print(150 * "-")
            print(f"         [1] Ataque{22 * ' '}[2] Especial{22 * ' '}[3] Itens{22 * ' '}[4] ULTIMATE")
            print(150 * "-")

        template_menu()

        opcao = input("Qual sua ação: ")

        while opcao not in ('1', '2', '3', '4'):
            print('\n' * 50)
            template_menu()
            opcao = input("Qual sua ação: ")

        return int(opcao)

    def target(enemies):
        for i in range(len(enemies)):
            print(
                f"{i+1} - {enemies[i]}{(30 - len(enemies[i])) * ' '}HP:{enemy_open(enemies[i])['hp']}/{enemy_open(enemies[i])['hp_maximum']}"
                f"{5 * ' '}LVL:{enemy_open(enemies[i])['level']}")

        opcao = leiaint("Selecione o Alvo: ")

        while opcao >= len(enemies) or opcao < 0:
            print('\n' * 50)

            for i in range(len(enemies)):
                print(
                    f"{i+1} - {enemies[i]}{(30 - len(enemies[i])) * ' '}HP:{enemy_open(enemies[i])['hp']}/{enemy_open(enemies[i])['hp_maximum']}"
                    f"{5 * ' '}LVL:{enemy_open(enemies[i])['level']}")

            opcao = leiaint("Selecione o Alvo: ")

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
        for character in characters.keys():
            if character == new_character:
                game_state["main_party"]["characters"][new_character] = characters[new_character]
                break

    def character_open(character):
        return game_state["main_party"]["characters"][character]['state']

    def enemy_open(enemy):
        return game_state["enemy_party"]["enemies"][enemy]['state']

    def create_enemy(new_enemy):
        for enemy in enemies.keys():
            if enemy == new_enemy:
                game_state["enemy_party"]["enemies"][new_enemy] = enemies[new_enemy]
                break

    def character_printer():
        if len(game_state["main_party"]["characters"].keys()) <= 0:
            print("[test_printer] -> Nao existem personagens")
            return

        for character_key in game_state["main_party"]["characters"]:
            print(character_key, "\n")

    def enemy_printer():
        if len(game_state["enemy_party"]["enemies"].keys()) <= 0:
            print("[test_printer] -> Nao existem inimigos")
            return

        for enemy_key in game_state["enemy_party"]["enemies"]:
            print(enemy_key, "\n")

    def delete_character(character):
        del game_state["main_party"]["characters"][character]

    def delete_enemy(enemy):
        del game_state["enemy_party"]["enemies"][enemy]

    def hit_enemy(character, target):
        minimum_damage = game_state["main_party"]["characters"][character]["state"]["minimum_atk"]
        maximum_damage = game_state["main_party"]["characters"][character]["state"]["maximum_atk"]
        true_damage = randint(minimum_damage, maximum_damage)

        game_state["enemy_party"]["enemies"][target]["state"]["hp"] -= true_damage

        print(f"{character} deu {true_damage} de dano, forte.")
        sleep(1)
        print(f'{target} agora tem {game_state["enemy_party"]["enemies"][target]["state"]["hp"]} de vida')
        print("")

    def hit_character(enemie, target):
        minimum_damage = game_state["enemy_party"]["enemies"][enemie]["state"]["minimum_atk"]
        maximum_damage = game_state["enemy_party"]["enemies"][enemie]["state"]["maximum_atk"]
        true_damage = randint(minimum_damage, maximum_damage)

        game_state["main_party"]["characters"][target]["state"]["hp"] -= true_damage

        print(f"{enemie} deu {true_damage} de dano, ouch.")
        sleep(1)
        print(f'{target} agora tem {game_state["main_party"]["characters"][target]["state"]["hp"]} de vida')
        print("")

    def fight(characters, enemies):
        battle_order = initiative(characters, enemies)

        while len(characters) > 0 and len(enemies) > 0:
            for fighter in battle_order:
                if fighter in characters:
                    opcao = menu(characters, enemies)
                    if opcao == 1:
                        index = target(enemies)
                        hit_enemy(fighter, enemies[index - 1])
                        if enemy_open(enemies[index - 1])["hp"] <= 0:
                            print(f"inimigo {enemies[index - 1]} derrotado.")
                            enemies.remove(enemies[index - 1])
                    else:
                        print("Indisponível")
                if fighter in enemies:
                    menu(characters, enemies)
                    hit_character(fighter, characters[0])
                    characters.remove(characters[0])


    return game(
        create_character,
        create_enemy,
        character_printer,
        enemy_printer,
        fight,
        menu,
        target
    )
