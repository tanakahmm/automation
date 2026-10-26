import subprocess
from time import perf_counter

def run_command(command:list[str],timeout:float=5.0)->None:
    started=perf_counter()
    try:
        result=subprocess.run(command,capture_output=True,text=True,timeout=timeout,check=False)

        duration=perf_counter()-started
        
        print(f"Command: {command}")
        print(f"Exitcode: {result.returncode}")
        print(f"Duration: {duration:.3f} seconds")
        print(f"STDOUT: {result.stdout.strip()}")
        print(f"STDERR: {result.stderr.strip()}")

        if result.returncode==0:
            print("Result:Pass")
        else:
            print("Result:Failed")
        
    except subprocess.TimeoutExpired:
        print("Result:Timeout after {timeout} seconds ")

if __name__=="__main__":
    run_command(
    ["python3", "-c", "import time; time.sleep(10)"],
    timeout=2.0,
)
        
