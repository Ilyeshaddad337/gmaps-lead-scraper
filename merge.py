import os
import pandas as pd


folder = "outputs/restaurant_alger"
KEYWORD = "restaurant"
output_file = f"Leads/{folder.split('/')[-1].lower()}_merged.csv"
path_list = []
for subfolder in os.listdir(folder):
    if subfolder.startswith(KEYWORD):
        f_path = os.path.join(folder, subfolder )
        if os.path.isdir(f_path):
            csv_file = [f for f in os.listdir(f_path) if (f.endswith('.csv') and "phone" not in f)][0]
            final_path = os.path.join(f_path, csv_file)
            path_list.append(final_path)
            
df = pd.concat([pd.read_csv(f) for f in path_list], ignore_index=True)

df.to_csv(output_file, index=False)
print(f"Files merged into {output_file}")
print(f"Total files merged: {len(path_list)}")
print(f"shape of merged file: {df.shape}")