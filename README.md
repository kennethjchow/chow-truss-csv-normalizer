# CSV Normalization

The purpose of this function is to normalize the incoming csv data. 

## Installation Steps

1. Go to https://www.python.org/downloads/ and download python
2. Go to the following page https://python-poetry.org/docs/ and install poetry using the command line
3. Verify poetry installation by running `poetry --version`
4. In your terminal, navigate to the directory where you saved this code
5. Run `poetry install`
6. Run `poetry shell`
7. Verify you are in the virtual environment by seeing `(.venv)` at the beginning of the terminal command

You can now either run your an input csv file by using a test file and output file name. If you want to use sample files already provided by the repo, run: 

`python3 transformation.py test_files/input/sample.csv test_files/output/output.csv`

If you want to run your own files. You can drop them into the project folder and run the program with this command:

`python3 transformation.py <input_filename.csv> <output_filename.csv>`

Both parameters are required

## Business Requirements


The requirements are as follows:
- The entire CSV is in the UTF-8 character set.
- The `Timestamp` column should be formatted in RFC3339 format.
- The `Timestamp` column should be assumed to be in US/Pacific time; please convert it to US/Eastern.
- All `ZIP` codes should be formatted as 5 digits. If there are less than 5 digits, assume 0 as the prefix.
- The `FullName` column should be converted to uppercase. There will be non-English names.
- The `Address` column should be passed through as is, except for Unicode validation. Please note there are commas in the Address field; your CSV parsing will need to take that into account. Commas will only be present inside a quoted string.
- The `FooDuration` and `BarDuration` columns are in HH:MM:SS.MS format (where MS is milliseconds); please convert them to the total number of seconds.
- The `TotalDuration` column is filled with garbage data. For each row, please replace the value of `TotalDuration` with the sum of `FooDuration` and `BarDuration`.
- The `Notes` column is free form text input by end-users; please do not perform any transformations on this column. If there are invalid UTF-8 characters, please replace them with the Unicode Replacement Character.

Assumptions Given:
- The input document is in UTF-8.
- Invalid characters can be replaced with the Unicode Replacement Character. If that replacement makes data invalid (for example, because it turns a date field into something unparseable), print a warning to `stderr` and drop the row from your output.
- Times that are missing timezone information are in `US/Pacific`.
- The sample data we provide contains all date and time format variants you will need to handle.
- Any type of line endings are permissible in the output.

## Approach

A few tradeoffs considered during development are as follows:

- Parsing the timestamp - Given the assumptions, I coded the solution to strictly follow the sample data timestamp format given and not allow other formats to be in the output file. My thinking was to preserve data integrity, having a stricter criteria would help with that.

- Verifying inputs - I made a few assumptions that I should validate certain characteristics of fields in the csv file. For example, the duration columns shouldn't have alphabetic characters. To verify this I check the input in the beginning and throw an exception if it doesn't meet my assumed criteria. For now, it doesn't attempt to fix the input if it seems straightforward, but just skips the row entirely.

- Comments and doc strings - Usually, I try discuss with the team and other stakeholders about the amount of comments and doc strings needed. I usually air on the side of less comments and focus on code readability without comments, but some people feel different. 

## Future Improvements


- Handling multiple types of timestamp and duration inputs - Currently, it only takes one format and that format alone. If there are other varying formats seen in the test data, more inputs or a flexible library may be added. 
- Environment variables for US/Pacific and US/Eastern to be more easily configurable without having to dig through the code again. 
- The timestamp seems to be given PST or PDT, but it should be standardized as either/or
- More log messages tracking the important information necessary for debugging
- For replacing the non-utf8 characters, it doesn't log that it just modified the data. It should log it for data integrity purposes
