p='data//lfb_incidents_2009_2017.csv'
n=sum(1 for _ in open(p,'r',encoding='latin-1',errors='replace'))-1
print('csv_rows',n)
