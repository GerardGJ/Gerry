from jutge import read
num=read(int)
while num is not None:
	dicmatrix={}
	for n in range(2):	
		for x in range(num):
			posicio=[]
			for y in range(2):
				location=read(str)
				posicio.append(location)
			posicio=' '.join(posicio)
			nummatrix=read(int)
			if posicio in dicmatrix:
				dicmatrix[posicio] = dicmatrix[posicio] + nummatrix
			else:
				dicmatrix[posicio] = nummatrix 
			print(dicmatrix)
			#print('posicio',str(n), str(x), str(y))
		num=read(int)
		sorteddic=sorted(dicmatrix)
		#print(sorteddic)
	
	for posicio in sorteddic:
		if dicmatrix[posicio] != 0:
			print(posicio, str(dicmatrix[posicio]))
	print('-'*10)
	num=read(int)
