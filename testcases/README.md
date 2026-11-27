# Test Cases and Evidence

This document describes the automated tests for `rainfall_analyzer.py` and provides a place to record visual test evidence. The test suite uses Python's built-in `unittest` framework.

## Run the test suite

Run this command from the repository root:

```bash
python -m unittest discover -s testcases -p "test_*.py" -v
```

Expected result: all 15 tests pass. The chart tests mock `plt.show()`, so they verify chart-related output without opening GUI windows.

## Test-case list

| ID | Test case | Expected result |
| --- | --- | --- |
| TC01 | Load a valid CSV | Returns all valid month and rainfall rows. |
| TC02 | CSV contains missing values | Skips rows with missing month or rainfall and prints a message. |
| TC03 | CSV contains non-numeric rainfall | Skips the invalid rainfall row and reports its value. |
| TC04 | CSV contains negative rainfall | Skips the negative value and reports why. |
| TC05 | Input file does not exist | Prints a not-found message and returns `None`. |
| TC06 | Input file is empty | Prints an empty-file message and returns `None`. |
| TC07 | Statistics for the sample dataset | Reports total, mean, maximum, minimum, standard deviation, and heavy-rainfall months. |
| TC08 | No month exceeds the heavy-rainfall threshold | Reports that no month is above 200 mm. |
| TC09 | Compare values with the average | Separates above- and below-average months and reports that the bar chart was displayed. |
| TC10 | Draw the rainfall trend | Reports that the trend line chart was displayed. |
| TC11 | Select Exit in the menu | Displays the menu prompt and exits the loop. |
| TC12 | Enter an unsupported menu choice | Prints an invalid-option message. |
| TC13 | Select Statistics in the menu | Runs the statistics report. |
| TC14 | Select Heavy rainfall in the menu | Lists months above 200 mm. |
| TC15 | No valid input data | Prints a no-valid-data message and returns without showing the menu. |

The detailed assertions and test data are in [`test_rainfall_analyzer.py`](test_rainfall_analyzer.py).

## Visual test evidence (screenshots)

There are no captured screenshots in the repository at this time. Add genuine screenshots to a `testcases/screenshots/` directory, then replace the checklist below with links or embedded images. Do not use mock-ups as though they were actual application output.

Suggested captures:

1. **Main menu** — application started with a valid CSV.
2. **Statistics** — option 1 showing summary values and heavy-rainfall months.
3. **Input validation** — terminal output for skipped missing, invalid, or negative values.
4. **Average comparison** — option 3 output and the generated bar chart.
5. **Rainfall trend** — option 4 and its generated line chart.
6. **No valid data** — message shown when the CSV has no usable rows.

Suggested filenames: `01-main-menu.png`, `02-statistics.png`, `03-input-validation.png`, `04-average-comparison.png`, `05-rainfall-trend.png`, and `06-no-valid-data.png`.

Example Markdown to add after uploading a screenshot:

```markdown
### TC07 — Statistics

![Statistics output](screenshots/02-statistics.png)

**Expected:** total, mean, max/min, standard deviation, and heavy-rainfall months are shown.
```

## Test environment notes

- Requires the application dependencies: NumPy, Pandas, and Matplotlib.
- The tests use temporary CSV files and clean them up after each test.
- Matplotlib uses the `Agg` backend in tests to avoid requiring a display.
