# AA - Data Dictionary Enrichment Tool

A Python tool that enriches data dictionary CSV files using OpenAI's LLM. For each column in your data dictionary, the tool automatically assigns:

- **Group**: Classification as `identifier`, `numeric`, `categorical`, or `datetime`
- **Description**: A clear explanation of what the column represents
- **Confidence Score**: A score (0-1) indicating the LLM's confidence in its analysis

## Features

- 🤖 Leverages OpenAI's LLM for intelligent column analysis
- 📊 Supports multiple data types: identifiers, numeric, categorical, and datetime
- 📈 Provides confidence scores for quality assessment
- 🔍 Can use actual data samples for more accurate classification
- 🎯 Simple CSV input/output format
- ⚙️ Configurable model selection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Joehmyers/AA.git
cd AA
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Usage

Enrich a data dictionary with just column names:

```bash
python enrich_data_dictionary.py example_data_dictionary.csv
```

This will create an enriched file: `example_data_dictionary_enriched.csv`

### With Sample Data

For better accuracy, provide a CSV file with actual data samples:

```bash
python enrich_data_dictionary.py example_data_dictionary.csv \
  --sample-data example_sample_data.csv \
  --output enriched_output.csv
```

### With Custom Model

Use a different OpenAI model:

```bash
python enrich_data_dictionary.py example_data_dictionary.csv \
  --model gpt-4 \
  --api-key your_api_key_here
```

### Command-Line Options

```
usage: enrich_data_dictionary.py [-h] [-o OUTPUT] [-k API_KEY] [-m MODEL] 
                                  [-s SAMPLE_DATA] input_csv

positional arguments:
  input_csv             Path to input data dictionary CSV file

optional arguments:
  -h, --help           show this help message and exit
  -o OUTPUT, --output OUTPUT
                       Path to output enriched CSV file (default: input_enriched.csv)
  -k API_KEY, --api-key API_KEY
                       OpenAI API key (or set OPENAI_API_KEY environment variable)
  -m MODEL, --model MODEL
                       OpenAI model to use (default: gpt-3.5-turbo)
  -s SAMPLE_DATA, --sample-data SAMPLE_DATA
                       Optional path to CSV file with actual data samples for better analysis
```

## Input Format

Your data dictionary CSV should have at least one column with column names. The tool looks for common column name fields like:
- `column_name`
- `column`
- `name`
- `field`

Example input (`example_data_dictionary.csv`):
```csv
column_name
user_id
first_name
last_name
email
age
signup_date
account_type
```

## Output Format

The tool adds three new columns to your data dictionary:

Example output:
```csv
column_name,group,description,confidence
user_id,identifier,"Unique identifier for each user in the system",0.95
first_name,categorical,"User's first name",0.90
email,identifier,"User's email address used for communication and login",0.92
age,numeric,"User's age in years",0.88
signup_date,datetime,"Date when the user registered their account",0.95
account_type,categorical,"Type or tier of user account (e.g., basic, premium)",0.85
```

## Column Groups

The tool classifies columns into four groups:

1. **identifier**: Unique identifiers like IDs, keys, or unique codes
2. **numeric**: Numerical measurements, quantities, counts, or metrics
3. **categorical**: Categories, labels, classifications, or discrete values
4. **datetime**: Dates, times, timestamps, or temporal information

## Examples

The repository includes example files:

- `example_data_dictionary.csv` - Sample data dictionary with column names
- `example_sample_data.csv` - Sample actual data for better analysis

Try the examples:
```bash
# Basic enrichment
python enrich_data_dictionary.py example_data_dictionary.csv

# With sample data
python enrich_data_dictionary.py example_data_dictionary.csv \
  --sample-data example_sample_data.csv
```

## Configuration

### Environment Variables

Set your OpenAI API key in `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Model Selection

Supported models include:
- `gpt-3.5-turbo` (default, cost-effective)
- `gpt-4` (more accurate, higher cost)
- `gpt-4-turbo-preview`
- Other OpenAI chat models

## Requirements

- Python 3.7+
- OpenAI API key
- Dependencies listed in `requirements.txt`:
  - openai >= 1.0.0
  - pandas >= 2.0.0
  - python-dotenv >= 1.0.0

## Error Handling

The tool includes robust error handling for:
- Missing API keys
- Invalid CSV formats
- LLM response parsing errors
- Network connectivity issues

If an error occurs for a specific column, it will be assigned default values and the process will continue.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.