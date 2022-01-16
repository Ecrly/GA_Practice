w = [0, 2, 3, 4, 5]
v = [0, 3, 4, 5, 6]
cap = 8
n = 4
dp = []
for i in range(n + 1):
    dp.append([0] * (cap + 1))
for i in range(1, n + 1):
    for j in range(1, cap + 1):
        if(w[i] > j):
            dp[i][j] = dp[i - 1][j]
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w[i]] + v[i])
print(dp)