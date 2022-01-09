from alphavantage import getAllSymbols

import os

all_symbols = getAllSymbols()
print(all_symbols, len(all_symbols))

# symbols_downloaded = set()
# for file in os.listdir('quotes'):
#     symbols_downloaded.add(file.split('-')[0])
# # print(symbols_downloaded)

# symbols_not_downloaded = [item for item in all_symbols if item not in symbols_downloaded]
# print(symbols_not_downloaded)

ignore_symbols = ['CL=F', 'CNH=F', 'DX-Y.NYB', 'EURUSD=X']

for symbol in all_symbols:
    if symbol in ignore_symbols:
        continue
    for index in range(1,4):
        expectFile = f"{symbol}-year1month{index}.csv"
        # print(f'verify {expectFile}')
        if not os.path.isfile(os.path.join('quotes', expectFile)):
            print(f"{expectFile} is not downloaded")