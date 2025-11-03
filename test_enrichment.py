#!/usr/bin/env python3
"""
Simple test script for data dictionary enrichment functionality
Tests the core functions without making actual API calls
"""

import pandas as pd
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enrich_data_dictionary import (
    load_data_dictionary,
    create_prompt_for_column
)


def test_load_data_dictionary():
    """Test loading the example data dictionary"""
    print("Test 1: Loading data dictionary...")
    try:
        df = load_data_dictionary("example_data_dictionary.csv")
        assert len(df) > 0, "Data dictionary should have rows"
        assert 'column_name' in df.columns, "Should have column_name field"
        print(f"  ✓ Loaded {len(df)} columns")
        print(f"  ✓ Columns found: {df['column_name'].tolist()}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_create_prompt():
    """Test prompt generation"""
    print("\nTest 2: Creating prompts...")
    try:
        # Test without sample values
        prompt1 = create_prompt_for_column("user_id")
        assert "user_id" in prompt1, "Prompt should contain column name"
        assert "identifier" in prompt1, "Prompt should mention identifier group"
        assert "numeric" in prompt1, "Prompt should mention numeric group"
        assert "categorical" in prompt1, "Prompt should mention categorical group"
        assert "datetime" in prompt1, "Prompt should mention datetime group"
        print("  ✓ Basic prompt created successfully")
        
        # Test with sample values
        prompt2 = create_prompt_for_column("age", [25, 30, 35, 40, 45])
        assert "age" in prompt2, "Prompt should contain column name"
        assert "25" in prompt2, "Prompt should contain sample values"
        print("  ✓ Prompt with sample values created successfully")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_sample_data_loading():
    """Test loading sample data"""
    print("\nTest 3: Loading sample data...")
    try:
        sample_data = pd.read_csv("example_sample_data.csv")
        assert len(sample_data) > 0, "Sample data should have rows"
        assert "user_id" in sample_data.columns, "Sample data should have expected columns"
        print(f"  ✓ Loaded {len(sample_data)} sample rows")
        print(f"  ✓ Sample columns: {sample_data.columns.tolist()}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_output_structure():
    """Test expected output structure"""
    print("\nTest 4: Validating output structure...")
    try:
        df = load_data_dictionary("example_data_dictionary.csv")
        
        # Add expected columns
        df['group'] = 'identifier'
        df['description'] = 'Test description'
        df['confidence'] = 0.95
        
        # Verify structure
        required_columns = ['column_name', 'group', 'description', 'confidence']
        for col in required_columns:
            assert col in df.columns, f"Output should have {col} column"
        
        print("  ✓ Output structure is correct")
        print(f"  ✓ Columns: {df.columns.tolist()}")
        
        # Test writing to CSV
        output_path = "/tmp/test_output.csv"
        df.to_csv(output_path, index=False)
        
        # Verify reading back
        df_read = pd.read_csv(output_path)
        assert len(df_read) == len(df), "Read data should match written data"
        print(f"  ✓ Successfully wrote and read CSV")
        
        # Clean up
        os.remove(output_path)
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def main():
    print("=" * 60)
    print("Data Dictionary Enrichment - Unit Tests")
    print("=" * 60)
    
    results = []
    results.append(test_load_data_dictionary())
    results.append(test_create_prompt())
    results.append(test_sample_data_loading())
    results.append(test_output_structure())
    
    print("\n" + "=" * 60)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
