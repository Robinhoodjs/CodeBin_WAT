import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

s = open(r'c:\Users\haloj\PycharmProjects\CodeBin_WAT\backend\generator\src\controller.py', encoding='utf-8').read()

# Pattern: match "from . import (" followed by content until closing ")"
result = re.sub(r'from \. import \([^)]*\)', '', s, flags=re.DOTALL)
# Also strip single-line form  
result = re.sub(r'from \. import [^\n(]+\n', '\n', result)

print("=== HAS text_checker ===", 'def text_checker' in result)
print("=== HAS text_corrector ===", 'def text_corrector' in result)
print()

# Test input_reader.py
s2 = open(r'c:\Users\haloj\PycharmProjects\CodeBin_WAT\backend\generator\src\input_reader.py', encoding='utf-8').read()
r2 = re.sub(r'from \. import \([^)]*\)', '', s2, flags=re.DOTALL)
r2 = re.sub(r'from \. import [^\n(]+\n', '\n', r2)
print("=== input_reader: HAS input_reader ===", 'def input_reader' in r2)

# Test description_creator.py
s3 = open(r'c:\Users\haloj\PycharmProjects\CodeBin_WAT\backend\generator\src\description_creator.py', encoding='utf-8').read()
r3 = re.sub(r'from \. import \([^)]*\)', '', s3, flags=re.DOTALL)
r3 = re.sub(r'from \. import [^\n(]+\n', '\n', r3)
print("=== description_creator: HAS scenario_creator ===", 'def scenario_creator' in r3)
print("=== description_creator: HAS story_teller ===", 'def story_teller' in r3)

# Test output_describer.py
s4 = open(r'c:\Users\haloj\PycharmProjects\CodeBin_WAT\backend\generator\src\output_describer.py', encoding='utf-8').read()
r4 = re.sub(r'from \. import \([^)]*\)', '', s4, flags=re.DOTALL)
r4 = re.sub(r'from \. import [^\n(]+\n', '\n', r4)
print("=== output_describer: HAS output_describer ===", 'def output_describer' in r4)
