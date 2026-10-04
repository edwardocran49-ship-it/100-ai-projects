from pathlib import Path
from urllib.request import urlretrieve
base="https://raw.githubusercontent.com/OpenBCI/OpenBCI_GUI/master/OpenBCI_GUI/data/EEG_Sample_Data/"
out=Path(__file__).with_name("data");out.mkdir(exist_ok=True)
for remote,local in [("OpenBCI_GUI-v6-blinks-jawClench-alpha.txt","blinks-jawclench-alpha.txt"),("OpenBCI_GUI-v6-meditation.txt","meditation.txt")]:
 print(f"Downloading {remote}...");urlretrieve(base+remote,out/local)
