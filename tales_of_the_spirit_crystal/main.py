from game_rules.game import create_game


def main():
    game = create_game()

    game.create_enemy("Kawan Cabeludo")

    game.create_character("Nikolal Legal")

    game.menu("Nikolal Legal", "Kawan Cabeludo")


if __name__ == '__main__':
    main()
