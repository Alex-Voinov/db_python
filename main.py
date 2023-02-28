from os.path import abspath, exists, split as filesplit, join
from time import time, ctime

ABSOLUTEPATH: str = abspath(__file__)
PATH_DB: str = r'c:\proect_set\database\python_scripts\DATABASE.txt'
PATH_LOGS: str = r'c:\proect_set\database\python_scripts\LOGS.txt'
DERFILE, NAMEFILE = filesplit(ABSOLUTEPATH)
NAMEDB: str = 'DATABASE.txt'
NAMELOGS: str = 'LOGS.txt'
POSITIVE: bool = True
NEGATIVE: bool = False
POSITIVE_LIST: tuple = ('да', 'ага', '+', 'yes', 'yep', 'ya', 'ofcourse', )
NEGATIVE_LIST: tuple = ('нет', 'не', '-', 'no', 'nope', 'nah', 'иди нафиг', )
EXIT: int = NEGATIVE
UNKNOW: int = -1
DATA_BASE: dict = {
    'path': PATH_DB,
    'name': 'Database',
    'global_name': NAMEDB,
    'global_var_path': 'PATH_DB',
}

LOGS_FILE: dict = {
    'path': PATH_LOGS,
    'name': 'Logs file',
    'global_name': NAMELOGS,
    'global_var_path': 'PATH_LOGS',
}

FEILDS_DESCRIPTION: dict = {
    'ID': 'unice auntithicator',
    'ID_RECORD': 'Уникальный номер записи', 
    'TIME_CREATIVE': 'time of crating reminder', 
    'DATATIME': 'reminding time', 
    'DESCRIPTION': 'description', 
    'DURATION': 'duration', 
    'CLIENT': 'name of client', 
    'NOTIFICATION': 'how important it is', 
    'TEXT_NOTIFICATION': 'text of notification'
}
FIELDS_LOGS: tuple = (
    'ID',
    'LOGIN',
    'PASSWORD',
)
SEPARATION: str = '\t' * 3

user_id: int = UNKNOW

def input_int(request: str, min = '', max = '') -> int:
    data: str = ''
    if min and max:
        request += f'(Number should be in the rande from {min} and {max})'
    else:
        if min == -1:
            request += f'(Number should be positive):'
        elif min:
            request += f'(Number should be bigger {min}):'
        elif max == 1:
            request += f'(Number should be negative):'
        elif max:
            request += f'(Number should be smaler {max}):'
    while not ((
        data.isdigit() or
        (not min or int(data) > int(min)) or
        (not max or int(data) < int(max))
    )):
        print(request)
        data = input()
    return int(data)


def answer(
    request: str, 
    natification: str='', 
    positive_list = POSITIVE_LIST, 
    negative_list = NEGATIVE_LIST
) -> bool:
    '''Function for geting answers from users.'''
    user_answer: str = ''
    if natification:
        print(natification)
    while user_answer not in positive_list + negative_list:
        print(request)
        user_answer = input()
        if user_answer in positive_list:
            return POSITIVE
        elif user_answer in negative_list:
            return NEGATIVE
        else:
            print("I don't understand you :(")
            print('I only understand thees answers:')
            print(*(positive_list+negative_list), sep='\n')


def reg_path(element: dict) -> bool:
    '''Registrade a path do the element file.'''
    data: list = []
    if not exists(element['path']):
        if answer(
            f"Do you want to create a {element['name']} file in the same plase with program?", 
            natification=f'If you say yes file will be loade in this directory:\n{DERFILE}'
            ):
            globals()[element['global_var_path']] = join(DERFILE, element['global_name'])
        else:
            user_direcory: str = input("Enter derictory's full path")
            globals()[element['global_var_path']] = join(user_direcory, element['global_name'])
            try:
                open(join(user_direcory, element['global_name']), 'wt', encoding='utf').close()
            except:
                print('Не удалось создать файл в нужной директории')
                return NEGATIVE
        path: str = globals()[element['global_var_path']]
        with open(ABSOLUTEPATH, 'rt', encoding='utf') as main_file:
            data = main_file.readlines()
        for index, row in enumerate(data):
            if f'{element["global_var_path"]}: str = r' in row:
                data[index] = f"{element['global_var_path']}: str = r'{path}'\n"
                break
        with open(ABSOLUTEPATH, 'wt', encoding='utf') as main_file:
            print(*data, sep='', end='', file=main_file)
    return POSITIVE


def row_write(data: tuple) -> str:
    '''Converts tuples in to text for database'''
    return SEPARATION.join(map(str, data))


def row_read(data: str) -> tuple:
    '''Converts from database text to tuples'''
    return tuple(data.split(SEPARATION))


def create_user(id: int) -> tuple:
    '''Create a new user.'''
    user_id: int = id
    user_login: str = input("{введите свой <LOGIN>: ")
    user_password: str = input('введите свой <PASSWORD>: ')
    return user_id, user_login, user_password


def create_records(id: int) -> str:
    index_first_field_man: int = tuple(FEILDS_DESCRIPTION.keys()).index('DATATIME')
    time_now = ctime(time())
    record_id: int = id
    record: list = [user_id, record_id, time_now, ]
    for field in tuple(FEILDS_DESCRIPTION.keys()) [index_first_field_man:]:
        record.append(input(f'Введите <{FEILDS_DESCRIPTION[field]}>: '))
    return row_write(record)


def feel(element: dict) -> None: #Сделать возможным принудительную регистрацию пользователя
    '''Felling select element.'''
    data: list
    if element == LOGS_FILE:
        global user_id
        data = [row_write(FIELDS_LOGS), ]
        if answer(
            'Логс файлы успешно созданы, желаете ли вы создать первого пользователя?'
        ):
            new_user: tuple = create_user(user_id:=0)
            data.append(row_write(new_user))
        with open(PATH_LOGS, 'wt', encoding='utf-8') as logs_file:
            print(*data, sep='\n', end='', file=logs_file)   
    elif element == DATA_BASE:
        data = [row_write(tuple(FEILDS_DESCRIPTION.keys())), ]
        if not user_id == UNKNOW and answer(
                'База данных успешно создана, хотите ли вы заполнить её записями?'
            ):
            records_amount: int = int(input('Введите колличество новых записей:'))#
            for i in range(records_amount):
                print(f'Создаём запись №{i + 1}:')
                data.append(create_records(i))
        with open(PATH_DB, 'wt', encoding='utf-8') as data_base_file:
            print(*data, sep='\n', end='', file=data_base_file)


def create(element: dict) -> bool:
    '''Creates a data base if it is not found.'''
    if answer(
        f'Do you wanna create {element["name"]}?',
        natification=f"App won't work with out {element['name']}"
    ) and reg_path(element):
        feel(element)
        print(f'{element["name"]} is created sucssesfuly')
        return POSITIVE
    return NEGATIVE


def check(element: dict) -> bool:
    '''Checks elements.'''
    result_find =  exists(element['path'])
    print(f"{element['name']} is {('not ', '')[result_find]}found")
    if not result_find:
        result_create: bool = create(element)
        return result_create
    return result_find


def main() -> None:
    '''Main function'''
    if all((check(LOGS_FILE), check(DATA_BASE))):
        print('All fiells is loaded sucsessful')
        ...
    else:
        print('Program have succsesfuly ended')


if __name__ == '__main__':
    '''Checks that the program is launched but nod used like a module.'''
    main()