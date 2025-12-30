#!/usr/bin/env python3
"""
Script to extract Uganda Government Secondary Schools data from PDF
and create a structured JSON dataset.
"""

import pdfplumber
import json
from collections import defaultdict


def extract_schools_from_pdf(pdf_path):
    """
    Extract school data from the PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with district names as keys and list of schools as values
    """
    districts_data = defaultdict(list)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            
            for line in lines:
                # Skip header lines and empty lines
                if not line.strip():
                    continue
                if 'School District EMIS' in line:
                    continue
                if line.strip().startswith('SN'):
                    continue
                if 'Government Secondary Schools' in line:
                    continue
                
                # Parse the line: SN SCHOOL_NAME DISTRICT [EMIS_CODE]
                parts = line.strip().split()
                
                # We need at least: serial number, school name (1+ words), district
                # EMIS code is optional in the PDF
                if len(parts) >= 3 and parts[0].isdigit():
                    try:
                        # Check if last part is numeric (EMIS code)
                        if parts[-1].isdigit():
                            # Format: SN SCHOOL_NAME DISTRICT EMIS_CODE
                            emis_code = parts[-1]
                            district = parts[-2]
                            school_name = ' '.join(parts[1:-2])
                        else:
                            # Format: SN SCHOOL_NAME DISTRICT (no EMIS code)
                            emis_code = ""
                            district = parts[-1]
                            school_name = ' '.join(parts[1:-1])
                        
                        # Only add if we have valid data
                        if school_name and district:
                            school_entry = {
                                "name": school_name,
                                "emis": emis_code
                            }
                            
                            districts_data[district].append(school_entry)
                            
                    except Exception as e:
                        print(f"Warning: Could not process line: {line}")
                        print(f"Error: {e}")
    
    return districts_data


def create_json_dataset(districts_data, output_path):
    """
    Create the final JSON dataset in the required format.
    
    Args:
        districts_data: Dictionary with district data
        output_path: Path where JSON file should be saved
    """
    # Create the final structure
    dataset = {
        "uganda": {
            "description": "This dataset contains information about all Government Secondary Schools in Uganda, organized by district. The data includes school names and their corresponding EMIS (Education Management Information System) codes, which are unique identifiers for educational institutions in Uganda.",
            "total_districts": str(len(districts_data)),
            "districts": {}
        }
    }
    
    # Add all districts and their schools
    for district, schools in sorted(districts_data.items()):
        dataset["uganda"]["districts"][district] = schools
    
    # Write to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
    
    return dataset


def main():
    """Main execution function."""
    pdf_path = 'Government-Secondary.pdf'
    output_path = 'uganda_schools_dataset.json'
    
    print("Extracting data from PDF...")
    districts_data = extract_schools_from_pdf(pdf_path)
    
    # Calculate statistics
    total_schools = sum(len(schools) for schools in districts_data.values())
    
    print(f"\nExtraction complete!")
    print(f"Total districts: {len(districts_data)}")
    print(f"Total schools: {total_schools}")
    
    print(f"\nCreating JSON dataset...")
    dataset = create_json_dataset(districts_data, output_path)
    
    print(f"JSON dataset created successfully: {output_path}")
    print(f"\nSample districts: {', '.join(sorted(districts_data.keys())[:5])}")
    
    # Display a sample
    first_district = sorted(districts_data.keys())[0]
    print(f"\nSample data from {first_district} district:")
    for school in districts_data[first_district][:3]:
        print(f"  - {school['name']} (EMIS: {school['emis']})")


if __name__ == "__main__":
    main()
