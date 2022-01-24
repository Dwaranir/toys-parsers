import os
import sys
import subprocess

m_menu = {}
tasks = {}

user_choise = 'user_choise'

# Scanning for all spider projects in root dir
# Adding their names to the main menu
# And appending their paths to the sys.path
def tasks_generator():
    dirs = os.scandir()
    menu_number = 1
    for entry in dirs:
        if entry.is_dir() and 'parser_' in entry.name:
            name = entry.name.replace('parser_', '')
            spiders_dir = os.scandir(path=f'{entry.name}/spider_{name}/spiders/')
            for file in spiders_dir:
                if file.is_file() and file.name == f'{name}.py':
                    parcer_name = file.name.replace('.py','')
                    m_menu[menu_number] = f'Run {parcer_name.upper()} Spider'
                    tasks[menu_number] = parcer_name
                    
                    sys.path.append(sys.path[5].replace('\\venv', f'\\parser_{parcer_name}\\spider_{parcer_name}\\spiders'))
                    menu_number += 1
    m_menu[0] = 'Exit'

tasks_generator()


# Run spider depending on user choise in main menu
while user_choise not in m_menu:
    print('Type a number of required task: \n')
    print(*[str(k) + ' : ' + str(v) for k,v in m_menu.items()], sep='\n')
    user_choise = int(input('\n'))

if user_choise != 0:
    subprocess.call(f'parser_gulliverru\\spider_gulliverru\\spiders\\{tasks[user_choise]}', shell=True)
else:
    sys.exit(0)



# while user_choise != int 