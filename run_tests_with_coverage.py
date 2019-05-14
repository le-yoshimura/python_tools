import os, sys
import subprocess
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

if __name__ == "__main__":
    target = os.path.join(parent_dir, 'unittests')
    for (curr, dirs, files) in os.walk(target):
        if curr != target:
            continue
        for file in files:
            if ".py" not in file:
                continue
            path = os.path.join(curr, file)
            answer = subprocess.call(f'coverage run {path}'.split())
            print(answer)
            answer = subprocess.call('coverage report'.split())
            print(answer)
