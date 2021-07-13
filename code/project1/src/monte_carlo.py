import numpy as np
import matplotlib.pyplot as plt

N = 40
x = np.random.rand(N)
y = np.random.rand(N) * 10

# random colour for points, vector of length N
colors = np.random.rand(N)
print(f"colors={colors}")

# area of the circle, vectoe of length N
area = (30 * np.random.rand(N)) ** 2
# 0 to 15 point radii

## a normal scatter plot with default features
# plt.scatter(x, y, alpha=0.8)
# plt.xlabel('Numbers')
# plt.ylabel('Values')
# plt.title('Normal Scatter Plot')
# plt.show()
#
## a scater plot with different size
# plt.figure()
# plt.scatter(x, y, s=area, alpha=0.8)
# plt.xlabel('Numbers')
# plt.ylabel('Values')
# plt.title('Different Size')
# plt.show()
#
# a scatter plot with different collour
plt.figure()
plt.scatter(x, y, c=colors, alpha=0.8)
plt.xlabel("Numbers")
plt.ylabel("Values")
plt.title("Different Colour")
plt.show()

# A combined Scatter Plot
plt.figure()
plt.scatter(x, y, s=area, c=colors, alpha=0.8)
plt.xlabel("Numbers")
plt.ylabel("Values")
plt.title("Combined")
plt.show()
