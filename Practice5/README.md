# Practice 5: Python Regular Expressions (RegEx)

## Objective

This practice focuses on mastering regular expressions in Python. You will learn to search, match, find, and replace text patterns using Python's `re` module. Practical exercises include parsing receipt data from the provided `raw.txt` file.

## Tasks

### 2.1 Learn Python RegEx from W3Schools

Read and complete exercises from [W3Schools Python Tutorial](https://www.w3schools.com/python/python_regex.asp).

**Topics to Cover:**
- RegEx Introduction
- RegEx Syntax and Metacharacters (., *, +, ?, ^, $, |, [], ())
- Special Sequences (\d, \w, \s, \D, \W, \S, \A, \Z)
- Sets and Character Classes
- Quantifiers ({n}, {n,}, {n,m})
- `re.search()` - Find first match
- `re.findall()` - Find all matches
- `re.split()` - Split strings
- `re.sub()` - Replace patterns
- `re.match()` - Match at beginning
- Flags (re.IGNORECASE, re.MULTILINE, etc.)

### 2.2 Practical Exercise: Receipt Parsing

Use the provided `raw.txt` file in this folder to practice receipt parsing.

**Tasks:**
1. Extract all prices from the receipt
2. Find all product names
3. Calculate total amount
4. Extract date and time information
5. Find payment method
6. Create a structured output (JSON or formatted text)

**Implementation:**
- Create a `receipt_parser.py` file
- Use appropriate regex patterns to extract data
- Handle various formatting edge cases
- Output parsed data in a readable format

### 2.3 RegEx Exercises (regex.md)

Complete the 10 Python RegEx exercises from `regex.md`. Solutions are in `regex_solutions.py`.

### 2.4 Save Examples to GitHub

**Repository Structure for Practice5:**
- `receipt_parser.py` - Receipt parsing implementation
- `raw.txt` - Sample receipt data
- `regex_solutions.py` - RegEx exercise solutions
- `regex.md` - RegEx exercise list
- `README.md` - This file

**Commit Instructions:**
```bash
git add .
git commit -m "Add Practice5 - Python RegEx and receipt parsing examples"
git push origin main
```

## How to Run

From the repository root:

```bash
# Run receipt parser
python3 Practice5/receipt_parser.py

# Run RegEx solutions
python3 Practice5/regex_solutions.py
```

## What You Must Complete

- [x] Complete all RegEx sections from W3Schools
- [x] Create examples for each regex function (search, findall, split, sub)
- [x] Demonstrate metacharacters, special sequences, and quantifiers
- [x] Complete the receipt parsing exercise using `raw.txt`
- [x] Extract and display all required information from receipts
- [ ] Push all code to GitHub with clear commit messages
- [ ] Deadline: check MS Teams announcements
