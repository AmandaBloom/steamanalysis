import steammarket as sm

for i in range(20):
    tmp = sm.get_item(appid=730, name="Sticker | dupreeh | Berlin 2019", currency='PLN')
    print(i, tmp)
for i in range(2):
    tmp = sm.get_item(appid=730, name="Sticker | RpK | Berlin 2019", currency='PLN')
    print(i, tmp)
