from game_rules.game import create_game


def main():
    game = create_game()

    game.create_character("Nikolal Legal")
    game.create_character("João Feijão")
    game.create_character("Pedro Pedra")
    game.create_character("Kawan Cabeludo")
    #game.create_enemy("Slime")
    #game.create_enemy("Mimico")

    main_party = ["Nikolal Legal", "João Feijão", "Pedro Pedra", "Kawan Cabeludo"]
    #party_enemy = ["Slime", "Mimico"]
    game.world_menu(main_party)


if __name__ == '__main__':
    main()
