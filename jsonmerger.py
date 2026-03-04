import os
import json

data_path = '../MakingOfNewAgent/data'
dest_path = 'combined.json'

with open(dest_path, 'w') as outfile:
    for root, dirs, files in os.walk(data_path):
        for f in files:
            if f.endswith('.json'):
                full_path = os.path.join(root, f)

                try:
                    with open(full_path, 'r') as infile:
                        data = json.load(infile)

                        # If file contains a list
                        if isinstance(data, list):
                            for item in data:
                                outfile.write(json.dumps(item))
                                outfile.write('\n')
                        else:
                            outfile.write(json.dumps(data))
                            outfile.write('\n')

                except Exception as e:
                    print(f"Error in file {full_path}: {e}")

print("Streaming merge complete.")