from game_rules.game import create_game


def main():
    game = create_game()

    game.create_enemy("Kawan Cabeludo")

    game.create_character("Nikolal Legal")

    game.create_enemy("Slime")

    game.create_character("Pedro Pedra")

    game.menu(["Nikolal Legal", "Pedro Pedra"], ["Slime", "Kawan Cabeludo"])


if __name__ == '__main__':
    main()
