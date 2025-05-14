#!/usr/bin/env python
# coding: utf-8

"""
Convert Excel data file to DDF format.
This script converts the calculated_datapoints.xlsx file containing
TradAgg and SurvSAgg values into DDF format files.
After running this script, use 'validate-ddf-ng -p' in the project root
to validate and update the datapackage.json file.
"""

import os
import re
import pandas as pd
from pathlib import Path

# File paths
EXCEL_FILE = "../source/calculated_datapoints.xlsx"
OUTPUT_DIR = "../../"  # Root of the DDF dataset
CONCEPTS_FILE = os.path.join(OUTPUT_DIR, "ddf--concepts.csv")
ENTITIES_FILE = os.path.join(OUTPUT_DIR, "ddf--entities--geo--country.csv")
TRADAGG_FILE = os.path.join(OUTPUT_DIR, "ddf--datapoints--tradagg--by--geo--year.csv")
SURVSAGG_FILE = os.path.join(OUTPUT_DIR, "ddf--datapoints--survsagg--by--geo--year.csv")

def extract_country_year(country_year_str):
    """Extract country name and year from combined string."""
    pattern = r"(.*)\s*\((\d{4})\)"
    match = re.match(pattern, country_year_str)
    if match:
        country = match.group(1).strip()
        year = match.group(2)
        return country, int(year)
    return None, None

def country_to_code(country_name):
    """Convert country name to lowercase code."""
    # Simple conversion - remove spaces, commas, dots, lowercase
    # In a real implementation, you might use a more comprehensive mapping
    return country_name.lower().replace(" ", "_").replace(",", "").replace(".", "").replace("__", "_")

def update_concepts_file():
    """Update the concepts file with new indicators."""
    # Read existing concepts file
    try:
        concepts_df = pd.read_csv(CONCEPTS_FILE)
    except:
        # If file doesn't exist or is empty, create a new dataframe
        concepts_df = pd.DataFrame(columns=["concept", "concept_type", "name", "domain"])

    # Check if our indicators already exist
    new_concepts = []
    if "tradagg" not in concepts_df["concept"].values:
        new_concepts.append({
            "concept": "tradagg",
            "concept_type": "measure",
            "name": "Traditional vs Rational Values"
        })
    if "survsagg" not in concepts_df["concept"].values:
        new_concepts.append({
            "concept": "survsagg",
            "concept_type": "measure",
            "name": "Survival vs Self-Expression Values"
        })
    if "geo" not in concepts_df["concept"].values:
        new_concepts.append({
            "concept": "geo",
            "concept_type": "entity_domain",
            "name": "Geography"
        })
    if "country" not in concepts_df["concept"].values:
        new_concepts.append({
            "concept": "country",
            "concept_type": "entity_set",
            "name": "Country",
            "domain": "geo"
        })
    if "name" not in concepts_df["concept"].values:
        new_concepts.append({
            "concept": "name",
            "concept_type": "string",
            "name": "Name"
        })
    if "year" not in concepts_df["concept"].values:
        new_concepts.append({
            "concept": "year",
            "concept_type": "time",
            "name": "Year"
        })
    if "domain" not in concepts_df["concept"].values:
        new_concepts.append({
            "concept": "domain",
            "concept_type": "string",
            "name": "Domain"
        })

    # Add new concepts if needed
    if new_concepts:
        new_df = pd.DataFrame(new_concepts)
        concepts_df = pd.concat([concepts_df, new_df], ignore_index=True)

    # Update existing 'country' concept if it exists but doesn't have domain
    if 'country' in concepts_df['concept'].values:
        country_idx = concepts_df[concepts_df['concept'] == 'country'].index
        if 'domain' not in concepts_df.columns:
            concepts_df['domain'] = None
        concepts_df.loc[country_idx, 'concept_type'] = 'entity_set'
        concepts_df.loc[country_idx, 'domain'] = 'geo'

    # Save updated concepts file
    concepts_df.to_csv(CONCEPTS_FILE, index=False)
    print(f"Updated concepts file: {CONCEPTS_FILE}")

def main():
    """Main function to convert Excel to DDF format."""
    print("Converting Excel data to DDF format...")

    # Read Excel file
    try:
        # Skip the first two rows (header and "Mean" row)
        df = pd.read_excel(EXCEL_FILE, skiprows=2)
        print(f"Read {len(df)} rows from Excel file")

        # Skip the last row if it's a summary
        if "Total" in str(df.iloc[-1, 0]) or "Mean" in str(df.iloc[-1, 0]):
            df = df.iloc[:-1]
            print("Skipped summary row")

        # Extract data from the first three columns
        data = df.iloc[:, 0:3]
        data.columns = ["Country_Year", "TradAgg", "SurvSAgg"]
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Process the data
    countries = {}
    tradagg_data = []
    survsagg_data = []

    for _, row in data.iterrows():
        country_name, year = extract_country_year(row["Country_Year"])
        if country_name and year:
            country_code = country_to_code(country_name)

            # Store unique countries
            countries[country_code] = country_name

            # Store datapoints
            if not pd.isna(row["TradAgg"]):
                tradagg_data.append({
                    "geo": country_code,
                    "year": year,
                    "tradagg": row["TradAgg"]
                })

            if not pd.isna(row["SurvSAgg"]):
                survsagg_data.append({
                    "geo": country_code,
                    "year": year,
                    "survsagg": row["SurvSAgg"]
                })

    # Update concepts file
    update_concepts_file()

    # Create entities file
    entities_df = pd.DataFrame([
        {"country": code, "name": name}
        for code, name in countries.items()
    ])
    entities_df.to_csv(ENTITIES_FILE, index=False)
    print(f"Created entities file with {len(entities_df)} countries")

    # Create datapoints files
    tradagg_df = pd.DataFrame(tradagg_data)
    tradagg_df.to_csv(TRADAGG_FILE, index=False)
    print(f"Created tradagg datapoints file with {len(tradagg_df)} rows")

    survsagg_df = pd.DataFrame(survsagg_data)
    survsagg_df.to_csv(SURVSAGG_FILE, index=False)
    print(f"Created survsagg datapoints file with {len(survsagg_df)} rows")

    print("Conversion completed successfully!")
    print("Now run 'validate-ddf-ng -p' in the project root to validate and update the datapackage.json")

if __name__ == "__main__":
    main()
