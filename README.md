# Permissions and Ownership Scanner (V1)

A cross-platform Python utility for scanning file permissions, identifying risky permission configurations, and exporting results in CSV and JSON formats for further analysis.

This tool was built as a **learning-focused but production-minded** utility, with emphasis on:

* clear architecture
* predictable CLI behaviour
* safe output handling
* extensibility for future versions

---

## Why This Tool Exists

This tool was created as a practical learning project to explore how filesystem permissions work across platforms and how permission-related risks can be identified and reported in a structured way.

Rather than focusing on remediation or deletion, the emphasis is on safe inspection, clear reporting, and predictable CLI behaviour, making the output suitable for review, auditing, or further processing. The project intentionally prioritises correctness, portability, and extensibility over aggressive automation.

---

## Features

* Scan files in a target directory (optionally recursive)
* Detect and report:

  * UNIX-style permission strings (e.g. `-rw-rw-rw-`)
  * Octal permission values (e.g. `666`, `777`)
  * Risk indicators such as:

    * `WORLD_WRITABLE`
    * `EXECUTABLE_WRITABLE`
    * `WINDOWS_PERMISSION_HEURISTIC`
	
* Cross-platform support:
  * POSIX ownership (user/group) on Unix-like systems
  * Safe heuristics on Windows where POSIX permissions do not apply

* Export results to:
  * CSV (Excel-compatible)
  * JSON (machine-readable)

* CLI flags for quiet / verbose output control

---

## Usage
	python permissions_scanner_v1.py <path> [options]

### Examples

Scan a directory (non-recursive, default quiet mode):
	python permissions_scanner_v1.py D:\TEST

Recursive scan:
	python permissions_scanner_v1.py D:\TEST --recursive


Write a custom CSV file:
	python permissions_scanner_v1.py D:\TEST --csv myreport.csv
```

Suppress all terminal output:
	python permissions_scanner_v1.py D:\TEST --quiet
```

Enable per-file terminal output:
	python permissions_scanner_v1.py D:\TEST --verbose

---

## Command-Line Options

| Flag            | Description                     |
| --------------- | ------------------------------- |
| `--recursive`   | Recursively scan subdirectories |
| `--csv <file>`  | Write results to a CSV file     |
| `--json <file>` | Write results to a JSON file    |
| `--quiet`       | Suppress all terminal output    |
| `--verbose`     | Show per-file scan results      |

> **Note:**
> Quiet mode suppresses per-file output but still allows completion messages and report generation.

---

## Output Format

### CSV Columns

	* `path`
	* `permissions_text`
	* `permissions_octal`
	* `risk_flags`
	* `is_windows`

### JSON

	An array of result objects containing the same fields as the CSV output.

---

## Excel Compatibility Note

Some permission strings (for example those beginning with `-`, such as `-rwxrwxrwx`) may be interpreted by Microsoft Excel as formulas, resulting in `#NAME?` errors.

To ensure compatibility:

	* All CSV fields are written as quoted text
	* JSON output is unaffected and preserves raw values

This behaviour is due to Excel’s automatic formula evaluation and is not a data integrity issue.

---

## Design Notes

	* Core scanning logic is isolated in `scan_directory()` for future reuse
	* Output handling (CSV / JSON) is separated from scanning logic
	* CLI parsing and execution flow are centralized in `main()`
	* Architecture is intentionally stable to support incremental versioned enhancements

---

## Limitations

	* This tool is read-only and does not modify, delete, or remediate files. Any corrective action must be performed manually by the user.
	* On Windows systems, traditional UNIX permission models do not apply. As a result, permission-related flags on Windows are based on 			heuristics rather than POSIX ownership and should be interpreted as indicators, not absolute security findings.
	* The tool does not currently evaluate effective permissions inherited through complex ACLs on Windows.
	* Designed for reporting and inspection rather than real-time monitoring.

	These limitations are intentional and help keep the tool predictable, safe, and suitable for learning and auditing purposes.

---

## Planned Improvements (V2+)

	* Progress indicators for large scans
	* Summary statistics (file counts, risk totals)
	* Optional deletion / remediation mode (explicit opt-in)
	* Structured logging support
	* Unit tests and CI integration

---

## License

MIT License
See `LICENSE` file for details.

---

## 👤 Author

Created as part of a learning and portfolio project focused on:

* Python fundamentals
* filesystem inspection
* CLI tooling
* defensive programming practices

Darren Williamson
Python Utility Development * Automation * Data Analysis
Uk Citizen / Spain-based / Remote
LinkedIn: https://www.linkedin.com/in/darren-williamson3/




