# UG-GOV-SEC-SCH
Uganda Government secondary schools data.

## Overview
This repository contains a comprehensive dataset of all Government Secondary Schools in Uganda, extracted from the official PDF document and structured as a JSON dataset.

## Dataset Files
- `Government-Secondary.pdf` - Original PDF document containing school data
- `uganda_schools_dataset.json` - Structured JSON dataset with all school information
- `extract_pdf_data.py` - Python script used to extract data from PDF

## Dataset Structure
The JSON dataset is organized in the following format:
```json
{
    "uganda": {
        "description": "Dataset description",
        "total_districts": "113",
        "districts": {
            "DISTRICT_NAME": [
                {
                    "name": "School Name",
                    "emis": "EMIS Code"
                }
            ]
        }
    }
}
```

## Dataset Statistics
- **Total Districts**: 113
- **Total Schools**: 1,033
- **Schools with EMIS codes**: 1,011
- **Schools without EMIS codes**: 22

## Usage

### Loading the Dataset
```python
import json

# Load the dataset
with open('uganda_schools_dataset.json', 'r') as f:
    data = json.load(f)

# Access district data
districts = data['uganda']['districts']

# Get schools from a specific district
kampala_schools = districts['KAMPALA']
for school in kampala_schools:
    print(f"{school['name']} - EMIS: {school['emis']}")
```

### Re-generating the Dataset
To re-extract data from the PDF:
```bash
python3 extract_pdf_data.py
```

Requirements:
- Python 3.x
- pdfplumber library (`pip install pdfplumber`)

## Notes
- Some schools (22 total) do not have EMIS codes in the original PDF. These schools have empty EMIS values in the dataset.
- EMIS (Education Management Information System) codes are unique identifiers for educational institutions in Uganda.
- The data is organized alphabetically by district name.
