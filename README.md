# ASU FSE Scholar Scraper

This repository contains two scripts that work together to extract **ASU SCAI faculty names** and gather their **Google Scholar publication data**.

---

## 📌 1. `extractor.py` — ASU SCAI Faculty Extractor

This script scrapes the **ASU SCAI faculty directory** and collects the names of all listed professors.

### **Features**

- Headless Selenium browser for reliable scraping
- Auto-pagination through all directory pages
- Deduplication using a Python set
- Prints the complete list of professors found

### **Usage**

```bash
python extractor.py
```

### **Output**

Prints the total number of faculty and their names.

---

## 📌 2. `main.py` — Google Scholar Crawler

This script takes a list of professor names and:

1. Searches each name on Google Scholar
2. Opens the first matching profile
3. Checks if the professor is affiliated with **Arizona State University**
4. Scrapes up to 100 papers, including:

   - Title
   - URL
   - Publication year

5. Saves all results to a CSV file.

### **Usage**

```bash
python main.py
```

### **Output**

A CSV file named:

```
asu_authors_papers.csv
```

Containing:

| author | title | link | year |
| ------ | ----- | ---- | ---- |

---

## 🛠 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## 📌 3. `non_affiliate_extractor.py` — Google Scholar Crawler

This script identifies **which professors from the master list did NOT appear in the Google Scholar CSV**, meaning they were either:

- Not found on Google Scholar
- Found but **not ASU-affiliated**
- Or had no retrievable publication data

It outputs a clean CSV containing only the **non-affiliated or missing authors**.

---

## 📌 What the Script Does

### **1. Loads the full list of 60 SCAI faculty**

These represent all expected authors.

### **2. Reads `asu_authors_papers.csv`**

This file contains authors whose Scholar profiles _were found_ and confirmed to be **ASU-affiliated**.

### **3. Compares the two lists**

Any author missing from the CSV is labeled as **non-affiliate**.

### **4. Saves results to `non_affiliate.csv`**

A single-column CSV:

\`\`\`
author
John Doe
Jane Smith
...
\`\`\`

---

## 🧠 Functions Overview

### \`extract_csv_authors(csv_path)\`

Reads the Scholar CSV and extracts all unique author names.

### \`find_non_affiliates(all_authors, affiliated_authors)\`

Computes the set difference → authors not found in the CSV.

### \`save_to_csv(authors, filename)\`

Writes all non-affiliated authors to a clean CSV file.

---

## 🚀 Usage

Run the script:

\`\`\`bash
python non_affiliate_extractor.py
\`\`\`

---

## 📦 Output Files

| File                       | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| \`asu_authors_papers.csv\` | Input file containing confirmed ASU-affiliated authors  |
| \`non_affiliate.csv\`      | Output file containing missing / non-affiliated authors |

---
