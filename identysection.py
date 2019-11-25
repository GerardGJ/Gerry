from jutge import read_line, read
start_sec=read(str)
end_sec=read(str)

while start_sec is not None:
	number_of_num=read(int)
	acuofnum=[]
	ended=False
	started=False
	x=0
	while x in range(number_of_num):
		num=read(str)
		if num==end_sec and started:
			ended=True
		if started and not ended:
			acuofnum.append(num)
		if num==start_sec:
			started=True
		x+=1
	if ended:
		stracu=''
		for letter in acuofnum:
			stracu=stracu+letter+' '
		print(stracu)
	else:
		print('')
	print('----------')
	start_sec=read(str)
	end_sec=read(str)
	
