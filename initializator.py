import os
import shutil
import re
import subprocess

PATH_TO_ENGINE_SRC = '../graph-drawer-engine/src/'

###############     _____                  
###############    / ____|                 
###############   | |     ___  _ __  _   _ 
###############   | |    / _ \| '_ \| | | |
###############   | |___| (_) | |_) | |_| |
###############    \_____\___/| .__/ \__, |
###############               | |     __/ |
###############               |_|    |___/ 

# Copy the contents of assets into the graph-drawer-engine

assets_path = os.path.join(PATH_TO_ENGINE_SRC, 'assets')
dynamic_assets_path = os.path.join(PATH_TO_ENGINE_SRC, 'assets', 'dynamic')
static_assets_path = os.path.join(PATH_TO_ENGINE_SRC, 'assets', 'static')

# Delete previous content

if os.path.isdir(dynamic_assets_path):
    shutil.rmtree(dynamic_assets_path, ignore_errors=False, onerror=None)
if os.path.isdir(static_assets_path):
    shutil.rmtree(static_assets_path, ignore_errors=False, onerror=None)

# Then copy
shutil.copytree('assets/dynamic', dynamic_assets_path) 
shutil.copytree('assets/static', static_assets_path) 

###############    _____            _                
###############   |  __ \          | |               
###############   | |__) |___ _ __ | | __ _  ___ ___ 
###############   |  _  // _ \ '_ \| |/ _` |/ __/ _ \
###############   | | \ \  __/ |_) | | (_| | (_|  __/
###############   |_|  \_\___| .__/|_|\__,_|\___\___|
###############              | |                     
###############              |_|                    

# Replace relative links into copyed files (dynamic content only)

import_pattern = rf"(?P<prefix>import .* from [\"\'][\./]*)({re.escape(PATH_TO_ENGINE_SRC)})(?P<suffix>[a-zA-Z-./]*[\"\'].*)"

for (dirpath, dirnames, filenames) in os.walk(dynamic_assets_path):
    for _file in filenames:
        with open(os.path.join(dirpath, _file), mode='r+', encoding='utf-8') as file_object:
            # print(re.sub(import_pattern, r'\g<prefix>\g<suffix>', file_object.read(), flags = re.MULTILINE))
            new_content = re.sub(import_pattern, r'\g<prefix>\g<suffix>', file_object.read(), flags = re.MULTILINE)
            # Use truncate/seek in conjunction with 'r+' mode to replace
            # from https://www.kite.com/python/answers/how-to-update-and-replace-text-in-a-file-in-python#:~:text=truncate()%20to%20replace%20text,replace%20in%20the%20provided%20string%20.
            file_object.seek(0)
            file_object.write(new_content)
            file_object.truncate()

###############    _____          _                                            
###############   |  __ \        | |                                           
###############   | |__) |__  ___| |_ ______ _ __  _ __ ___   ___ ___  ___ ___ 
###############   |  ___/ _ \/ __| __|______| '_ \| '__/ _ \ / __/ _ \/ __/ __|
###############   | |  | (_) \__ \ |_       | |_) | | | (_) | (_|  __/\__ \__ \
###############   |_|   \___/|___/\__|      | .__/|_|  \___/ \___\___||___/___/
###############                             | |                                
###############                             |_|                               

# Rewrite the .gitignore
# with open(os.path.join(assets_path, '.gitignore'), encoding='utf-8', mode = 'w') as gitignore_file_object:
#     gitignore_file_object.write('*/')

# Execute the setup
current_path = os.getcwd()
homedir = os.path.expanduser("~")
ts_node_path = os.path.join(homedir, 'AppData/Roaming/npm/ts-node.cmd')
os.chdir(f"{PATH_TO_ENGINE_SRC}..")
subprocess.run([ts_node_path, f"{os.getcwd()}/setup.ts", f"{os.getcwd()}/src/assets"])
os.chdir(current_path)
