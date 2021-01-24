import os
import re
import json
from google.cloud import bigquery

def update_null_value(obj, key):
    if obj[key] == "null":
        obj[key] = None
    return obj

def clean_json(date, file, j_content):
    for line in file:
        obj = json.loads(line)
        
        # create date field
        obj['date'] = date
        # remove unique key
        obj.pop('unique_key', None)
        # transform "null" into null
        obj = update_null_value(obj, 'latitude')
        obj = update_null_value(obj, 'longitude')
        obj = update_null_value(obj, 'location')
        j_content.append(obj)

def write_ndjson(table_json):
    result = [json.dumps(record) for record in table_json]
    with open('output.ndjson', 'w') as out:
        out.write('\n'.join(result))

def main():
    input_date = input('Data no formato AAAA-MM-DD: ')

    # Construct a BigQuery client object.
    bq_client = bigquery.Client()

    # Big query table ID
    table_id = f"bi-psel.danilo_teo.austin_incidents_{input_date}"

    # temp folder to keep GCS data
    temp_folder = "./data"
    download_cmd = f"gsutil -m cp -r gs://arquivei-austin-incidents/{input_date} {temp_folder}"
    os.system(download_cmd)


    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Descript", "STRING"),
            bigquery.SchemaField("Date", "DATE"),
            bigquery.SchemaField("Time", "TIME"),
            bigquery.SchemaField("Address", "STRING"),
            bigquery.SchemaField("Longitude", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("Latitude", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("Location", "STRING"),
            bigquery.SchemaField("Timestamp", "TIMESTAMP"),
        ],
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )



    file_name = "incidents.ndjson"
    regex = r"\d{4}\-\d{2}\-\d{2}"
    table_json = []
    # Navigate the downloaded files getting each ndjson file
    for subdir, dirs, files in os.walk(temp_folder):
        result = re.search(regex, subdir)
        if(result):
            date_string = result.group()
            for file in files: 
                if(file == file_name):
                    print(f"{subdir}/{file}")
                    with open(f"{subdir}/{file}", 'rb') as json_file:
                        clean_json(date_string,json_file, table_json)

    # Write the resulted JSON as a NDJSON
    write_ndjson(table_json)

    # Make an API request.
    with open('output.ndjson', 'rb') as source_file:
        load_job = bq_client.load_table_from_file(
            source_file,
            table_id,
            location="US",  
            job_config=job_config,
        ) 

    load_job.result()  # Waits for the job to complete.

    destination_table = bq_client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))
    
    # delete temp files
    os.system(f"rm -rf {temp_folder}")
    os.system('rm output.ndjson')

if __name__== "__main__":
    main()