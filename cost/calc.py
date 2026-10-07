import argparse,json
def estimate(row,input_tokens,output_tokens,cache_tokens=0):
 return (input_tokens-cache_tokens)*row['input']+cache_tokens*row.get('cached',row['input'])+output_tokens*row['output']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('prices');ap.add_argument('--input',type=int,default=200000);ap.add_argument('--output',type=int,default=20000);a=ap.parse_args()
 rows=json.load(open(a.prices));print(json.dumps({k:round(estimate(v,a.input,a.output),6) for k,v in rows.items()},indent=2))
if __name__=='__main__':main()
