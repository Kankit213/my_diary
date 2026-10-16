print("="*40)
print ("MINI PROJECT: My Diary (File Modes Practice")

print("Modes used: x, a+, r, r+, w+, rb, wb, w, a")
print("="*40)
 
import os                          # file exist hai ya nahi check karne ke liye
from datetime import datetime      # date aur time ke liye
 
# File ke naam ek jagah rakhe (baad me badalna aasan)
DIARY_FILE = "diary.txt"
VIEWS_FILE = "views.txt"
LOG_FILE = "log.txt"
BACKUP_FILE = "diary_backup.bin"
SEARCH_FILE = "search_results.txt"
 
# ---------- Setup: views counter file ----------
# r+ mode tabhi chalta hai jab file pehle se ho, isliye pehle check karte hain
try:
    with open(VIEWS_FILE, "r+") as f:
        pass                       # file hai, kuch karna nahi
except FileNotFoundError:
    with open(VIEWS_FILE, "x") as f:   # x: nayi file banao
        f.write("12345")                # 4 digit counter
 
# ---------- Main menu loop ----------
while True:
    print("\n===== MY DIARY =====")
    print("1. Create diary")
    print("2. Add entry")
    print("3. Read diary")
    print("4. Search word")
    print("5. Backup diary")
    print("6. Clear diary")
    print("7. View activity log")
    print("8. Exit")
 
    choice = input("Choose (1-8): ")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")   # abhi ka time
    action = "dairy created"                    # log me kya likhna hai (khaali = kuch nahi)
 
    # Option 2-6 ke liye diary pehle se honi chahiye
    if choice in ["2", "3", "4", "5", "6"] and not os.path.exists(DIARY_FILE):
        print("Pehle diary banao (option 1).")
        continue                   # menu par wapas
 
    # ----- 1. Create diary: mode "x" -----
    if choice == "1":
        try:
            with open(DIARY_FILE, "x") as f:       # file hai to error
                f.write("=== My Diary ===\n")      # pehli line = header
            print("Diary ban gayi!")
            action = "Diary created"
        except FileExistsError:
            print("Diary pehle se hai. Overwrite nahi kiya.")
            action = "Create failed (already exists)"
 
    # ----- 2. Add entry: mode "a+" -----
    elif choice == "2":
        text = input("Aaj kya hua? ")
        with open(DIARY_FILE, "a+") as f:
            f.write(f"[{time_now}] {text}\n")       # end me judega
            f.seek(0)                               # padhne ke liye shuru me jao
            lines = f.readlines()                   # saari lines list me
        total_entries = len(lines) - 1              # header line minus
        print("Entry save ho gayi! Total entries:", total_entries)
        action = "Entry added"
 
    # ----- 3. Read diary: mode "r" + views counter: mode "r+" -----
    elif choice == "3":
        with open(DIARY_FILE, "r") as f:
            for line in f:
                print(line.strip())                 # \n hata ke print
 
        with open(VIEWS_FILE, "r+") as f:
            views = int(f.read()) + 1               # purana count padho, +1
            f.seek(0)                               # pointer wapas shuru me
            f.write(str(views).zfill(4))            # 4 digit me overwrite
        print("\nDiary", views, "baar padhi gayi.")
        action = "Diary read"
 
    # ----- 4. Search word: mode "w+" -----
    elif choice == "4":
        word = input("Kaunsa word dhundhna hai? ").lower()
        found = 0
        with open(SEARCH_FILE, "w+") as result_file:   # purana result delete
            with open(DIARY_FILE, "r") as f:
                for line in f:
                    if word in line.lower():
                        result_file.write(line)        # match mila to likho
                        found += 1
            result_file.seek(0)                        # padhne ke liye shuru me
            if found > 0:
                print("\n--- Results ---")
                print(result_file.read())
            else:
                print("Koi result nahi mila.")
        action = "Searched: " + word
 
    # ----- 5. Backup: modes "rb" aur "wb" -----
    elif choice == "5":
        with open(DIARY_FILE, "rb") as src:            # binary me padho
            data = src.read()
        with open(BACKUP_FILE, "wb") as dst:           # binary me likho
            dst.write(data)
        print("Backup ban gaya!", len(data), "bytes copy hue.")
        action = "Backup created"
 
    # ----- 6. Clear diary: mode "w" -----
    elif choice == "6":
        sure = input("Pakka saari entries delete karni hain? (yes/no): ")
        if sure.lower() == "yes":
            with open(DIARY_FILE, "w") as f:           # truncate = purana saaf
                f.write("=== My Diary ===\n")
            print("Diary saaf ho gayi.")
            action = "Diary cleared"
        else:
            print("Cancel kar diya.")
 
    # ----- 7. View log: mode "r" -----
    elif choice == "7":
        try:
            with open(LOG_FILE, "r") as f:
                print("\n--- Activity Log ---")
                print(f.read())
        except FileNotFoundError:
            print("Abhi koi log nahi hai.")
 
    # ----- 8. Exit -----
    elif choice == "8":
        action = "Program closed"
 
    else:
        print("Galat choice. 1 se 8 ke beech number daalo.")
 
    # ---------- Har action ko log me likho: mode "a" ----------
    if action != "dairy created":
        with open(LOG_FILE, "a") as f:
            f.write(f"[{time_now}] {action}\n")
 
    if choice == "8":
        print("Bye!")
        break