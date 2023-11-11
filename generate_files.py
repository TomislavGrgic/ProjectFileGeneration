import os


def createSingleDirectory(name, path = None):
    path_name = f"{path}/{name}" if path is not None else f"{name}"
    os.mkdir(f'{path_name}') 
    

def createDoubleDirectory(name, path = None):
    path = f"/{path}" if path is not None else ""

    createSingleDirectory(name, f'src{path}')
    createSingleDirectory(name, f'include{path}')



def createFile(name, path = None, type = None):
    path = f"/{path}" if path is not None else ""
    
    if type == 'c' or type == None:
        createSourceFile(name = name, path = f'src{path}', include_path = f'include{path}')
    elif type == 'h' or type == None:
        createHeaderFile(name = name, path = f'include{path}')


def generateFileCore():
    #Creating main folders
    createSingleDirectory(name = "src") 
    createSingleDirectory(name = "lib") 
    createSingleDirectory(name = "include") 

    #Creating subfolders
    createDoubleDirectory(name = "modules")
    createDoubleDirectory(name = "debug")
    createSingleDirectory(name = "types", path = "include")

    #Create main file
    createSourceFile(name = "main", append_code = "#include <stdio.h>\r\nint main(void){\r\treturn 1;\r}")


def createSourceFile(name, path = None, include_path = None, append_code = None):
    if path == None:
        file = open(f'{name}.c', 'x')
    else:
        file = open(f'{path}/{name}.c', 'x')

    if include_path != None:
        file.write(f'#include \"{include_path}/{name}.h\"\r\n')
    
    if append_code != None:
        file.write(f'{append_code}')

    file.close()


def createHeaderFile(name, path = None, append_code = None):
    if path == None:
        file = open(f'{name}.h', 'x')
    else:
        file = open(f'{path}/{name}.h', 'x')

    name_upper = name.upper()
    file.write(f'#ifndef __{name_upper}_H__\r#define __{name_upper}_H__\r\r')
    
    if append_code != None:
        file.write(f'{append_code}')

    file.write(f'#endif /*__{name_upper}_H__*/')
    file.close()


def main():
    generateFileCore()
    createFile(name = "debugSerial", path = "debug")
    createFile(name = "utils")


if __name__ == "__main__":
    main()
