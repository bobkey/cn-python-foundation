"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
任务2: 哪个电话号码的通话总时间最长? 不要忘记，用于接听电话的时间也是通话时间的一部分。
输出信息:
"<telephone number> spent the longest time, <total time> seconds, on the phone during
September 2016.".

提示: 建立一个字典，并以电话号码为键，通话总时长为值。
这有利于你编写一个以键值对为输入，并修改字典的函数。
如果键已经存在于字典内，为键所对应的值加上对应数值；
如果键不存在于字典内，将此键加入字典，并将它的值设为给定值。
"""
Phone_dict = {}

def tells_count(phone,time):
    if phone in Phone_dict.keys():
        Phone_dict[phone] = Phone_dict[phone] + time
    else:
        Phone_dict[phone] = time

for i in calls:
    tells_count(i[0],int(i[3]))
    tells_count(i[1],int(i[3]))




max_time = max(Phone_dict.values())
for k,v in Phone_dict.items():
    if v == max_time:
        p_number = k

print("{} spent the longest time, {} seconds, on the phone during \
September 2016.".format(k,max_time))