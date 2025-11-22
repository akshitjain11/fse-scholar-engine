import csv


INPUT_CSV = "asu_authors_papers.csv"
OUTPUT_CSV = "non_affiliate.csv"

# Given list of all 60 authors
ALL_AUTHORS = [
    "Yezhou Yang", "Adam Doupé", "Adil Ahmad", "Aman Arora", "Andrea Richa", "Ariane Middel",
    "Arunabha Sen", "Aviral Shrivastava", "Bing Si", "Chitta Baral", "Chris Bryan",
    "Dimitri Bertsekas", "Douglas Montgomery", "Feng Ju", "Fish Wang", "Gail-Joon Ahn",
    "George Runger", "Geunyeong Byeon", "Giulia Pedrielli", "Guoliang Xue", "Hani Ben Amor",
    "Hao Yan", "Hasan Davulcu", "Hessam Sarjoughian", "Huan Liu", "James Collofello",
    "Jedidiah Crandall", "Joshua Daymude", "K. Selcuk Candan", "Kevin Gary", "Lacy Greening",
    "Michel Kinsy", "Ming Zhao", "Nakul Gopalan", "Paul Grogan", "Rakibul Hasan", "Rida Bazzi",
    "Robert Atkinson", "Rong Pan", "Ross Maciejewski", "Sandeep Gupta", "Sarma Vrudhula",
    "Sethuraman Panchanathan", "Siddharth Srivastava", "Srividya Bansal", "Stephanie Forrest",
    "Stephen Yau", "Subbarao Kambhampati", "Ted Pavlic", "Teresa Wu", "Tiffany Bao",
    "Violet Syrotiuk", "Vivek Gupta", "Xusheng Xiao", "Yalin Wang", "Yan Shoshitaishvili",
    "Yanjie Fu", "YooJung Choi", "Yu Zhang", "Zhichao Cao"
]

def extract_csv_authors(csv_path):
    """Extract all unique author names from the CSV."""
    authors = set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("author", "").strip()
            if name:
                authors.add(name)
    return authors

def find_non_affiliates(all_authors, affiliated_authors):
    """Return authors not found in the CSV (non-affiliates)."""
    return sorted(set(all_authors) - set(affiliated_authors))

def save_to_csv(authors, filename):
    """Save non-affiliates to CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["author"])
        for name in authors:
            writer.writerow([name])
    print(f"💾 Saved {len(authors)} non-affiliated authors to {filename}")

if __name__ == "__main__":
    affiliated_authors = extract_csv_authors(INPUT_CSV)
    print(f"✅ Found {len(affiliated_authors)} authors in {INPUT_CSV}")

    non_affiliates = find_non_affiliates(ALL_AUTHORS, affiliated_authors)
    print(f"🚫 Non-affiliated authors: {len(non_affiliates)}")

    save_to_csv(non_affiliates, OUTPUT_CSV)
