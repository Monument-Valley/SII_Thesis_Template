import glob

def count(file_list):
	# 计算每个文件列表中的中文字符数量，输出单项与总计
	total_count = 0
	for file_path in file_list:
		try:
			with open(file_path, 'r', encoding='utf-8') as f:
				content = f.read()
				count = sum(1 for char in content if '\u4e00' <= char <= '\u9fff')
				print(f"{file_path}: {count} 个中文字符")
				total_count += count
		except Exception as e:
			print(f"无法读取文件 {file_path}: {e}")
	print(f"总计: {total_count} 个中文字符")


if __name__ == "__main__":
	fl = sorted(glob.glob("source/zest_cn/chap/*.tex"))
	count(fl)