from game_rules.game import create_game


def main():
    game = create_game()

    game.create_character("Nikolal Legal")

    game.create_character("João Feijão")

    game.create_enemy("Slime")
    game.create_enemy("Esqueleto Guerreiro")
    game.create_enemy("Esqueleto Healer")
    game.create_enemy("Pedrinha Viva")

    game.create_character("Pedro Pedra")
    game.create_character("Kawan Cabeludo")

    main_party = ["Nikolal Legal", "João Feijão", "Pedro Pedra", "Kawan Cabeludo"]
    party_enemy = ["Slime", "Esqueleto Guerreiro", "Esqueleto Healer", "Pedrinha Viva"]

    game.fight(main_party, party_enemy)


if __name__ == '__main__':
    main()
