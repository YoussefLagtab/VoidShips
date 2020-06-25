from cx_Freeze import setup, Executable
import sys

version = "0.0.0.3"
modules = ["pygame", "noise", "random", "sys", "pytweening", "pickle"]
files = ["objects/", "scripts/", "textures/", "settings.py"]
outputdir = "C:\\Users\\Ciro\\VoidBoats" if sys.platform == "win32" else "/home/kolterdyx/PythonBuilds/VoidBoats"

build_options = {
	"packages": [],
	"excludes": [],
	"includes": modules,
	"build_exe": outputdir,
	"include_files": files,
}

base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("main.py", base=base, targetName="VoidBoats")]

setup(
	name="Void Boats",
	author="Kolterdyx",
	version=version,
	options={"build_exe": build_options},
	executables=executables,
)
