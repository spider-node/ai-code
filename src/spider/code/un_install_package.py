import subprocess


def uninstall_llama_index_packages():
    try:
        # 使用pip命令获取所有与llama-index相关的包
        packages = subprocess.check_output(['pip', 'freeze']).decode().split()
        for package in packages:
            if 'langchain' in package.lower():
                subprocess.check_call(['pip', 'uninstall', '-y', package])
                print(f"Uninstalled package: {package}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    uninstall_llama_index_packages()
