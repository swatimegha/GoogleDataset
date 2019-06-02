import re
str = """hello 

   world   and 

      India"""
#print(category1.replace("\n", "").replace("  ", " "))
print(re.sub(' +', ' ', str.replace('\n',' ')))