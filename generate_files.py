import os
import sys
import json
import re

PATH_ARGUMENT = 1

YES_CHARACTER = 'Y'
NO_CHARACTER = 'n'

green_code = '\033[92m'  # ANSI escape code for green text
purple_code = '\033[95m'  # ANSI escape code for purple text
cyan_code = '\033[96m'  # ANSI escape code for cyan text
reset_code = '\033[0m'    # Reset the color to default

content_pattern = r'@.*?\.json'

filegen_prompt = f"{purple_code}[File generator]{green_code} >> {reset_code}"
option_names = ['Generate Core', 'Generate Core with Support', 'Custom generation', 'Exit']
keyword_list = ['$NAME_UPPER$', '$NAME_LOWER$', '$NAME$']

python_script_path = os.getcwd()
project_root_path = os.getcwd()

def loadTemplateFile(template_name: str):
    os.chdir(python_script_path)
    f = open(os.path.join('data','templates', template_name))
    template_file = json.load(f)
    f.close()
    os.chdir(project_root_path)

    return template_file


def printOutJSONLoop(json_data, tab_cnt):
    for i,file in enumerate(json_data["files"]):
        print(('    '*tab_cnt) + f'{purple_code}- {reset_code}{file["name"]}' + (f'/' if file["type"] == "folder" else f'.{file["type"]}'))
        if file["files"] is not []:
            printOutJSONLoop(file, tab_cnt+1)


def addFileToDirectoryJSON(dest, src, path):
    return


def printOutJSON(json_data):
    tab_cnt = 1
    print(f"{filegen_prompt}Printing out the JSON template directory tree. {reset_code}\r")
    printOutJSONLoop(json_data, tab_cnt)


def generateFromJSON(json_data, path):
    for file in json_data["files"]:
        if file["type"] == "folder":
            createSingleDirectory(name = file["name"], path = path)
            if file["files"] is not []:
                path_next = os.path.join(f'' if path is None else f'{path}', file["name"])
                generateFromJSON(file, path_next)
        else: 
            createAnyFile(name = file["name"], path = path, type = file["type"], append_code = file["content"])


def clearTerminal():
    if os.name == 'nt':
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Unix/Linux/MacOS


def splashScreen():
    clearTerminal()
    print(f'{purple_code}')
    print("\r\n\r\n")
    print("\t███████╗██╗██╗     ███████╗     ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗  \r") 
    print("\t██╔════╝██║██║     ██╔════╝    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗ \r") 
    print("\t█████╗  ██║██║     █████╗      ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝ \r") 
    print("\t██╔══╝  ██║██║     ██╔══╝      ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗ \r") 
    print("\t██║     ██║███████╗███████╗    ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║ \r") 
    print("\t╚═╝     ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ \r")
    print(f"\t{cyan_code}by: Etaler Æman")
    print("\r\n")
    print(f'{reset_code}')


def displayFooter():
    print(f'\tFor more information type{cyan_code} -help{reset_code} \r\n')


def displayMenus():
    print(f'\tChoose one of the following options by typing the index number: \r\n')
    for i,names in enumerate(option_names):
        print(f'\t{purple_code}{i+1}) {reset_code} {names}\r')
    print("\r")
    displayFooter()


def getFolderPathArgument():
    current_directory = os.getcwd()

    try:
        root_path = sys.argv[PATH_ARGUMENT]

        if os.path.isabs(root_path):
            path_out = root_path
        else:
            path_out = os.path.abspath(root_path)

        print(f"{filegen_prompt}Folder path where the project will be created is: {cyan_code}{path_out}{reset_code}\r")
    except:
        path_out = None
        print(f"{filegen_prompt}Project will be created in current folder: {cyan_code}{current_directory}{reset_code}\r")

    val = input(f"{filegen_prompt}Are you sure you want to proceed? {green_code}[Y/n]{reset_code}: ")
    while val != YES_CHARACTER and val != NO_CHARACTER:
        val = input(f"{filegen_prompt}Invalid input. Are you sure you want to proceed? {green_code}[Y/n]{reset_code}: ")

    if val.lower() == YES_CHARACTER.lower():
        return path_out
    else:
        sys.exit()


