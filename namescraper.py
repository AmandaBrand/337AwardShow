text_file = open("awardnames.txt", "r")
lines = text_file.readlines()
array = []
for line in lines:
	 array.append(line)
print array