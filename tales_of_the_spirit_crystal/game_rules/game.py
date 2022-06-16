from characters.specs_enemies_area1 import enemies
from characters.specs_characters import characters
from util.input import *
from util.printer import *

from collections import namedtuple
from random import *
from time import sleep

game = namedtuple("State", "create_character create_enemy character_printer enemy_printer fight fight_menu target world_menu")


def create_game():
    game_state = {
        "main_party": {
            "characters": {}
        },
        "enemy_party": {
            "enemies": {}
        }
    }

    def world_menu(characters):
        print_world_menu(characters)

        option = leiaint("Selecione uma opção:")

        if option == 1:
            walk()
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
        else:
            print("A calmaria continua na jornada dos herois")

    def fight_menu(characters, enemies):
        print_fight_menu(characters, enemies)

        option = leiaint("Selecione uma opção:")

        if option == 1:
            # Precisa chamar a função target
            print("[Ataque] -> In Development")
        elif option == 2:
            print("[Especial] -> In Development")
        elif option == 3:
            print("[Itens] -> In Development")
        elif option == 4:
            print("[Ultimate] -> In Development")
        else:
            print('\033[1;3;31mERROR! Digite uma opção válida.\033[m')
            sleep(0.7)

            fight_menu(characters, enemies)

    def target(enemies):
        for i in range(len(enemies)):
            print(
                f"{i + 1} - {enemies[i]}{(30 - len(enemies[i])) * ' '}HP:{enemy_open(enemies[i])['hp']}/{enemy_open(enemies[i])['hp_maximum']}"
                f"{5 * ' '}LVL:{enemy_open(enemies[i])['level']}")

        opcao = leiaint("Selecione o Alvo: ")

        while opcao >= len(enemies) or opcao < 0:
            print('\n' * 50)

            print('\033[1;3;31mERROR! Digite um numero inteiro válido.\033[m')
            for i in range(len(enemies)):
                print(
                    f"{i + 1} - {enemies[i]}{(30 - len(enemies[i])) * ' '}HP:{enemy_open(enemies[i])['hp']}/{enemy_open(enemies[i])['hp_maximum']}"
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

    def generate_enemy_party():
        possible_enemies = list(enemies.keys())

        for i in range(randint(1,4)):
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
                    opcao = fight_menu(characters, enemies)
                    if opcao == 1:
                        index = target(enemies)
                        hit_enemy(fighter, enemies[index - 1])
                        if enemy_open(enemies[index - 1])["hp"] <= 0:
                            print(f"inimigo {enemies[index - 1]} derrotado.")
                            enemies.remove(enemies[index - 1])
                    else:
                        print("Indisponível")
                if fighter in enemies:
                    fight_menu(characters, enemies)
                    hit_character(fighter, characters[0])
                    characters.remove(characters[0])

    return game(
        create_character,
        create_enemy,
        character_printer,
        enemy_printer,
        fight,
        fight_menu,
        target,
        world_menu
    )
