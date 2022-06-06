from feature_selector import FeatureSelector

n = int(input())

for i in range(1,n+1):
    kol = (i+1)*2-1
    for m in range(kol):
        if m < n:
            print(m,end='')
        else:
            print(m,end='')
    print()