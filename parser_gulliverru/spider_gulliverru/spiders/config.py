import sys

project_root_dir = sys.path[5].replace('\\venv', '')

input_data = f'{project_root_dir}\\inputdata.csv'

# Important var, using in naming of "parcer_" and "spider_" dirs
# In settings and main Spider class name var
parcer_name = 'gulliverru'

# Adding project dirs to sys.paths
def add_paths():
    sys.path.append(project_root_dir)
    sys.path.append(sys.path[0].replace('\\spiders', ''))
    sys.path.append(sys.path[5].replace('\\venv', '\\reuse'))
    sys.path.append(sys.path[5].replace('\\venv', f'\\parser_{parcer_name}'))
    sys.path.append(sys.path[5].replace('\\venv', f'\\parser_{parcer_name}\\spider_{parcer_name}'))