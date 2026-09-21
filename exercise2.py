import subprocess
import os

def offline_repository_creation():
    """Creating offline repository"""
    repo = r"E:\python_testing\Exercise2_repo"
    os.mkdir(repo)
    os.mkdir(r"E:\python_testing\exercise2_temp") 
    env = os.environ.copy()

    env["LORE_GLOBAL_PATH"] = "e:/python_testing/Exercise2_temp"
    env["LORE_AUTH_PATH"] = "e:/python_testing/Exercise2_temp"
 
    result = subprocess.run(["lore.exe", "repository", "create", "--offline", "Exercise2_repo"], cwd=repo,env=env, capture_output=True, text=True)
    print("stout: " + str(result.stdout)),
    print("sterr: " + str(result.stderr)),
    print("returncode: " + str(result.returncode)),
    return result
offline_repository_creation()    
    
