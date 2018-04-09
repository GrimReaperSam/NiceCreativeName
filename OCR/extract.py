import os

for root, dirs, files in os.walk("./Crawler"):
    for file in files:
        if file.endswith(".pdf"):
            print(file)
            # base_name = os.path.basename(file)
            os.system("pdfextract Crawler/{0}:3-5 -o Pdf/{0}".format(file))

