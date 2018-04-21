# coding=UTF-8

import re
import os

for root, dirs, files in os.walk("Text/"):
    for file in files:
        if file.endswith(".txt"):
            ocr_file = open("Text/" + file, "r")
            print("[Parsing] " + file)
            all_str = ocr_file.read().replace("\r", "").replace("\n", "")
            area_raw = re.match(r'.*計畫範圍:.*?區(.*?)地號', all_str)
            if area_raw:
                area = area_raw.group(1).replace(" ", "").replace("(部分)", "").replace("(部份)", "").replace("|", "")
                sec_num = re.match(r"(.+段)(.*)", area)
                section = sec_num.group(1)
                numbers = sec_num.group(2).split("、")

                csv_file = os.path.splitext(file)[0] + '.csv'
                with open('LandNumber/' + csv_file, 'w') as out_file:
                    for i in range(len(numbers)):
                        number = numbers[i]
                        # Fix when i-1 and i+1 both less than i - tricky "1xx"
                        if "及" in number:
                            numsAnd = number.split("及")
                            out_file.write(section + "," + numsAnd[0] + "\n")
                            out_file.write(section + "," + numsAnd[1] + "\n")
                        else:
                            if i < len(numbers) - 1 and number.isdigit() and numbers[i+1].isdigit() and int(number.split("-")[0]) > int(numbers[i+1].split("-")[0]):
                                number = number[1:]
                            out_file.write(section + "," + number + "\n")
            else:
                print(' --- NO MATCH --- ' + file)
