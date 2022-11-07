import json
from collections import defaultdict
import pandas as pd

from async_get_ballot_bu import  get_bu_file_name

df_data = defaultdict(list)

with open("ballots_with_decoding_issues.json", "r+") as fp:
    issues_bu_file = json.load(fp)


for ballot in issues_bu_file:
    file_name = get_bu_file_name(ballot)
    df_data['file_name'].append(file_name)
    df_data['state_code'].append(ballot['state_code'])
    df_data['council_name'].append(ballot['mu_name'])
    df_data['council_code'].append(ballot['mu_cd'])
    df_data['zone_code'].append(ballot['zone_cd'])
    df_data['section_code'].append(ballot['section_cd'])
    
df = pd.DataFrame(df_data)

df.to_csv("bu_not_able_decode.csv", index=False)