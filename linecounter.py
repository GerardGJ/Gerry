from jutge import read, read_line
word=read(str)
line=read_line()
line_counter=0
while line is not None:
	for paraula in line.split():
		if paraula == word:
			line_counter +=1
			break
	line=read_line()
print(line_counter)
	
