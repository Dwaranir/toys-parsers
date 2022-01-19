import sys
import subprocess

enable_venv = subprocess.Popen(["powershell.exe", 
              "venv\\scripts\\activate.ps1"], 
              stdout=sys.stdout)
enable_venv.communicate()



m_menu = {
    1: 'Run Gulliver.Ru Spider',
    0: 'Exit'
}

tasks = {
    1: 'gulliverru.py'
}

user_choise = 'user_choise'

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