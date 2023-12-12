import glob
import os
import zipfile

all_files = set()

def zip_directory(directory_path, zipf, parent_dir=''):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.join(parent_dir, os.path.relpath(file_path, directory_path))
            if arcname in all_files:
                continue
            print(arcname)
            zipf.write(file_path, arcname)
            all_files.add(arcname)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            arcname = os.path.join(parent_dir, os.path.relpath(dir_path, directory_path))
            zip_directory(dir_path, zipf, arcname)

if __name__ == '__main__':
    script_path = os.path.dirname(os.path.abspath(__file__))
    version = None
    version_file_path = os.path.join(script_path, 'examples.txt')
    with open(version_file_path) as f:
        version = f.read().strip()
    if not version:
        raise 'examples.txt not found'
    print('Version:', version)
    resource_path = os.path.join(script_path, f'canmv-ide-resource-v{version}.zip')
    print('Resource:', resource_path)
    with zipfile.ZipFile(resource_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zip_directory(os.path.join(script_path, 'examples'), zipf, 'examples')
        zip_directory(os.path.join(script_path, 'models'), zipf, 'models')
