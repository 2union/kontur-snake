from game.teams import Teams


teams = Teams()

results = teams.get_top_accounts()

for result in results:
    print(f'[{result[0]}] {result[1]} ({result[2]})')
