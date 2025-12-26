# Cook County Foreclosure Intelligence Pipeline

An end-to-end, multi-phase automation system that scrapes, enriches, OCR-processes, and analyzes Cook County foreclosure records.

This pipeline is designed for **real estate investors, analysts, researchers, and automation engineers** who need structured, decision-ready foreclosure intelligence from public records.

---

## 🔹 Pipeline Overview

| Phase | Script | Purpose |
|-----|------|-------|
| Phase 1 | `phase1_scraper.py` | Scrapes LIS PENDENS foreclosure filings |
| Phase 2 | `phase2_scraper.py` | Visits each filing, extracts metadata, downloads PDFs |
| Phase 3 | `phase3_results.py` | OCR + case number, amount, address extraction |
| Phase 4 | `phase4_results.py` | Court status verification & case classification |

---

## 📂 Folder Structure

```text
project-root/
│
├── phase1_scraper.py
├── phase2_scraper.py
├── phase3_results.py
├── phase4_results.py
│
├── pdf/                # Phase 2 downloaded PDFs
├── pdfs/               # Phase 3 OCR source PDFs
│
├── phase1_results.csv
├── phase2_results.csv
├── phase3_results.csv
├── phase4_results.csv
│
├── phase1_results.json
├── phase2_results.json
├── phase3_results.json
├── phase4_results.json
│
├── requirements.txt
└── README.md

⚙️ Environment Setup

1️⃣ Python

python --version
# Python 3.9 – 3.11 recommended

2️⃣ Install Python Dependencies

pip install -r requirements.txt

3️⃣ Install Playwright Browsers

playwright install chromium

4️⃣ Install Tesseract OCR

Windows

Download installer: https://github.com/UB-Mannheim/tesseract/wiki

Add to PATH

Mac = brew install tesseract poppler

LINUX = sudo apt install tesseract-ocr poppler-utils

🚀 How To Run (CLI)
▶ Phase 1 – Scrape Foreclosure Filings

python phase1_scraper.py


Supports manual date range or automated month-by-month scraping

Outputs:

phase1_results.csv

phase1_results.json

▶ Phase 2 – Visit Filings & Download PDFs

python phase2_scraper.py

Extracts document metadata

Downloads foreclosure PDFs

Outputs:

phase2_results.csv

phase2_results.json

/pdf/ folder


▶ Phase 3 – OCR & Data Extraction

python phase3_results.py

OCR with watermark handling

Extracts:

Case Number

Dollar Amount

Property Address

Outputs:

phase3_results.csv

phase3_results.json

▶ Phase 4 – Court Case Status Verification

python phase4_results.py

Searches Cook County Clerk of Court

Classifies cases as:

GREEN – Judgment of Foreclosure

RED – Excluded / Disposed / Sale-related

NEUTRAL – No judgment found

Outputs:

phase4_results.csv

phase4_results.json


🧠 Key Features

✅ Human-like Playwright automation

✅ Anti-bot evasion (UA + viewport rotation)

✅ Resume-safe (no duplicate processing)

✅ OCR optimized for watermarked court PDFs

✅ Structured CSV + JSON outputs

✅ Designed for automation & scaling


⚠️ Legal & Ethical Notice

This project uses publicly accessible government websites.

You are responsible for:

Respecting website terms
Throttling requests
Using results ethically and legally