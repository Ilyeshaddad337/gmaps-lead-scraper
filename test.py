import pandas as pd



def merge_dfs (df1_path, df2_path, output_path):
    df = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path)
    print(df.shape)
    print(df2.shape)


    new_df = pd.concat([df, df2], ignore_index=True)
    new_df = new_df.drop_duplicates(subset=['name', 'phone'], keep='last')
    new_df = new_df.reset_index(drop=True)
        

    new_df.to_csv(output_path, index=False)
    print("Merged data saved to "+ output_path)

    print(new_df.shape)

f = "outputs/hotel_alger/hotel_alger_2025_08_03_14_44_07.csv"
output = "outputs/hotel_alger/hotels_alger_nowebsite.csv"
df = pd.read_csv(f)
print(df.shape)
import re

df = df[(df['website'] == "no website") |( df['website'].str.startswith("https://www.ins")) | (df['website'].str.startswith("https://www.face"))]
df["rate_count"] = df["rating"].apply(lambda x: re.sub(r"[^0-9]","",x.split("(")[-1].replace(")","").strip()) if isinstance(x, str) else x)
df["rate_count"] = pd.to_numeric(df["rating_count"], errors='coerce')
df.sort_values(by='rate_count', ascending=False, inplace=True)
df.to_csv(output,columns=["name", "rating", "phone", "website"], index=False)
print(df.shape)
