# ASU FSE Scholar Scraper

This repository contains two scripts that work together to extract **ASU Fulton Schools of Engineering (FSE) faculty names** and gather their publication data.


## 🛠 Requirements

Install dependencies with:

```bash
make .venv
```

## 1. `extractor.py` — ASU FSE Faculty Extractor

We begin with SCAI (School of Computing and Augmented Intelligence) as our initial target department.
This script scrapes the **ASU SCAI faculty directory** and collects the names of all listed professors.

### **Features**

- Headless Selenium browser for reliable scraping
- Auto-pagination through all directory pages
- Deduplication using a Python set
- Prints the complete list of professors found

### **Usage**

```bash
make extract-faculty
```

### **Output**
```
python -m flordb dataframe name
```

Prints dataframe of faculty and their names.

##  2. `main.py` — Publications Crawler

Crawls the last 10 years of publications for each ASU FSE professor:

1. Searches each name on Google Scholar, DBLP, or Semantic Scholar
2. Opens the first matching profile
3. Checks if the professor is affiliated with **Arizona State University**
4. Scrapes up to 100 papers, including:

   - Title
   - URL
   - Publication year

5. Saves all results to a CSV file.

### **Usage**

```bash
make asu_authors_papers.csv
```
**Output**

A CSV file named:
`asu_authors_papers.csv`

Containing:

| author | title | link | year |
| ------ | ----- | ---- | ---- |



## Miscellaneous
#### `non_affiliate_extractor.py` — Google Scholar Crawler

This script identifies **which professors from the master list did NOT appear in the Google Scholar CSV**, meaning they were either:

- Not found on Google Scholar
- Found but **not ASU-affiliated**
- Or had no retrievable publication data

It outputs a clean CSV containing only the **non-affiliated or missing authors**.

   1. Loads the full list of all expected authors.
   2. Reads the `asu_authors_papers.csv` file.
   3. Compares the two lists.
   4. Saves results to `non_affiliate.csv`.

Run:
```bash
make non_affiliate.csv
```

**Output:** A single-column CSV:

| author |
| ------ |
