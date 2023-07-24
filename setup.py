from cx_Freeze import setup, Executable

executable = Executable(script="redshifter.py", target_name="redshifter")

build_exe_options = {
    "build_exe": "dist",
    "packages": ["gi"],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
}

setup(
    name="redshifter",
    version="1.0.0",
    description="Redshifter",
    options={"build_exe": build_exe_options},
    executables=[executable],
)
