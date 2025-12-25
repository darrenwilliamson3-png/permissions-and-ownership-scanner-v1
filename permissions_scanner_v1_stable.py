import csv
import os
import stat
import platform
import json
import argparse

results = []

if platform.system() != "Windows":
    import pwd
    import grp

def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan files for permission and ownership risks"
    )

    parser.add_argument(
        "path",
        help="Path to directory to scan"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan directories"
    )

    parser.add_argument(
        "--csv",
        default="permissions_report.csv",
        help="Output CSV file path"
    )

    parser.add_argument(
        "--json",
        default="permissions_report.json",
        help="Output JSON file path", metavar="FILE"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show per-file output"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress all output"
    )

    parser.add_argument(
        "--windows-only",
        action="store_true",
        help="Only flag Windows-relevant permission risks"
    )

    return parser.parse_args()

def scan_directory(path, recursive=False, windows_only=False, quiet=True):
    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            try:
                file_stat = os.stat(full_path)
                # Ownership (POSIX systems only)
                owner = "N/A"
                group = "N/A"

                if platform.system() != "Windows":
                    try:
                        owner = pwd.getpwuid(file_stat.st_uid).pw_name
                        group = grp.getgrgid(file_stat.st_gid).gr_name
                    except KeyError:
                        owner = str(file_stat.st_uid)
                        group = str(file_stat.st_gid)

                perm_text = stat.filemode(file_stat.st_mode)
                perm_octal = format(stat.S_IMODE(file_stat.st_mode), 'o')

                risk_flags = []

                if file_stat.st_mode & stat.S_IWOTH:
                    risk_flags.append("WORLD_WRITABLE")

                if (file_stat.st_mode & stat.S_IXUSR) and (
                        file_stat.st_mode & stat.S_IWGRP or file_stat.st_mode & stat.S_IWOTH
                     ):
                        risk_flags.append("EXECUTABLE_WRITABLE")

                # Windows specific context
                IS_WINDOWS = platform.system() == "Windows"
                if IS_WINDOWS and risk_flags:
                    risk_flags.append("WINDOWS_PERMISSION_HEURISTIC")

                    flags = ".".join(risk_flags) if risk_flags else "OK"

                    results.append({
                        "path": full_path,
                        # Prefix with apostrophe to prevent Excel treating '.rwx...' as a formula
                        "permissions_text": f"'{perm_text}",
                        "permissions_octal": perm_octal,
                        "risk_flags": flags,
                        "is_windows": IS_WINDOWS,
                    })

                if not quiet:
                    print(f"{perm_text} {perm_octal} {flags} {full_path}")

            except Exception as e:
                print(f"ERROR reading {full_path}: {e}")

        if not recursive:
            break

    return results

for r in results:
    print(
        f"{r['permissions_text']} {r['permissions_octal']}) "
        f"{r['risk_flags']} {r['path']})"
    )

def write_csv(results, output_path="permissions_report.csv"):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "path",
                "permissions_text",
                "permissions_octal",
                "risk_flags",
                "is_windows",
            ],
            quoting=csv.QUOTE_ALL
        )

        writer.writeheader()
        writer.writerows(results)

def write_json(results, output_path="permissions_report.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def main():
    args = parse_args()

    quiet = args.quiet or not args.verbose

    results = scan_directory(
        path=args.path,
        recursive=args.recursive,
        windows_only=args.windows_only,
        quiet=not args.verbose,
    )

    if args.csv:
        write_csv(results, args.csv)

    if args.json:
        write_json(results, args.json)

    if not quiet:
        print("Scan complete")

    if args.csv and not args.quiet:
        print(f"CSV Written: {args.csv}")

    if args.json and not args.quiet:
        print(f"JSON Written: {args.json}")

if __name__ == "__main__":
    main()