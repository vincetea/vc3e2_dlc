import subprocess
from pathlib import Path
import sys


script_dir = Path(__file__).parent
quickbms = script_dir / "quickbms.exe"
bms_script = script_dir / "cpk.bms"
output_dir = script_dir / "Extracted"


if len(sys.argv) > 1:
    base_dir = Path(sys.argv[1])
else:
    base_dir = script_dir / "OG DLC Files"


if not quickbms.exists():
    print(f"Error: quickbms.exe not found in {script_dir}")
    sys.exit(1)

if not bms_script.exists():
    print(f"Error: cpk.bms script not found in {script_dir}")
    sys.exit(1)

if not base_dir.exists():
    print(f"Error: Input folder not found: {base_dir}")
    sys.exit(1)


output_dir.mkdir(exist_ok=True)


for folder in base_dir.iterdir():
    if folder.is_dir():
        suboutput = output_dir / folder.name
        suboutput.mkdir(exist_ok=True)

        # Recursively find *_DATA.EDAT
        edat_file_list = list(folder.rglob("*_DATA.EDAT"))
        if not edat_file_list:
            print(f"No *_DATA.EDAT files found in {folder}")
            continue

        for edat_file in edat_file_list:
            print(f"Extracting {edat_file} -> {suboutput}")
            subprocess.run([
                str(quickbms),
                str(bms_script),
                str(edat_file),
                str(suboutput)
            ])