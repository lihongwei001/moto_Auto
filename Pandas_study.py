import pandas as pd

# Create a DataFrame
data1 = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

m = pd.DataFrame(data1)
print(m)
# Create a DataFrame from the dictionary
data2 = ["David", 40, "Houston"]
# Create a Series from the list with custom index
s = pd.Series(data2, index=['Name', 'Age', 'City'])
# print(s)
# print(s['Name'])  # Accessing by index label
# print(s[0])  # Accessing by integer position
# print(s[0:1])  # Slicing by integer position
# df = pd.DataFrame({
#     "姓名": ["张三", "李四", "王五", "赵六"],
#     "年龄": [20, 25, 30, 35],
#     "城市": ["北京", "上海", "广州", "深圳"]
# })
# print(df.iloc[1:3])
#
# data3 = ['Alice', 'Bob', 'Charlie', 'David']
