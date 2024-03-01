from pathlib import Path
import os
import shutil
import subprocess

def main():
    project_name = ""
    project_location = ""
    raylib_version = "5.0"

    project_name = input("Enter the project name: ")
    while project_name == "":
        print("Project name cannot be empty")
        project_name = input("Enter the project name: ")

    project_location = input("Enter the project location: ")
    while project_location == "":
        print("Project location cannot be empty")
        project_location = input("Enter the project location: ")

    project_location = Path(project_location).resolve()

    try:
        os.makedirs(f"{str(project_location)}/{project_name}/{project_name}/src")
    except FileExistsError:
        print(f"Directory {project_name} already exists")
        return

    shutil.copy("assets/main.cpp", f"{str(project_location)}/{project_name}/{project_name}/src/main.cpp")
    shutil.copy("assets/setup.py", f"{str(project_location)}/{project_name}/setup.py")

    shutil.copy("assets/premake-template.lua", f"assets/premake5.lua")

    with open(f"assets/premake5.lua", "r") as file:
        file_data = file.read()

    file_data = file_data.replace("PROJECT_NAME", project_name)

    with open(f"assets/premake5.lua", "w") as file:
        file.write(file_data)

    shutil.copy("assets/premake5.lua", f"{str(project_location)}/{project_name}/premake5.lua")

    raylib_version = input("Enter the raylib version (5.0, 4.5...): ")
    raylib_download_path = f"https://github.com/raysan5/raylib/releases/download/{raylib_version}/raylib-{raylib_version}_win64_msvc16.zip"

    os.makedirs("assets/temp")
    os.makedirs("assets/vendor/raylib")

    os.system(f"curl -L {raylib_download_path} -o assets/temp/raylib.zip")
    shutil.unpack_archive("assets/temp/raylib.zip", "assets/temp/raylib")

    shutil.copytree(f"assets/temp/raylib/raylib-{raylib_version}_win64_msvc16/include", f"assets/vendor/raylib/include")
    shutil.copytree(f"assets/temp/raylib/raylib-{raylib_version}_win64_msvc16/lib", f"assets/vendor/raylib/lib")
    shutil.copy(f"assets/temp/raylib/raylib-{raylib_version}_win64_msvc16/LICENSE", f"assets/vendor/raylib/LICENSE")


    shutil.copytree("assets/vendor", f"{str(project_location)}/{project_name}/vendor")

    shutil.rmtree("assets/temp")
    shutil.rmtree("assets/vendor/raylib")

    shutil.copy("assets/gitignore", f"{str(project_location)}/{project_name}/.gitignore")

    print(f"Project {project_name} created at {project_location}")
    print(f"Run 'cd {project_location}/{project_name} && python setup.py' to generate the project files.")

if __name__ == "__main__":
    main()