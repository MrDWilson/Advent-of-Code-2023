from pathlib import Path
from functools import reduce

def main():
    p = Path(__file__).with_name('game.txt')
    with p.open('r') as file:
        lines = file.readlines()
        results = {}

        for line in lines:
            game_info = line.split(":")
            game_id = game_info[0].split(" ")[1]

            games = game_info[1].split(";")
            all_games = []
            for game in games:
                this_game = {}
                cubes = game.split(",")
                for cube in cubes:
                    value = cube.strip().split(" ")
                    this_game[value[1]] = value[0]
                all_games.append(this_game)
            
            results[game_id] = all_games

        max_values = { "red": 12, "green": 13, "blue" : 14 }

        possible_games = []
        for id, rounds in results.items():
            impossible = False
            for round in rounds:
                for colour, max in max_values.items():
                    if colour in round:
                        count = round[colour]
                        if int(count) > int(max):
                            impossible = True
                            break
                
                if impossible:
                    break
            
            if not impossible:
                possible_games.append(int(id))

        print("Part one: " + str(sum(possible_games)))

        cubes = []
        for id, rounds in results.items():
            max_values = {}
            for round in rounds:
                for colour, value in round.items():
                    if colour not in max_values:
                        max_values[colour] = value
                    else:
                        current_value = max_values[colour]
                        if int(value) > int(current_value):
                            max_values[colour] = value

            max_items = [x[1] for x in max_values.items()]
            cubes.append(reduce(lambda x, y: int(x) * int(y), max_items))

        print("Part two: " + str(sum(cubes)))
                
if __name__ == "__main__":
    main()