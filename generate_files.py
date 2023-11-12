import os
import sys
import json

PATH_ARGUMENT = 1

YES_CHARACTER = 'Y'
NO_CHARACTER = 'n'

green_code = '\033[92m'  # ANSI escape code for green text
purple_code = '\033[95m'  # ANSI escape code for purple text
cyan_code = '\033[96m'  # ANSI escape code for cyan text
reset_code = '\033[0m'    # Reset the color to default

filegen_prompt = f"{purple_code}[File generator]{green_code} >> {reset_code}"

option_names = ['Generate Core', 'Generate Core with Support', 'Custom generation', 'Exit']

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


def displayMenus():
    print(f'\tChoose one of the following options by typing the index number: \r\n')
    for i,names in enumerate(option_names):
        print(f'\t{purple_code}{i+1}) {reset_code} {names}\r')
    print("\r")
    print(f'\tFor more information type{cyan_code} -help{reset_code} \r\n')


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



def createFile(name, path = None, type = None):
    path = f"{path}" if path is not None else ""
    
    if type == 'c' or type == None:
        createSourceFile(name = name, path = os.path.join('src', path), include_path = f'include/{path}')
    if type == 'h' or type == None:
        createHeaderFile(name = name, path = os.path.join('include', path))


def goToRootPath():
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
    createFile(name = "debugSerial", path = "debug")
    createFile(name = "utils")


def createSourceFile(name, path = None, include_path = None, append_code = None):
    append_code = "" if append_code is None else append_code
    include_path = "" if include_path is None else f'#include \"{include_path}{name}.h\"\r'
    createAnyFile(name, 'c', path, f'{include_path}{append_code}')


def createHeaderFile(name, path = None, append_code = None):
    append_code = f'' if append_code is None else append_code
    createAnyFile(name, 'h', path, f'#ifndef __{name.upper()}_H__\r#define __{name.upper()}_H__\r\r{append_code}\r#endif /*__{name.upper()}_H__*/')


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
        file.write(f'{append_code}')

    file.close()
    print(f"{filegen_prompt}File created: {cyan_code}{name}.{type}{reset_code}\r")

def inputHandler():
    input_val: str = input(f"\t{cyan_code}User input: {reset_code}")
    print("\r")

    match input_val:
        case '1':
            f = open(os.path.join('templates', 'c_template.json'))
            generate_template = json.load(f)
            f.close()

            goToRootPath()
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
