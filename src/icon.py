import cv2
import os

def set_folder_icon(folder_path, icon_path):
    # Create desktop.ini file
    ini_path = os.path.join(folder_path, "desktop.ini")
    with open(ini_path, "w") as f:
        f.write("[.ShellClassInfo]\n")
        f.write(f"IconResource={icon_path},0\n")

    # Set folder attributes to system and read-only
    os.system(f"attrib +r\"{ini_path}\"")

    # Set desktop.ini as folder icon
    os.system(f"echo \"[ViewState]\" > \"{os.path.join(folder_path, 'desktop_.ini')}\"")
    os.system(f"attrib +h +r +s \"{os.path.join(folder_path, 'desktop_.ini')}\"")
    os.system(f"ren \"{os.path.join(folder_path, 'desktop_.ini')}\" desktop.ini")

    print(f"Folder icon set to {icon_path}.")


# Example usage
set_folder_icon("icon", "icon/fold.ico")
