from game_rules.game import create_game


def main():
    game = create_game()

    game.create_character("Nikolal Legal")
    #game.create_character("João Feijão")

    game.create_enemy("Slime")
    game.create_enemy("Mimico")

    main_party = ["Nikolal Legal"]
    party_enemy = ["Slime", "Mimico"]
    game.fight(main_party, party_enemy)


if __name__ == '__main__':
    main()
