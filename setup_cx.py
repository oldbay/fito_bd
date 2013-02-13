from cx_Freeze import setup, Executable
import sys

productName = "FitoBD"

build_exe_options = {"packages": ["os",
                                  "sys",
                                  "camelot",
                                  "psycopg2"],
                     "includes" : "atexit"}

base = None
if sys.platform == "win32":
    exe = Executable(
        script = "main.py",
        base = "Win32GUI",
        initScript = None,
        targetName="FitoBD.exe",
        compress = True,
        copyDependentFiles = True,
        appendScriptToExe = False,
        appendScriptToLibrary = False,
        icon = "icon.ico",
        shortcutName = "FitoBD",
        shortcutDir = "ProgramMenuFolder"
        )
else:
    exe = Executable("main.py")

if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', 'C:\\' + productName]
    #sys.argv += ['--install-script', 'install.py']

setup(
      name="fitoBD",
      version="0.9",
      author="AGU",
      description="flora list database",
      long_description="""
      Installator for flora list database
      """,
      options = {"build_exe": build_exe_options},
      executables=[exe])
#      scripts=[
#               'install.py'
#               ]
#      )
