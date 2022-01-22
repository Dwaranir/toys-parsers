import os
import sys
import subprocess

m_menu = {}
tasks = {}

user_choise = 'user_choise'



def tasks_generator():
    dirs = os.scandir()
    menu_number = 1
    for entry in dirs:
        if entry.is_dir() and 'parser_' in entry.name:
            name = entry.name.replace('parser_', '')
            spiders_dir = os.scandir(path=f'{entry.name}/spider_{name}/spiders/')
            for file in spiders_dir:
                if file.is_file() and file.name == f'{name}.py':
                    m_menu[menu_number] = f'Run {file.name} Spider'
                    tasks[menu_number] = file.name
                    menu_number += 1
    m_menu[0] = 'Exit'

tasks_generator()



while user_choise not in m_menu:
    print('Type a number of required task: \n')
    print(*[str(k) + ' : ' + str(v) for k,v in m_menu.items()], sep='\n')
    user_choise = int(input('\n'))

if user_choise != 0:
    parcer_name = tasks[user_choise].replace('.py','')
    sys.path.append(sys.path[5].replace('\\venv', f'\\parser_{parcer_name}\\spider_{parcer_name}\\spiders'))

    subprocess.call(f'parser_gulliverru\\spider_gulliverru\\spiders\\{tasks[user_choise]}', shell=True)
else:
    sys.exit(0)



# while user_choise != int 