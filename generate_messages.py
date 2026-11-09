import pandas as pd
message_file = "Leads/message-dentists.txt"

variables = {
    "[name]": {
               "column":"dr-name",
                "default":""
               }
}

data = pd.read_csv("Leads/updated_Dentist_Leads.csv")
message = open(message_file, "r").read().strip()
new_df = data.copy()

new_df['message'] = data['dr-name'].apply(lambda x: message.replace("[name]", ("Dr. "+x) if pd.notna(x) else variables["[name]"]["default"]))

new_df.to_csv("Leads/messages_dentists.csv", index=False)