def createSingleDirectory(name, path = None):
    path_name = os.path.join(path, name) if path is not None else f"{name}"
    
    try:
        os.mkdir(f'{path_name}')
        print(f"{filegen_prompt}Folder created: {cyan_code}{path_name}{reset_code}\r")
    except: 
        print(f"{filegen_prompt}Folder {cyan_code}{path_name}{reset_code} already exists.\r")
    

def createDoubleDirectory(name, path = None):
    path = f"{path}" if path is not None else ""
    os.path.join('src', path)
    createSingleDirectory(name, os.path.join('src', path))
    createSingleDirectory(name, os.path.join('include', path))


def goToRootPath():
    global project_root_path
    project_root_path = getFolderPathArgument()

    if project_root_path is not None:
        try:
            os.mkdir(project_root_path)
        except:
            print(f"{filegen_prompt}Project path already exists: {cyan_code}{project_root_path}{reset_code}\r")

        os.chdir(project_root_path)


def generateSupportFiles():
    #Creating folders
    createSingleDirectory(name = "lib")

    #Creating subfolders
    createDoubleDirectory(name = "modules")
    createDoubleDirectory(name = "debug")
    createSingleDirectory(name = "types", path = "include")

    #Create main file
    createAnyFile(name = "debugSerial", type = 'c', path = os.path.join('src', 'debug'))
    createAnyFile(name = "debugSerial", type = 'h', path = os.path.join('include', 'debug'))
    createAnyFile(name = "utils", type = 'c', path = 'src')
    createAnyFile(name = "utils", type = 'h', path = 'include')


def createAnyFile(name, type, path = None, append_code = None):
    if path == None:
        file_path = f'{name}.{type}'
    else:
        file_path = os.path.join(path, f'{name}.{type}')

    if os.path.exists(file_path) is True:
        print(f"{filegen_prompt}File {cyan_code}{name}.{type}{reset_code} already exists.\r")
        return
    
    file = open(file_path, 'x')
    
    if append_code is not None:
        append_code = substituteContents(append_code)
        append_code = substituteKeywords(append_code, name)
        file.write(f'{append_code}')

    file.close()
    print(f"{filegen_prompt}File created: {cyan_code}{name}.{type}{reset_code}\r")


def substituteContents(append_code: str):
    modified_code = append_code
    match_list = re.findall(content_pattern, modified_code)
    
    if not match_list:
        return modified_code
    
    os.chdir(python_script_path)

    for json_pattern in match_list:
        json_file_name = json_pattern.replace('@', '')
        f = open(os.path.join('data','contents', json_file_name))
        json_file = json.load(f)
        f.close()
        modified_code = modified_code.replace(json_pattern, json_file["content"])
    
    os.chdir(project_root_path)

    return modified_code


def substituteKeywords(append_code: str, name):
    modified_code = append_code

    while '$NAME_UPPER$' in modified_code:
        modified_code = modified_code.replace('$NAME_UPPER$', name.upper())

    while '$NAME_LOWER$' in modified_code:
        modified_code = modified_code.replace('$NAME_LOWER$', name.upper())

    while '$NAME$' in modified_code:
        modified_code = modified_code.replace('$NAME$', name.upper())

    return modified_code


def inputHandler():
    input_val: str = input(f"\t{cyan_code}User input: {reset_code}")
    print("\r")

    match input_val:
        case '1':
            goToRootPath()
            generate_template = loadTemplateFile('c_template.json')
            printOutJSON(generate_template)
            generateFromJSON(generate_template, None)

        case '2':
            print("LOL2")

        case '3':
            print("LOL3")
        
        case '4':
            print("LOL4")


def main():
    splashScreen()
    displayMenus()
    inputHandler()


if __name__ == "__main__":
    main()
