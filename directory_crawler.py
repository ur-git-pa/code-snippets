import os
import pandas as pd

def update_and_save_excel_files(input_dir):
    # Get the base name of the input directory
    base_dir = os.path.basename(input_dir)

    # Create the 'Updated' directory alongside the input directory
    updated_dir = os.path.join(os.path.dirname(input_dir), f"{base_dir} Updated")
    os.makedirs(updated_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith(".xlsx"):
                input_path = os.path.join(root, filename)
                # Calculate the relative path from the input directory to the Excel file
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(updated_dir, rel_path)

                # Create the output folder if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                try:
                    # Read the Excel file directly into a DataFrame
                    excel_document = pd.read_excel(input_path)

                    # Call the functions to update the Excel document
                    ######### Function call goes here #################
                    excel_document = excel_document.applymap(lambda x: str(x).upper())

                    # Write the DataFrame to the output Excel file
                    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                        excel_document.to_excel(writer, sheet_name='Sheet1', index=False)
                        log.append(f"Successfully updated {input_path}")

                except Exception as e:
                    # print(f"Error processing {input_path}: {str(e)}")
                    log.append(f"Error processing {input_path}: {str(e)}")
                    continue  # Skip to the next Excel file





# Specify the input directory
input_directory = r"directory"
log = []

update_and_save_excel_files(input_directory)

with open(r'directory\Log File.txt', 'w') as output_file:
    for line in log:
        output_file.write(line + '\n')
