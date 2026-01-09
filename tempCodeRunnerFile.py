import random
import time
from datetime import datetime, timedelta

# Phrases to mix
phrases = [
    "code paints invisible landscapes",
    "silence holds the next idea",
    "patterns bloom from noise",
    "light folds into logic",
    "stars compile the night",
    "ideas ripple like water",
    "curiosity maps new terrain",
    "time hums in quiet loops",
    "pixels drift into meaning",
    "keys tap the rhythm of thought",
    "algorithms dance in shadows",
    "bytes whisper ancient truths",
    "functions unfold like origami",
    "logic flows like liquid silver",
    "data streams carve new paths",
    "variables hold infinite possibility",
    "loops spiral toward understanding",
    "conditions branch into futures",
    "memory traces forgotten dreams",
    "threads weave parallel stories"
]

# Read current line count
try:
    with open('live_text.tsx', 'r', encoding='utf-8') as f:
        current_lines = sum(1 for _ in f)
except FileNotFoundError:
    current_lines = 0

target_lines = 1000000
lines_to_add = target_lines - current_lines

if lines_to_add <= 0:
    print(f"File already has {current_lines} lines (target: {target_lines})")
    exit(0)

print(f"Current lines: {current_lines}")
print(f"Adding {lines_to_add} lines to reach {target_lines} lines total")
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Calculate timing for ~4 hours
target_duration = 40 * 60 * 60  # 4 hours in seconds

batch_size = 1  # Write one line at a time for live effect
delay_per_batch = target_duration / lines_to_add if lines_to_add > 0 else 1

print(f"Writing {batch_size} lines every {delay_per_batch:.2f} seconds")
print(f"Estimated completion time: {(datetime.now() + timedelta(seconds=target_duration)).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Writing slowly... Press Ctrl+C to stop\n")

# Open file in append mode
start_time = time.time()
try:
    with open('live_text.tsx', 'a', encoding='utf-8') as f:
        # Write header
        f.write(f"\n-- Slow Random Text Generator (4hr target): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} --\n")
        

        line_number = 1
        for i in range(lines_to_add):
            phrase1 = random.choice(phrases)
            phrase2 = random.choice(phrases)
            random_num = random.randint(100000, 999999)
            line = f"[{line_number:06d}-{random_num}] {phrase1}; {phrase2}.\n"
            f.write(line)
            f.flush()  # Write each line immediately
            line_number += 1
            # Progress update every 1000 lines
            if (i + 1) % 1000 == 0:
                elapsed = time.time() - start_time
                percent = ((i + 1) / lines_to_add) * 100
                eta_seconds = (elapsed / (i + 1)) * (lines_to_add - i - 1)
                eta_time = datetime.now() + timedelta(seconds=eta_seconds)
                print(f"Progress: {i + 1:,} / {lines_to_add:,} ({percent:.1f}%) | ETA: {eta_time.strftime('%H:%M:%S')}")
            if i + 1 < lines_to_add:
                time.sleep(delay_per_batch)

except KeyboardInterrupt:
    print(f"\n\nStopped by user at {line_number:,} lines")
    print(f"Total lines in file now: {current_lines + line_number}")
    exit(0)

elapsed_time = time.time() - start_time
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total time: {elapsed_time/3600:.2f} hours")
print(f"Total lines in file: {current_lines + lines_to_add}")