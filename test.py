from re import IGNORECASE


def post_processing_insured(insured_name):
    import json
    import re
    #import pdb; pdb.set_trace()
    with open(r'./synonymML.json') as fp:
        synonymML=json.load(fp)
        for key in synonymML['Insured_Name']:
            insured_name=re.sub(key,'',insured_name)
    insured_name=re.sub(r"[:_()]",'',insured_name).strip()
    return(insured_name)

insured_name="Name of Proposer (Policy Holder):__AMCO Investments Ltd and subsidiaries"
print(post_processing_insured(insured_name))

its tetts kali