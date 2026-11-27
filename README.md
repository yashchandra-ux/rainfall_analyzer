# Rainfall Data Analyzer

A menu-driven Python application that reads monthly rainfall data from a CSV file, validates it, reports useful statistics, and visualizes rainfall comparisons and trends.

## Project at a glance

- **Language:** Python
- **Libraries:** NumPy, Pandas, Matplotlib
- **Input:** CSV with month names and rainfall measurements in millimetres
- **Validation:** Skips rows with missing, non-numeric, or negative rainfall values
- **Visualizations:** Average-comparison bar chart and rainfall trend line chart
- **Automated tests:** 15 `unittest` cases

## Features

1. Loads rainfall data from a CSV file and reports invalid rows.
2. Calculates total rainfall, mean, population standard deviation, maximum, and minimum.
3. Lists months with heavy rainfall (strictly **above 200 mm**).
4. Compares each month with the average and displays a colour-coded bar chart.
5. Displays a line chart showing the rainfall trend.
6. Provides an interactive menu for choosing an analysis.

## Requirements and setup

Python 3.9 or later is recommended. Install the required libraries:

```bash
python -m pip install numpy pandas matplotlib
```

Clone the repository and move into its directory:

```bash
git clone https://github.com/yashchandra-ux/rainfall_analyzer.git
cd rainfall_analyzer
```

## CSV format

The CSV should contain two columns: `Month` and `Rainfall_mm`. A header is optional.

```csv
Month,Rainfall_mm
Jan,100
Feb,250
Mar,150
Apr,300
```

Rainfall must be a non-negative number. Rows with missing values, invalid rainfall, or negative rainfall are skipped with a message. The program accepts a CSV path as its first command-line argument; if omitted, it looks for `rain.csv` in the current directory.

## Run the application

```bash
python rainfall_analyzer.py rain.csv
```

Choose an option from the menu:

| Option | Action |
| --- | --- |
| 1 | Show summary statistics and heavy-rainfall months |
| 2 | List heavy-rainfall months |
| 3 | Compare rainfall with the average and display a bar chart |
| 4 | Display a rainfall trend line chart |
| 5 | Exit |

## Example output

For the sample CSV above, option 1 reports results similar to:

```text
Total: 800 mm | Mean: 200.00
Max: Apr (300) | Min: Jan (100)
Std Dev: 77.46
Heavy rainfall months: Feb, Apr
```

## Automated tests

The test suite checks CSV loading and validation, statistics, chart-related output, and menu behaviour. Matplotlib is configured for a non-interactive backend during tests, so charts do not open during the test run.

Run all tests from the repository root:

```bash
python -m unittest discover -s testcases -p "test_*.py" -v
```

See [`testcases/README.md`](testcases/README.md) for the test-case list and results documentation.

## Screenshots and test evidence

The repository currently contains automated test code but **does not contain captured application screenshots**. No screenshots have been invented or represented as real test evidence. To add genuine screenshots, save them in `testcases/screenshots/` and link them in the [test evidence guide](testcases/README.md). Useful captures include the main menu, statistics output, invalid-row handling, the comparison bar chart, and the trend chart.

## Repository contents

```text
.
├── rainfall_analyzer.py
├── README.md
└── testcases/
    ├── README.md
    └── test_rainfall_analyzer.py
```

## Author

**Yash Chandra**
