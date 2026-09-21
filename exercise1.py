import subprocess

def check_lore_build_version():
    result = subprocess.run(["lore.exe", "--version"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    print(result.returncode)
    return result 
check_lore_build_version()