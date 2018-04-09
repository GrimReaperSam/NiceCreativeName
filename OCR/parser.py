import re
import os

for root, dirs, files in os.walk("Text/"):
    for file in files:
        if file.endswith(".txt"):
            ocr_file = open("Text/" + file, "r")
            all_str = ocr_file.read().replace("\r", "").replace("\n", "")
            area_raw = re.match(r'.*計畫範圍:.*?區(.*?)地號', all_str)
            if area_raw:
                area = area_raw.group(1).replace(" ", "").replace("(部分)", "")
                sec_num = re.match(r"(.+段)(.*)", area)
                section = sec_num.group(1)
                numbers = sec_num.group(2).split("、")

                csv_file = os.path.splitext(file)[0] + '.csv'
                with open('LandNumber/' + csv_file, 'w') as out_file:
                    for number in numbers:
                        # TODO: fix when i-1 and i+1 both less than i - tricky "1xx"
                        out_file.write(section + "," + number + "\n")
            else:
                print('NO AREA MATCHED: ' + file)
