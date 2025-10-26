#!/usr/bin/env python3
"""
System Resource Monitor Snapshot Analyzer
- Reads system_snapshot.txt (one line per snapshot)
- Detects threshold breaches (CPU > 85, MEM > 80, DISK > 90 by default)
- Computes averages and breach counts
- Writes flagged entries + summary to system_alerts.txt
- Optionally groups alerts by hour (bonus)
"""

import re
from datetime import datetime, timedelta
from collections import defaultdict

# ---------- CONFIG ----------
SNAPSHOT_FILE = "system_snapshot.txt"
ALERT_FILE = "system_alerts.txt"

CPU_THRESHOLD = 85
MEM_THRESHOLD = 80
DISK_THRESHOLD = 90

# Regex pattern to parse lines like:
# 2023-10-26 10:00:00 | CPU: 55% | MEM: 68% | DISK: 40%
LINE_PATTERN = re.compile(
    r'(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*'
    r'\|\s*CPU:\s*(?P<cpu>\d+)%\s*'
    r'\|\s*MEM:\s*(?P<mem>\d+)%\s*'
    r'\|\s*DISK:\s*(?P<disk>\d+)%\s*$'
)


# ---------- OPTIONAL: Create sample snapshot file for testing ----------
def generate_sample(filename=SNAPSHOT_FILE, start=None, count=24, step_minutes=5, seed=42):
    """
    Generates a sample system_snapshot.txt containing `count` lines.
    start: datetime or None (uses now if None)
    step_minutes: minutes between snapshots
    """
    import random
    random.seed(seed)
    if start is None:
        start = datetime.now().replace(second=0, microsecond=0)

    with open(filename, "w") as f:
        dt = start
        for i in range(count):
            # Simulate realistic percentages (0-100)
            cpu = random.randint(10, 100)
            mem = random.randint(20, 100)
            disk = random.randint(5, 100)
            line = f"{dt.strftime('%Y-%m-%d %H:%M:%S')} | CPU: {cpu}% | MEM: {mem}% | DISK: {disk}%\n"
            f.write(line)
            dt += timedelta(minutes=step_minutes)
    print(f"Generated sample file: {filename} with {count} lines.")


# ---------- Analyzer ----------
def analyze_snapshots(
    filename=SNAPSHOT_FILE,
    out_filename=ALERT_FILE,
    cpu_thresh=CPU_THRESHOLD,
    mem_thresh=MEM_THRESHOLD,
    disk_thresh=DISK_THRESHOLD,
    group_by_hour=False,
):
    total_lines = 0
    parsed_lines = 0

    cpu_sum = 0
    mem_sum = 0
    disk_sum = 0

    cpu_breaches = 0
    mem_breaches = 0
    disk_breaches = 0

    flagged_lines = []  # store raw lines that breached any threshold
    malformed_lines = []

    # bonus structure: group flagged entries by hour: { 'YYYY-MM-DD HH:00': [line, ...] }
    grouped_alerts = defaultdict(list)

    with open(filename, "r") as f:
        for raw in f:
            total_lines += 1
            line = raw.rstrip("\n")
            if not line.strip():
                continue  # skip empty lines

            m = LINE_PATTERN.match(line)
            if not m:
                malformed_lines.append(line)
                continue

            parsed_lines += 1
            # Convert captured strings to integers
            cpu = int(m.group("cpu"))
            mem = int(m.group("mem"))
            disk = int(m.group("disk"))
            timestr = m.group("time")

            # accumulate sums for averages
            cpu_sum += cpu
            mem_sum += mem
            disk_sum += disk

            # parse datetime for grouping if needed
            try:
                ts = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                ts = None

            # Check thresholds
            breached = False
            if cpu > cpu_thresh:
                cpu_breaches += 1
                breached = True
            if mem > mem_thresh:
                mem_breaches += 1
                breached = True
            if disk > disk_thresh:
                disk_breaches += 1
                breached = True

            if breached:
                flagged_lines.append(line)
                if group_by_hour and ts:
                    hour_key = ts.strftime("%Y-%m-%d %H:00")
                    grouped_alerts[hour_key].append(line)

    # Compute averages (handle zero parsed lines)
    def avg(total, count):
        return (total / count) if count else 0.0

    cpu_avg = avg(cpu_sum, parsed_lines)
    mem_avg = avg(mem_sum, parsed_lines)
    disk_avg = avg(disk_sum, parsed_lines)

    # Build summary
    summary_lines = []
    summary_lines.append(f"Snapshot file analyzed: {filename}")
    summary_lines.append(f"Total lines (raw): {total_lines}")
    summary_lines.append(f"Total parsed snapshots: {parsed_lines}")
    summary_lines.append("")
    summary_lines.append("AVERAGES:")
    summary_lines.append(f"  CPU average:  {cpu_avg:.2f}%")
    summary_lines.append(f"  MEM average:  {mem_avg:.2f}%")
    summary_lines.append(f"  DISK average: {disk_avg:.2f}%")
    summary_lines.append("")
    summary_lines.append("BREACH COUNTS (thresholds: CPU>{}, MEM>{}, DISK>{})".format(cpu_thresh, mem_thresh, disk_thresh))
    summary_lines.append(f"  CPU breaches:  {cpu_breaches}")
    summary_lines.append(f"  MEM breaches:  {mem_breaches}")
    summary_lines.append(f"  DISK breaches: {disk_breaches}")
    summary_lines.append("")
    summary_lines.append("FLAGGED ENTRIES:")
    if flagged_lines:
        for L in flagged_lines:
            summary_lines.append("  " + L)
    else:
        summary_lines.append("  None")
    summary_lines.append("")

    if malformed_lines:
        summary_lines.append("MALFORMED LINES (skipped):")
        for L in malformed_lines:
            summary_lines.append("  " + L)
        summary_lines.append("")

    # Bonus: grouped alerts by hour summary
    if group_by_hour:
        summary_lines.append("ALERTS GROUPED BY HOUR:")
        if grouped_alerts:
            for hour_key in sorted(grouped_alerts):
                summary_lines.append(f"  {hour_key}: {len(grouped_alerts[hour_key])} alerts")
                # Optionally show lines (commented to avoid long reports)
                for ln in grouped_alerts[hour_key]:
                    summary_lines.append("    " + ln)
        else:
            summary_lines.append("  None")
        summary_lines.append("")

    # Write results to file
    with open(out_filename, "w") as out:
        out.write("\n".join(summary_lines))

    # Also print to console
    print("\n".join(summary_lines))
    print(f"\nResults written to: {out_filename}")


# ---------- Example usage ----------
if __name__ == "__main__":
    # If you don't yet have a file, generate one to test:
    generate_sample(count=30, step_minutes=10)

    # Then analyze; set group_by_hour=True to see the bonus grouping
    analyze_snapshots(group_by_hour=True)
