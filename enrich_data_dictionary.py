#!/usr/bin/env python3
"""
Data Dictionary Enrichment Tool

This tool enriches a data dictionary CSV file using an LLM (OpenAI).
For each column, it assigns:
- Group: identifier, numeric, categorical, or datetime
- Description: what the column means
- Confidence Score: how confident the LLM is about the description (0-1)
"""

import os
import sys
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json
import argparse


def load_data_dictionary(csv_path):
    """Load the data dictionary CSV file."""
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)


def create_prompt_for_column(column_name, sample_values=None):
    """Create a prompt for the LLM to classify and describe a column."""
    prompt = f"""Analyze the following data column and provide classification and description.

Column Name: {column_name}
"""
    
    if sample_values:
        prompt += f"Sample Values: {', '.join(str(v) for v in sample_values[:5])}\n"
    
    prompt += """
Please provide a JSON response with the following fields:
1. "group": One of ["identifier", "numeric", "categorical", "datetime"]
   - identifier: unique identifiers like IDs, keys
   - numeric: numerical measurements or quantities
   - categorical: categories, labels, or classifications
   - datetime: dates, times, or timestamps
2. "description": A brief description of what this column represents (1-2 sentences)
3. "confidence": A confidence score between 0 and 1 indicating how confident you are about this classification and description

Respond ONLY with valid JSON in this exact format:
{
  "group": "category_name",
  "description": "column description",
  "confidence": 0.95
}
"""
    return prompt


def enrich_column_with_llm(client, column_name, sample_values=None, model="gpt-3.5-turbo"):
    """Use OpenAI LLM to classify and describe a column."""
    try:
        prompt = create_prompt_for_column(column_name, sample_values)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a data analyst expert who classifies and describes data columns. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        # Remove markdown code blocks if present
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
            result_text = result_text.strip()
        
        result = json.loads(result_text)
        
        # Validate the response structure
        required_fields = ["group", "description", "confidence"]
        if not all(field in result for field in required_fields):
            raise ValueError("Missing required fields in LLM response")
        
        # Validate group value
        valid_groups = ["identifier", "numeric", "categorical", "datetime"]
        if result["group"] not in valid_groups:
            print(f"Warning: Invalid group '{result['group']}' for column '{column_name}'. Defaulting to 'categorical'.")
            result["group"] = "categorical"
        
        # Ensure confidence is between 0 and 1
        result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response for column '{column_name}': {e}")
        # Sanitized error - not showing full response to avoid exposing sensitive data
        return {
            "group": "categorical",
            "description": "Unable to determine description",
            "confidence": 0.0
        }
    except Exception as e:
        print(f"Error processing column '{column_name}': {e}")
        return {
            "group": "categorical",
            "description": "Error occurred during processing",
            "confidence": 0.0
        }


def enrich_data_dictionary(input_csv, output_csv, api_key=None, model="gpt-3.5-turbo", 
                          sample_data_csv=None):
    """
    Enrich a data dictionary CSV with group, description, and confidence.
    
    Args:
        input_csv: Path to input CSV with column names
        output_csv: Path to output enriched CSV
        api_key: OpenAI API key (if None, will use environment variable)
        model: OpenAI model to use
        sample_data_csv: Optional path to actual data CSV for better analysis
    """
    # Load API key
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass via --api-key")
        sys.exit(1)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Load data dictionary
    df = load_data_dictionary(input_csv)
    
    # Load sample data if provided
    sample_data = None
    if sample_data_csv:
        try:
            sample_data = pd.read_csv(sample_data_csv)
            print(f"Loaded sample data from {sample_data_csv}")
        except Exception as e:
            print(f"Warning: Could not load sample data: {e}")
    
    # Determine column name field
    column_field = None
    for possible_name in ['column_name', 'column', 'name', 'field', 'Column Name', 'Column']:
        if possible_name in df.columns:
            column_field = possible_name
            break
    
    if column_field is None:
        # If no column name field, use the first column or all columns as column names
        if len(df.columns) == 0:
            print("Error: No columns found in input CSV")
            sys.exit(1)
        print("Warning: No 'column_name' field found. Using first column as column names.")
        column_field = df.columns[0]
    
    # Add new columns for enriched data
    df['group'] = ''
    df['description'] = ''
    df['confidence'] = 0.0
    
    print(f"Enriching {len(df)} columns using {model}...")
    print("-" * 60)
    
    # Process each column
    for idx, row in df.iterrows():
        column_name = row[column_field]
        print(f"Processing: {column_name}")
        
        # Get sample values if available
        sample_values = None
        if sample_data is not None and column_name in sample_data.columns:
            sample_values = sample_data[column_name].dropna().head(5).tolist()
        
        # Enrich with LLM
        enrichment = enrich_column_with_llm(client, column_name, sample_values, model)
        
        # Update dataframe
        df.at[idx, 'group'] = enrichment['group']
        df.at[idx, 'description'] = enrichment['description']
        df.at[idx, 'confidence'] = enrichment['confidence']
        
        print(f"  → Group: {enrichment['group']}, Confidence: {enrichment['confidence']:.2f}")
    
    # Save enriched data dictionary
    df.to_csv(output_csv, index=False)
    print("-" * 60)
    print(f"Enriched data dictionary saved to: {output_csv}")
    
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Enrich a data dictionary CSV using OpenAI LLM"
    )
    parser.add_argument(
        "input_csv",
        help="Path to input data dictionary CSV file"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Path to output enriched CSV file (default: input_enriched.csv)"
    )
    parser.add_argument(
        "-k", "--api-key",
        default=None,
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)"
    )
    parser.add_argument(
        "-m", "--model",
        default="gpt-3.5-turbo",
        help="OpenAI model to use (default: gpt-3.5-turbo)"
    )
    parser.add_argument(
        "-s", "--sample-data",
        default=None,
        help="Optional path to CSV file with actual data samples for better analysis"
    )
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output is None:
        base_name = os.path.splitext(args.input_csv)[0]
        output_csv = f"{base_name}_enriched.csv"
    else:
        output_csv = args.output
    
    # Run enrichment
    enrich_data_dictionary(
        args.input_csv,
        output_csv,
        api_key=args.api_key,
        model=args.model,
        sample_data_csv=args.sample_data
    )


if __name__ == "__main__":
    main()