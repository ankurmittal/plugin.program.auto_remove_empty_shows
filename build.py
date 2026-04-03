import os
import shutil

ADDON_NAME = 'script.auto_remove_empty_shows'
ZIP_NAME = 'plugin.program.auto_remove_empty_shows.zip'
TEMP_DIR = f'/tmp/{ADDON_NAME}'

print(f'Building {ZIP_NAME}...')

# 1. Copy the entire current directory to a temp folder
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
shutil.copytree('.', TEMP_DIR, ignore=shutil.ignore_patterns('.git', '__pycache__', 'build.py', '*.zip'))

# 2. Zip the temp folder
zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ZIP_NAME)
shutil.make_archive(zip_path.replace('.zip', ''), 'zip', '/tmp', ADDON_NAME)

# 3. Cleanup
shutil.rmtree(TEMP_DIR)
print(f'Success! Created {ZIP_NAME}')
