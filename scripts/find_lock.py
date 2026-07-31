import psutil, os
pdf = r'E:\Hermes Projects\cookbook\book\v2\index.pdf'
found = False
for proc in psutil.process_iter(['pid', 'name', 'open_files']):
    try:
        files = proc.info.get('open_files') or []
        for f in files:
            if f.path and os.path.samefile(f.path, pdf):
                print(f"{proc.info['name']} (PID {proc.info['pid']})")
                found = True
    except:
        pass
if not found:
    print("No process found with file open")
