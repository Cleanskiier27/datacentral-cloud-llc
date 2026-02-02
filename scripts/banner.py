"""
Shared banner utility for NetworkBuster scripts.
"""
import shutil

BANNER_TEXT = r"""
  _   _      _                      _    ____            _            
 | \ | | ___| |___      _____  _ __| | _| __ ) _   _ ___| |_ ___ _ __ 
 |  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ /  _ \| | | / __| __/ _ \ '__|
 | |\  |  __/ |_ \ V  V / (_) | |  |   <| |_) | |_| \__ \ ||  __/ |   
 |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\____/ \__,_|___/\__\___|_|   
"""

def print_ascii_art():
    """Print NetworkBuster ASCII Art."""
    print(BANNER_TEXT)

def print_centered_ascii_art():
    """Print NetworkBuster ASCII Art centered based on terminal width."""
    columns = shutil.get_terminal_size().columns
    print()
    for line in BANNER_TEXT.strip('\n').split('\n'):
        print(line.center(columns))
    print()