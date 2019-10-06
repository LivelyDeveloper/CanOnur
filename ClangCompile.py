from subprocess import call
from sys import argv
from os import path
import glob

#PROJECT SETTINGS_________________________________
Output_File = None
include_dirs=["/home/commander/Documents/Programming/Test"
]
library_dirs=[]
#_________________________________________________


#FILESETTINGS_____________________________________
ClangVer = 8
Verbose = False
Scanned_Filetypes = [".cpp", ".h", ".cc"]
Optimisation_Level = 3 #0 - 3
#_________________________________________________


def get_acceptable_int(min, max, text):
    error = False
    try:
        command = input(text)
        command = int(command)
    except TypeError:
        error = True
    if error:
        print("Value not a number")
        return get_acceptable_int(min,max,text)
    if not command < max and command >= min:
        print("Value not in range")
        return get_acceptable_int(min,max,text)
    return command

def scan_files():
    files = []
    for type in Scanned_Filetypes:
        if type == "":
            continue
        if type[0] != ".":
            type = "." + type
        for file in glob.glob("*" + type):
            files.append(file)
    if len(files) == 0:
        print("No files with compatible extensions found.")
        exit()
    elif len(files) == 1:
        return files[0]
    else:
        print("Please select one of the following files:")
        for x in range(len(files)):
            print(x+1, "-", files[x])
        file_id = get_acceptable_int(1,len(files) + 1, "File id:")
        return files[file_id - 1]

if len(argv) < 2:
    Filename = scan_files()
else:
    Filename = argv[1]


def compile_call():
    global Output_File
    if Output_File is None or Output_File=="":
        Output_File = path.splitext(Filename)[0] + "_" +"Output"
    call = ["clang++-" + str(ClangVer)[0], Filename,"-o" + str(Optimisation_Level), "-o", Output_File]
    for dir in include_dirs:
        if dir == "":
            continue
        else:
            arg = "--include-directory="
            arg = arg + dir
            call.append(arg)
    for dir in library_dirs:
        if dir == "":
            continue
        else:
            arg = "--library-directory="
            arg = arg + dir
            call.append(arg)
    if Verbose:
        call.append("--verbose")
    return call
c = compile_call()
print("Processing:", Filename)
print("Output File:", Output_File)

print("Launching Clang C++ Version", ClangVer, "|", "Optimisation Level", Optimisation_Level)
call(c)
print("Compile Command Complete")