import requests
from io import BytesIO
from pdfminer.high_level import extract_text

# PDF网页链接
url = "https://www.sigmaaldrich.cn/CN/zh/sds/sigma/g5516"

# 发送GET请求获取PDF文件
response = requests.get(url)
pdf_data = response.content

print(type(pdf_data))
# 使用pdfminer提取PDF内容
text = extract_text(BytesIO(pdf_data))

# 打印提取的内容
print(text)