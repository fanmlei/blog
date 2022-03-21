import os

path = "../source/_posts"

file_list = os.listdir(path)
for file in file_list:
    if file.startswith("blogs-"):
        new_name = file[6:]
        os.rename(f"{path}/{file}", f"{path}/{file[6:]}")
        print(f"{file}------>{new_name}")
print("批量修改完成")