from game.teams import Teams


def leader_board():
    teams = Teams()
    results = teams.get_top_accounts()
    ordered_list = []
    command = None
    i = 1
    j = 1
    for result in results:
        if command != result[1]:
            command = result[1]
            ordered_list.append(("", i, result[1], [result[0]]))
            j = i
            i += 1
        ordered_list.append((j, i, result[2], [""]))
        i += 1
        print(f'[{result[0]}] {result[1]} ({result[2]})')
    if not len(ordered_list):
        ordered_list.append(("", 1, "Результатов ещё нет", [""]))
    return ordered_list


def turncate_tables():
    Teams().turncate_tables()


if __name__ == "__main__":
    leader_board()
