from characters.specs_enemies_area1 import enemies
from characters.specs_characters import characters
from util.input import *
from util.printer import *

from collections import namedtuple
from random import *
from time import sleep

game = namedtuple("State", "create_character create_enemy character_printer enemy_printer fight fight_menu target world_menu generate_enemy_party print_fight_menu")


def create_game():
    game_state = {
        "main_party": {
            "characters": {}
        },
        "enemy_party": {
            "enemies": {}
        },
        "progression": {
            "walk_path": 0,
            "boss_area_kill": False

        }
    }

    def world_menu(characters):
        print_world_menu(characters)

        option = leiaint("Selecione uma opção:")

        if option == 1:
            walk()
            game_state["progression"]["walk_path"] += 1
        elif option == 2:
            print("[Party] -> In Development")
        elif option == 3:
            print("[Acampar] -> In Development")
        else:
            print('\033[1;3;31mERROR! Digite uma opção válida.\033[m')
            sleep(0.7)
        world_menu(characters)

    def walk():
        spawn_chance = random()

        if spawn_chance > 0.5:
            print("Voce escuta sons estranhos nos arbustos!")
            sleep(0.3)
            print("Novo inimigo encontrado")
            generate_enemy_party()
            enemy_printer()

            fight(list(game_state["main_party"]["characters"].keys()), list(game_state["enemy_party"]["enemies"].keys()))
        else:
            print("A calmaria continua na jornada dos herois")

    def print_fight_menu(characters, enemies):
        def party_text(name, txt):
            print(f"{name}{txt}")

        def template_menu():
            print(75 * "=-")
            print(f"{'HORA DO COMBATE':^150}")
            print(75 * "=-")

            if len(characters) < len(enemies):
                maior = enemies
                menor = characters

                for i in menor:
                    hp_bar = f"{(30 - len(i)) * ' '}HP:{character_open(i)['hp']}/{character_open(i)['hp_maximum']}"
                    ki_bar = f"{(20 - len(i)) * ' '}KI:{character_open(i)['ki']}/{character_open(i)['ki_maximum']}"
                    level_bar = f"{10 * ' '}LVL:{character_open(i)['level']}"
                    txt_party = hp_bar + ki_bar + level_bar
                    party_text(i, txt_party)

                print(150 * "-")

                for i in maior:
                    print(f"{i}{(30 - len(i)) * ' '}HP:{enemy_open(i)['hp']}/"
                          f"{enemy_open(i)['hp_maximum']}"
                          f"{25 * ' '}LVL:{enemy_open(i)['level']}")

            if len(characters) > len(enemies):
                maior = characters
                menor = enemies
                for i in maior:
                    hp_bar = f"{(30 - len(i)) * ' '}HP:{character_open(i)['hp']}/{character_open(i)['hp_maximum']}"
                    ki_bar = f"{(20 - len(i)) * ' '}KI:{character_open(i)['ki']}/{character_open(i)['ki_maximum']}"
                    level_bar = f"{10 * ' '}LVL:{character_open(i)['level']}"
                    txt_party = hp_bar + ki_bar + level_bar
                    party_text(i, txt_party)

                print(150 * "-")

                for i in menor:
                    print(f"{i}{(30 - len(i)) * ' '}HP:{enemy_open(i)['hp']}/"
                          f"{enemy_open(i)['hp_maximum']}"
                          f"{25 * ' '}LVL:{enemy_open(i)['level']}")

            if len(characters) == len(enemies):
                for i in characters:
                    hp_bar = f"{(30 - len(i)) * ' '}HP:{character_open(i)['hp']}/{character_open(i)['hp_maximum']}"
                    ki_bar = f"{(20 - len(i)) * ' '}KI:{character_open(i)['ki']}/{character_open(i)['ki_maximum']}"
                    level_bar = f"{10 * ' '}LVL:{character_open(i)['level']}"
                    txt_party = hp_bar + ki_bar + level_bar
                    party_text(i, txt_party)

                print(150 * "-")

                for i in enemies:
                    print(f"{i}{(30 - len(i)) * ' '}HP:{enemy_open(i)['hp']}/"
                          f"{enemy_open(i)['hp_maximum']}"
                          f"{25 * ' '}LVL:{enemy_open(i)['level']}")

            print(150 * "-")
            print(f"         [1] Ataque{22 * ' '}[2] Especial{22 * ' '}[3] Itens{22 * ' '}[4] ULTIMATE")
            print(150 * "-")

        template_menu()

    def fight_actions(characters, enemies):
        print_fight_menu(characters, enemies)

        option = leiaint("Selecione uma opção: ")

        while option not in(1, 2, 3, 4):
            print('\033[1;3;31mERROR! Digite uma opção válida.\033[m')
            option = leiaint("Selecione uma opção: ")

        return option

    def target(enemies):
        for i in range(len(enemies)):
            print(
                f"{i + 1} - {enemies[i]}{(30 - len(enemies[i])) * ' '}HP:{enemy_open(enemies[i])['hp']}"
                f"/{enemy_open(enemies[i])['hp_maximum']}"
                f"{5 * ' '}LVL:{enemy_open(enemies[i])['level']}")

        opcao = leiaint("Selecione o Alvo: ")

        while opcao - 1 >= len(enemies) or opcao < 0:
            print('\n' * 50)

            print('\033[1;3;31mERROR! Digite um numero inteiro válido.\033[m')
            for i in range(len(enemies)):
                print(
                    f"{i + 1} - {enemies[i]}{(30 - len(enemies[i])) * ' '}HP:{enemy_open(enemies[i])['hp']}"
                    f"/{enemy_open(enemies[i])['hp_maximum']}"
                    f"{5 * ' '}LVL:{enemy_open(enemies[i])['level']}")

            opcao = leiaint("Selecione o Alvo: ")

        return enemies[opcao - 1]

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

    def generate_enemy_party():
        possible_enemies = list(enemies.keys())

        for i in range(randint(1, 4)):
            create_enemy(possible_enemies[randint(0, len(possible_enemies) - 1)])

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

    def game_over():
        if len(list(game_state["main_party"]["characters"].keys())) == 0:
            sleep(2.5)
            print('\n' * 100)
            print_game_over()
            quit()
        else:
            pass

    def delete_character(character):
        for searched_character in game_state["main_party"]["characters"]:
            if searched_character == character:
                del game_state["main_party"]["characters"][character]
                break

    def delete_enemy(enemy):
        for searched_enemy in game_state["enemy_party"]["enemies"]:
            if searched_enemy == enemy:
                del game_state["enemy_party"]["enemies"][enemy]
                break

    def hit_enemy(character, target):
        minimum_damage = game_state["main_party"]["characters"][character]["state"]["minimum_atk"]
        maximum_damage = game_state["main_party"]["characters"][character]["state"]["maximum_atk"]
        true_damage = randint(minimum_damage, maximum_damage)

        game_state["enemy_party"]["enemies"][target]["state"]["hp"] -= true_damage

        print(50 * '=')
        print(f"{character} deu {true_damage} de dano, forte.")
        sleep(2)
        print(f'{target} agora tem {game_state["enemy_party"]["enemies"][target]["state"]["hp"]} de vida')
        print("")
        print(50 * '=')

    def hit_character(enemie, target):
        minimum_damage = enemy_open(enemie)["minimum_atk"]
        maximum_damage = enemy_open(enemie)["maximum_atk"]
        true_damage = randint(minimum_damage, maximum_damage)

        game_state["main_party"]["characters"][target]["state"]["hp"] -= true_damage

        print(50 * '=')
        print(f"{enemie} deu {true_damage} de dano, ouch.")
        sleep(2)
        print(f'{target} agora tem {character_open(target)["hp"]} de vida')
        print(" ")
        print(50 * '=')

    def melee_rule_atk(characters):
        hit_chance = random()

        if hit_chance > 0.5:
            return characters[0]
        if hit_chance <= 0.5:
            if len(characters) > 1:
                return characters[1]
            else:
                return characters[0]

    def ranged_rule_atk(characters):
        hit_chance = random()

        if hit_chance < 0.25:
            return characters[0]
        if 0.25 < hit_chance < 0.50:
            if len(characters) > 1:
                return characters[1]
            else:
                return characters[0]
        if 0.50 < hit_chance < 0.75:
            if len(characters) > 2:
                return characters[2]
            else:
                return characters[randint(0, 1)]
        if 0.75 < hit_chance < 1:
            if len(characters) > 3:
                return characters[3]
            else:
                return characters[randint(0, 2)]

    def fight(characters, enemies):
        battle_order = initiative(characters, enemies)

        while len(game_state["main_party"]["characters"].keys()) > 0 and len(game_state["enemy_party"]["enemies"].keys()) > 0:
            for fighter in battle_order:
                if fighter in game_state["main_party"]["characters"]:
                    opcao = fight_actions(characters, enemies)

                    if opcao == 1:
                        enemy_target = target(list(game_state["enemy_party"]["enemies"].keys()))
                        hit_enemy(fighter, enemy_target)

                        if enemy_open(enemy_target)["hp"] <= 0:
                            print(f'inimigo {enemy_target} derrotado.')

                            delete_enemy(enemy_target)
                            battle_order.remove(enemy_target)
                            enemies.remove(enemy_target)
                    else:
                        print("Indisponível")
                else:
                    if game_state["enemy_party"]["enemies"][fighter]["state"]["melee"]:
                        character_target = melee_rule_atk(characters)
                    else:
                        character_target = ranged_rule_atk(characters)

                    hit_character(fighter, character_target)

                    if character_open(character_target)["hp"] <= 0:
                        print(f'\033[1;3;31mPersonagem {character_target} foi derrotado.\033[m')
                        sleep(1.5)
                        print(" ")

                        delete_character(character_target)
                        battle_order.remove(character_target)
                        characters.remove(character_target)
                        game_over()

    return game(
        create_character,
        create_enemy,
        character_printer,
        enemy_printer,
        fight,
        fight_actions,
        target,
        world_menu,
        generate_enemy_party,
        print_fight_menu

    )
