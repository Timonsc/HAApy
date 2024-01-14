
import warnings
import datetime
from pandas import concat
from ffn import to_price_index
from yfinance import download
warnings.filterwarnings("ignore")


name = "Default Haa"

# Inputs
offensives = ['SPY','IWM','VEA','VWO','DBC','VNQ','IEF','TLT']
defensives = ['IEF', 'BIL']
protectives = ['TIP']
number_of_assets = 4
all_stocks = offensives + defensives + protectives
end_date=datetime.date.today()
delta=datetime.timedelta(days=500)
start_date=end_date-delta
yahoo_data = download(all_stocks, start=start_date, end=end_date)['Adj Close'].pct_change().dropna()

print("")
print("Raw data:")
print(yahoo_data[-10:])

# Overwrite yahoo data with a the stocks' price index
for column in yahoo_data.columns.to_list():
    yahoo_data[column] = yahoo_data[column].dropna().to_price_index()

print("")
print("Indexed data:")
print(yahoo_data[-5:])

data_monthly = yahoo_data.resample('BM').last()

print("")
print("Monthly change %")
print(data_monthly.pct_change().dropna()[-5:])

# Calculate momentum score
score = sum([(data_monthly / data_monthly.shift(m) - 1) / 4 for m in [1,3,6,12]]).dropna()
of_score = score[offensives]
def_score = score[defensives]
prot_score = score[protectives]

print("")
print("Momentum score:\n")
print(score[-5:])

# Calculate if there's absolute momentum (If protectives, TIP, have positive a positive momentum score)
absolute_momentum = score.apply(lambda x: True if min(x[protectives]) > 0 else False, axis=1).to_frame('absolute_momentum')

print("")
print(absolute_momentum[-5:])

def pick_4_best_assets(x):
    if x['absolute_momentum']:
        of_momentums = x[offensives].astype(float).sort_values(ascending=False).iloc[:number_of_assets]
        def_momentum = x[defensives].astype(float).sort_values(ascending=False).iloc[:1]
        pos_of_momentums = of_momentums.loc[lambda x: x > 0]
        print(pos_of_momentums)
        a = len(pos_of_momentums)
        while a < number_of_assets:
            a += 1
            pos_of_momentums = concat([pos_of_momentums, def_momentum], axis=0)
        return pos_of_momentums.index.to_list()
    else:
        return x[defensives].astype(float).idxmax()


prediction = score.join(absolute_momentum).apply(pick_4_best_assets, axis=1).dropna()

print("")
print("Prediction:")        
print(prediction[:])

print("")
print("The allocation for", (prediction.index[-1] + datetime.timedelta(days=1)).date() ,"is", prediction[-1:].to_list())
print("The allocation is only valid when the script is run on the last day of the month;", prediction.index[-1].date())

exit(0)


# data = idx.drop('TIP',axis=1).shift(0).resample('BM').last()



# haa = HAA('Default HAA', data, ['SPY','QQQ','IWM','VEA','VWO','VNQ','DBC','IEF','TLT'], ['IEF', 'BIL'], ['SIMTIP'], 4).calc_momentum().calc_abs_momentum().make_prediction().calc_returns())
