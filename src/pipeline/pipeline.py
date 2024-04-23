
def pipeline(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        #print(content)
       # print('-'*80)
        file.close()
        lines = content.split('\n')
        #print(len(lines))

        return [{"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}, {"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}, {"parameter": "iron", "value": 5.3, "unit": "mmol/mL"}]

if __name__ == "__main__":
    pass