import pandas as pd
from sqlalchemy import create_engine
import os

print("Running SQL Analysis Queries...\n")

# Connect to database
engine = create_engine('sqlite:///data/academic_performance.db')

# Create export directory
os.makedirs('data/exports', exist_ok=True)

# Read SQL file
with open('sql/02_analysis_queries.sql', 'r') as f:
    sql_content = f.read()

# Split queries
queries = sql_content.split('-- QUERY')
queries = [q for q in queries if 'SELECT' in q.upper()]

results = {}

for i, query_block in enumerate(queries, 1):
    lines = query_block.strip().split('\n')
    query_name = lines[0].replace(':', '').strip() if lines else f"Query {i}"
    
    # Extract SQL
    sql_lines = [line for line in lines[1:] if not line.strip().startswith('--')]
    sql_query = '\n'.join(sql_lines).strip()
    
    if not sql_query:
        continue
    
    try:
        print(f"\n{'='*60}")
        print(f"QUERY {i}: {query_name}")
        print(f"{'='*60}")
        
        df = pd.read_sql(sql_query, engine)
        
        print(df.to_string(index=False))
        print(f"\nRows returned: {len(df)}")
        
        # Save to CSV
        safe_name = query_name.lower().replace(' ', '_').replace('/', '_')
        output_file = f"data/exports/query_{i:02d}_{safe_name}.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved to: {output_file}")
        
        results[query_name] = df
        
    except Exception as e:
        print(f"Error in {query_name}: {str(e)}")

print(f"\n{'='*60}")
print(f"SQL ANALYSIS COMPLETE")
print(f"{'='*60}")
print(f"\nTotal queries executed: {len(results)}")
print(f"Results saved to: data/exports/")