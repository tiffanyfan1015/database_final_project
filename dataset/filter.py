import pandas as pd
import random

file_names = [
    "filtered_steam.csv",
    "filtered_steam_description_data.csv",
    "filtered_steam_media_data.csv",
    "filtered_steam_requirements_data.csv",
    "filtered_steam_support_info.csv",
    "filtered_steamspy_tag_data.csv"
]

steam_data = pd.read_csv("filtered_steam.csv")

sampled_appids = random.sample(list(steam_data['appid']), 1000)

for file_name in file_names:
    try:
        data = pd.read_csv(file_name)
        
        filtered_data = data[data['appid'].isin(sampled_appids)]
        
        missing_appids = set(sampled_appids) - set(data['appid'])
        if missing_appids:
            print(f"Info: {len(missing_appids)} appid(s) from the sample not found in {file_name}: {missing_appids}.")

            missing_data = pd.DataFrame(missing_appids, columns=['appid'])
            for col in data.columns:
                if col != 'appid':
                    missing_data[col] = None

            filtered_data = pd.concat([filtered_data, missing_data], ignore_index=True)
        
        output_file_name = f"filtered_{file_name}"
        filtered_data.to_csv(output_file_name, index=False)
        print(f"Filtered data saved to {output_file_name}")
    
    except Exception as e:
        print(f"Error processing {file_name}: {e}")