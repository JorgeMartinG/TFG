from pathlib import Path

PATH = Path(__file__).parent

with open(f'{PATH}\\user_data.sql', 'r', encoding="utf8") as f:
    lines = f.readlines()

lines = [line.replace('\n', ' ').replace('\t', '').strip() for line in lines]

with open(f'{PATH}\\data.sql', 'w', encoding="utf8") as f:

    for line in lines:
        f.writelines(line)

