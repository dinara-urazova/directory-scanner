"""
Консольный скрипт, который запускается из терминала 
Пример запуска из терминала:
$ python ./scan-dir-size.py C:\\Users\\79177\\Developer\\Занятия

Необходимые функции для реализации:
sys.argv - получает аргументы командной строки (путь к C:\\Users\\79177)
для этого нужно импортировать модуль import sys / from sys import argv

из модуля os (ф-ции операционной системы):
os.scandir(путь к директории, кот нужно просканировать), возвращает "список" файлов/папок в директории
ф-я возвращает итератор (похоже на массив или list), к итератору применим цикл for _ in
Каждый элемент итератора (dir_entry)  - 
1) файл (у файла есть название, размер и т.д) 
2) папку (директорию/каталог), сама папка  - только как точка для входа рекурс ф-ции (есть название, размер неизвестен)
3) ссылка (sym link (символическая ссылка) - при обходе мы их игнорируем (так как ссылки на другие папки)

dir_entry - Объект, у которого есть следующие полезные функции:
1) dir_entry.is_dir() - возвращает True, если данная entry - папка
2) dir_entry.is_symlink() - возвращает True, если данная entry - symlink
3) dir_entry.stat() - возвращает объект типа stat_result, у кот есть полезное св-во st_size (р-р файлов в байтах) - это int
"""
import os
import sys
MAX_DEPTH = 1_000
def get_icon_by_filename(filename: str) -> str:
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        return "🖼️  "
    if filename.lower().endswith((".mp3",".wav", ".aac", ".flac")):
        return "🎵 "
    if filename.lower().endswith((".doc",".docx", ".txt", ".pdf")):
        return "📕 "
    if filename.lower().endswith((".py")):
        return "💻 " 
    if filename.lower().endswith((".mp4", ".avi", ".mov", ".wmv")):
        return "📽️  "
    return "❓ "

def rec_scan(cur_dir: str, depth: int) -> None:
    if depth == MAX_DEPTH:
        return
    global count_files
    global total_size_in_bytes
    global count_skipped
    try:
        dir_entry_iter = os.scandir(cur_dir)
    except (PermissionError, FileNotFoundError):
        count_skipped += 1
        print(f"[WARN] {cur_dir} permission denied, skipped")
    else:
        dirs = []
        files = []
        for dir_entry in dir_entry_iter:
            if dir_entry.is_dir() and not dir_entry.is_symlink():
                dirs.append(dir_entry.name)
            elif dir_entry.is_symlink():
                count_skipped += 1
                print(f"[INFO] {dir_entry.name} is symlink, skipped")
            else: # dir_entry  - это файл,можно считать размер в total size
                files.append(dir_entry.name)
                count_files += 1
                total_size_in_bytes += dir_entry.stat().st_size
        size_dirs = len(dirs)
        size_files = len(files)
        for i in range(size_dirs):
            if i == size_dirs - 1 and size_files == 0:
                sep = "└──"
            else:
                sep = "├──"
            print(f"{'│   ' * depth}{sep}📁 {dirs[i]}")
            rec_scan(f"{cur_dir}/{dirs[i]}", depth + 1)
        for i in range(size_files):
            if i == size_files - 1:
                sep = "└── "
            else:
                sep = "├── "
            icon = get_icon_by_filename(files[i])
            print(f"{'│   ' * depth}{sep}{icon}{files[i]}")
        
     
base_dir = sys.argv[1] # путь к папке, для кот мы д посчитать р-р
count_files = 0
total_size_in_bytes = 0
count_skipped = 0

rec_scan(base_dir, 0)
print(f"Processed {count_files} files")
if count_skipped > 0:
    print(f"Skipped {count_skipped} files")
print(f"Total size: {total_size_in_bytes:,} bytes")
