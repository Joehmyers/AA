# Usage Guide

## Quick Start

1. **Set up your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   # Or create a .env file:
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

2. **Run the enrichment tool:**
   ```bash
   python enrich_data_dictionary.py example_data_dictionary.csv
   ```

3. **View the results:**
   The enriched data dictionary will be saved as `example_data_dictionary_enriched.csv`

## Common Use Cases

### Case 1: Basic Enrichment (Column Names Only)

If you only have a list of column names:

```bash
python enrich_data_dictionary.py my_columns.csv
```

**Input CSV format:**
```csv
column_name
user_id
email
purchase_date
total_amount
```

### Case 2: Enrichment with Sample Data

For better accuracy, provide sample data:

```bash
python enrich_data_dictionary.py my_columns.csv \
  --sample-data my_actual_data.csv
```

The tool will analyze actual values to make better classifications.

### Case 3: Custom Output Path

Specify where to save the enriched data:

```bash
python enrich_data_dictionary.py my_columns.csv \
  --output enriched/my_data_dictionary.csv
```

### Case 4: Using GPT-4 for Higher Accuracy

Use a more powerful model:

```bash
python enrich_data_dictionary.py my_columns.csv \
  --model gpt-4
```

Note: GPT-4 is more expensive but provides better accuracy for complex columns.

### Case 5: API Key as Command Line Argument

Pass the API key directly (useful for scripts/CI):

```bash
python enrich_data_dictionary.py my_columns.csv \
  --api-key sk-your-api-key-here
```

## Understanding the Output

The tool adds three columns to your data dictionary:

### 1. Group (Column Type)

- **identifier**: Unique IDs, keys, or codes
  - Examples: user_id, order_number, sku, uuid
  
- **numeric**: Numbers representing measurements or quantities
  - Examples: age, price, count, revenue, temperature
  
- **categorical**: Categories, labels, or discrete values
  - Examples: status, country, product_type, color
  
- **datetime**: Date and time information
  - Examples: created_at, birth_date, timestamp, month

### 2. Description

A human-readable explanation of what the column represents, typically 1-2 sentences.

Example:
- Column: `total_revenue`
- Description: "The total revenue generated from all transactions in the specified period, calculated in USD."

### 3. Confidence Score

A value between 0 and 1 indicating how confident the LLM is about its classification and description:

- **0.9-1.0**: Very high confidence
- **0.7-0.9**: Good confidence
- **0.5-0.7**: Moderate confidence (review recommended)
- **0.0-0.5**: Low confidence (manual review needed)

## Example Output

```csv
column_name,group,description,confidence
user_id,identifier,"Unique identifier for each user in the system",0.95
first_name,categorical,"User's first name",0.90
email,identifier,"User's email address used for communication and login",0.92
age,numeric,"User's age in years",0.88
signup_date,datetime,"Date when the user registered their account",0.95
account_type,categorical,"Type or tier of user account (e.g., basic, premium)",0.85
is_active,categorical,"Boolean flag indicating whether the user account is currently active",0.93
last_login,datetime,"Timestamp of the user's most recent login to the system",0.94
purchase_count,numeric,"Total number of purchases made by the user",0.91
```

## Tips for Best Results

1. **Use descriptive column names**: Better names lead to better classifications
   - Good: `customer_email`, `order_date`, `total_price`
   - Less ideal: `col1`, `data`, `field`

2. **Provide sample data when possible**: The tool can analyze actual values for more accurate classification

3. **Review low confidence scores**: Manually verify classifications with confidence < 0.7

4. **Use GPT-4 for complex domains**: If your data has specialized terminology, GPT-4 may perform better

5. **Batch processing**: The tool processes all columns in one run, no need to process individually

## Troubleshooting

### Error: "OpenAI API key not found"

Make sure you've set the `OPENAI_API_KEY` environment variable or passed it via `--api-key`.

### Error: "No 'column_name' field found"

Your CSV should have a column containing the column names. Accepted field names:
- `column_name`
- `column`
- `name`
- `field`

Or the tool will use the first column by default.

### Low confidence scores

Try:
- Providing sample data with `--sample-data`
- Using a more powerful model with `--model gpt-4`
- Improving column names to be more descriptive

### Rate limiting errors

If you hit OpenAI rate limits:
- Wait a few minutes between runs
- Upgrade your OpenAI API plan
- Process smaller batches

## Cost Estimation

Approximate costs using GPT-3.5-turbo (as of 2024):
- ~$0.001-0.002 per column
- 100 columns: ~$0.10-0.20
- 1000 columns: ~$1-2

GPT-4 costs approximately 10-30x more.

## Integration with Other Tools

### Use in Python Scripts

```python
from enrich_data_dictionary import enrich_data_dictionary

# Enrich programmatically
df = enrich_data_dictionary(
    input_csv="my_data.csv",
    output_csv="enriched.csv",
    api_key="your-key",
    model="gpt-3.5-turbo",
    sample_data_csv="sample_data.csv"
)
```

### Use in Data Pipelines

```bash
# In a bash script
#!/bin/bash
python enrich_data_dictionary.py raw_columns.csv \
  --output pipeline/enriched_dict.csv \
  --sample-data pipeline/sample_data.csv
```

### CI/CD Integration

```yaml
# In GitHub Actions or similar
- name: Enrich Data Dictionary
  run: |
    python enrich_data_dictionary.py data_dict.csv \
      --api-key ${{ secrets.OPENAI_API_KEY }}
```
