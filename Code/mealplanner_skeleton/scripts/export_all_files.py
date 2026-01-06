"""
Skripts, kas eksportē visu projekta failu saturus
"""
import os
from pathlib import Path
from datetime import datetime

def should_skip_file(file_path):
    """Pārbauda, vai failu vajag izlaist"""
    skip_patterns = [
        '__pycache__',
        '.pyc',
        '.pyo',
        '.pyd',
        '.db',
        '.sqlite3',
        '.env',
        'node_modules',
        '.git',
        '.venv',
        'venv',
        '*.log',
        '*.tmp',
        '*.swp',
        '*.swo',
        '.DS_Store',
        'Thumbs.db'
    ]
    
    file_str = str(file_path).lower()
    for pattern in skip_patterns:
        if pattern in file_str:
            return True
    return False

def export_all_files():
    """Eksportē visu failu saturus"""
    project_root = Path(__file__).parent
    output_file = project_root / f"PROJEKTA_VISI_FAILI_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    files_exported = 0
    total_size = 0
    
    with open(output_file, 'w', encoding='utf-8') as out:
        # Header
        out.write("=" * 80 + "\n")
        out.write("PROJEKTA VISU FAILU SATURU EKSPORTS\n")
        out.write("=" * 80 + "\n")
        out.write(f"Izveidots: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"Projekta mape: {project_root}\n")
        out.write("=" * 80 + "\n\n")
        
        # Eksportē failus
        for root, dirs, files in os.walk(project_root):
            # Izlaiž nevajadzīgas mapes
            dirs[:] = [d for d in dirs if not should_skip_file(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Pārbauda, vai nav izlaist
                if should_skip_file(file_path):
                    continue
                
                # Izlaiž pašu eksporta failu
                if file_path.name.startswith('PROJEKTA_VISI_FAILI_'):
                    continue
                
                try:
                    rel_path = file_path.relative_to(project_root)
                    file_size = file_path.stat().st_size
                    total_size += file_size
                    
                    out.write("\n" + "=" * 80 + "\n")
                    out.write(f"FAILS: {rel_path}\n")
                    out.write(f"Izmērs: {file_size} baiti ({file_size/1024:.2f} KB)\n")
                    out.write("=" * 80 + "\n")
                    
                    # Mēģina nolasīt failu
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            out.write(content)
                            if not content.endswith('\n'):
                                out.write('\n')
                    except Exception as e:
                        out.write(f"[Nevar nolasīt failu: {e}]\n")
                    
                    files_exported += 1
                    
                except Exception as e:
                    out.write(f"\n[Kļūda apstrādājot {file_path}: {e}]\n")
        
        # Footer
        out.write("\n\n" + "=" * 80 + "\n")
        out.write("EKSPORTS PABEIGTS\n")
        out.write("=" * 80 + "\n")
        out.write(f"Eksportēti faili: {files_exported}\n")
        out.write(f"Kopējais izmērs: {total_size} baiti ({total_size/1024:.2f} KB)\n")
        out.write("=" * 80 + "\n")
    
    print(f"[OK] Eksporteti {files_exported} faili")
    print(f"Fails: {output_file}")
    print(f"Izmers: {total_size/1024:.2f} KB")
    
    return output_file

if __name__ == "__main__":
    export_all_files()
