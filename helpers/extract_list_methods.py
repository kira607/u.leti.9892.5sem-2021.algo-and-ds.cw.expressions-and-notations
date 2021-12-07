import re
from latex_helper import TableCreator


def main():
    with open('../list/list.py', 'r') as file:
        content = file.read()

    funcs = re.findall(r'def [\s\S]*? -> [\S]*?:', content)
    data = [['Метод', 'Оценка сложности']]
    for func in funcs:
        print(func)
        data.append([f'\\verb|{func[len("def "):]}|', '\\textit{O($  $)}'])
    creator = TableCreator(data)
    print(creator.get_table())


if __name__ == '__main__':
    main()
