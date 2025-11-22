import PyInstaller.__main__
import os
import shutil

def build_exe():
    # Remove previous build directories
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    params = [
    'main.py',  # Your main script
    '--name=NinjaSageBot',
    '--onefile',  # Single executable
    '--console',  # Show console window (to view logs)
    '--add-data=data;data',  # Include the 'data' folder
    # '--add-data=quick_login.json;.',  # Include specific config file
    '--hidden-import=config',
    '--hidden-import=amf_req',
    '--hidden-import=leveling',
    '--hidden-import=eudemon',
    '--hidden-import=event',
    '--hidden-import=event_finisher',
    '--hidden-import=shadow_war',
    '--hidden-import=resources',
    '--hidden-import=utils',
    '--hidden-import=tkinter',
    '--hidden-import=keyboard',
    '--hidden-import=requests',
    '--hidden-import=pycryptodome',
    '--hidden-import=py3amf',
    '--hidden-import=pyamf',  # Add this line for pyamf module
    '--hidden-import=pyamf.amf0',  # Add this line for pyamf.amf0 module
    '--hidden-import=cpyamf',  # Add this line for cpyamf
    '--collect-all=tkinter',
    '--collect-all=keyboard',
    '--collect-all=requests',
    '--collect-all=pycryptodome',
    '--collect-all=py3amf',
    '--collect-all=pyamf',  # Ensure that pyamf is included in the bundle
    '--noconfirm',
    '--clean'
]

    
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    build_exe()
