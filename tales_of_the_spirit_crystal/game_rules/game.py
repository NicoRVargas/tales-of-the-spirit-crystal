from collections import namedtuple
from random import randint

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

    def menu(character, enemy):
        def template_menu():
            print(50 * "-=")
            print(f"{character:>43}{4 * ' '}"
                  f"HP:{character_open(character)['hp']}/{character_open(character)['hp_maximum']}"
                  f"{4 * ' '}KI:{character_open(character)['ki']}/{character_open(character)['ki_maximum']}{4 * ' '}"
                  f"LVL:{character_open(character)['level']}")
            print(50 * "-=")
            # print(f"{character}{3 * ' '}HP:{character['hp']}{3 * ' '}KI:{character['ki']}{3 * ' '}LVL:{character['level']}{5 * ' '}", end='||')
            print(f"{5 * ' '}{enemy}{5 * ' '}HP:{enemy_open(enemy)['hp']}/{enemy_open(enemy)['hp_maximum']}"
                  f"{5 * ' '}LVL:{enemy_open(enemy)['level']}")
            print("")
            print(100 * "-")
            print(f"      [1] Ataque{15 * ' '}[2] Especial{15 * ' '}[3] Itens{15 * ' '}[4] ULTIMATE")
            print(100 * "-")

        template_menu()
        opcao = input("Qual sua ação: ")

        while opcao not in ('1', '2', '3', '4'):
            print('\n' * 50)
            template_menu()
            opcao = input("Qual sua ação: ")

        return int(opcao)

    def create_character(new_character):
        game_state["main_party"]["characters"][new_character] = {
            "state": {
                "hp": 10,
                "hp_maximum": 10,
                "minimum_damage": 2,
                "maximum_damage": 7,
                "ki": 8,
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
                "minimum_damage": 4,
                "maximum_damage": 7,
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
        del game_state["characters"][character]

    def delete_enemy(enemy):
        del game_state["enemies"][enemy]

    def hit_enemy(character, target):
        minimum_damage = game_state["characters"][character]["state"]["minimum_damage"]
        maximum_damage = game_state["characters"][character]["state"]["maximum_damage"]
        true_damage = randint(minimum_damage, maximum_damage)

        game_state["enemies"][target]["state"]["hp"] -= true_damage

        print(f"{character} deu {true_damage} de dano, forte.")
        print(f'{target} agora tem {game_state["enemies"][target]["state"]["hp"]} de vida')
        print("")

    def hit_character(enemie, target):
        minimum_damage = game_state["enemies"][enemie]["state"]["minimum_damage"]
        maximum_damage = game_state["enemies"][enemie]["state"]["maximum_damage"]
        true_damage = randint(minimum_damage, maximum_damage)

        game_state["characters"][target]["state"]["hp"] -= true_damage

        print(f"{enemie} deu {true_damage} de dano, ouch.")
        print(f'{target} agora tem {game_state["characters"][target]["state"]["hp"]} de vida')
        print("")

    def fight(character, enemie):
        camp_battle = character, enemie

    return game(
        create_character,
        create_enemy,
        character_printer,
        enemy_printer,
        fight,
        menu
    )
