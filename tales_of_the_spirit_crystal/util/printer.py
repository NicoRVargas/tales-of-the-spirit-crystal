def print_world_menu(characters):
    print("\n" * 50)

    print(75 * "=-")
    print(f"{'Mundo 1':^150}")
    print(75 * "=-")

    for i in range(len(characters)):
        print(f"[{i}]\t",characters[i])

    print(150 * "-")
    print(f"[1] Andar{22 * ' '}[2] Party{22 * ' '}[3]Acampar")
    print(150 * "-")

def print_fight_menu(characters, enemies):
    print("\n" * 50)

    matrix = [characters, enemies]

    character_is_greater = False
    smaller_column = 0 if len(matrix[0]) <= len(matrix[1]) else 1

    if smaller_column == 1:
        character_is_greater = True

    for i in range(len(matrix[smaller_column])):
        print(matrix[0][i], end="")
        print(f"{'':<30}{matrix[1][i]}")

    if character_is_greater:
        for i in range(len(matrix[smaller_column]), len(matrix[0])):
            print(matrix[0][i])
    else:
        for i in range(len(matrix[smaller_column]), len(matrix[1])):
            print(f"{'':<30}{matrix[1][i]}")

    print(150 * "-")
    print(f"         [1] Ataque{22 * ' '}[2] Especial{22 * ' '}[3] Itens{22 * ' '}[4] ULTIMATE")
    print(150 * "-")
