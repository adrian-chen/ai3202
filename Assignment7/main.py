# Written by Adrian Chen

samples = [0.82, 0.56, 0.08, 0.81, 0.34, 0.22, 0.37, 0.99, 0.55, 0.61, 0.31, 0.66, 0.28, 1.0, 0.95, 0.71, 0.14, 0.1, 1.0, 0.71, 0.1, 0.6, 0.64, 0.73, 0.39, 0.03, 0.99, 1.0, 0.97, 0.54, 0.8, 0.97, 0.07, 0.69, 0.43, 0.29, 0.61, 0.03, 0.13, 0.14, 0.13, 0.4, 0.94, 0.19, 0.6, 0.68, 0.36, 0.67, 0.12, 0.38, 0.42, 0.81, 0.0, 0.2, 0.85, 0.01, 0.55, 0.3, 0.3, 0.11, 0.83, 0.96, 0.41, 0.65, 0.29, 0.4, 0.54, 0.23, 0.74, 0.65, 0.38, 0.41, 0.82, 0.08, 0.39, 0.97, 0.95, 0.01, 0.62, 0.32, 0.56, 0.68, 0.32, 0.27, 0.77, 0.74, 0.79, 0.11, 0.29, 0.69, 0.99, 0.79, 0.21, 0.2, 0.43, 0.81, 0.9, 0.0, 0.91, 0.01]

########################################################################
# Problem 1
########################################################################
sp_count = 0
wet_count = 0
sample_i = 0
c = True
sp = True
r = True
wet = True
results = []
while sample_i < 100:
	# c: True
	if samples[sample_i] < 0.5:
		sample_i += 1
		# c: True, sp: True
		if samples[sample_i] < 0.1:
			sample_i += 1
			# c: True, sp: True, r: True
			if samples[sample_i] < 0.8:
				sample_i += 1
				# c: True, sp: True, r: True, wet: True
				if samples[sample_i] < 0.99:
					sample_i += 1
					c = True
					sp = True
					r = True
					wet = True
				# c: True, sp: True, r: True, wet: False
				else:
					sample_i += 1
					c = True
					sp = True
					r = True
					wet = False
			# c: True, sp: True, r: False
			else:
				sample_i += 1
				# c: True, sp: True, r: False, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					c = True
					sp = True
					r = False
					wet = True
				# c: True, sp: True, r: False, wet: False
				else:
					sample_i += 1
					c = True
					sp = True
					r = False
					wet = False
		# c: True, sp: False
		else:
			sample_i += 1
			# c: True, sp: False, r: True
			if samples[sample_i] < 0.8:
				sample_i += 1
				# c: True, sp: False, r: True, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					c = True
					sp = False
					r = True
					wet = True
				# c: True, sp: False, r: True, wet: False
				else:
					sample_i += 1
					c = True
					sp = False
					r = True
					wet = False
			# c: True, sp: False, r: False
			else:
				sample_i += 2
				c = True
				sp = False
				r = False
				wet = False
	# c: False
	else:
		sample_i += 1
		# c: False, sp: True
		if samples[sample_i] < 0.5:
			sample_i += 1
			# c: False, sp: True, r: True
			if samples[sample_i] < 0.2:
				sample_i += 1
				# c: False, sp: True, r: True, wet: True
				if samples[sample_i] < 0.99:
					sample_i += 1
					c = False
					sp = True
					r = True
					wet = True
				# c: False, sp: True, r: True, wet: False
				else:
					sample_i += 1
					c = False
					sp = True
					r = True
					wet = False
			# c: False, sp: True, r: False
			else:
				sample_i += 1
				# c: False, sp: True, r: False, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					c = False
					sp = True
					r = False
					wet = True
				# c: False, sp: True, r: False, wet: False
				else:
					sample_i += 1
					c = False
					sp = True
					r = False
					wet = False
		# c: False, sp: False
		else:
			sample_i += 1
			# c: False, sp: False, r: True
			if samples[sample_i] < 0.2:
				sample_i += 1
				# c: False, sp: False, r: True, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					c = False
					sp = False
					r = True
					wet = True
				# c: False, sp: False, r: True, wet: False
				else:
					sample_i += 1
					c = False
					sp = False
					r = True
					wet = False
			# c: False, sp: False, r: False
			else:
				sample_i += 2
				c = False
				sp = False
				r = False
				wet = False
	results.append([c, sp, r, wet])

# Problem 1a
correct = 0
total = 0
for result in results:
	total += 1
	if result[0]:
		correct +=1
print "1a."
print correct/float(total)
print ""

# Problem 1b
correct = 0
total = 0
for result in results:
	if result[2]:
		total +=1
		if result[0]:
			correct +=1
print "1b."
print correct/float(total)

print ""

# Problem 1c
correct = 0
total = 0
for result in results:
	if result[3]:
		total +=1
		if result[1]:
			correct +=1
print "1c."
print correct/float(total)
print ""

# Problem 1d
correct = 0
total = 0
for result in results:
	if result[3] & result[0]:
			total +=1
			if result[1]:
				correct +=1
print "1d."
print correct/float(total)
print ""

########################################################################
# Problem 3
########################################################################
sample_i = 0
cloudy_count = 0
for item in samples:
	if item < 0.5:
		cloudy_count += 1
print "3a. Cloudy: " + str(cloudy_count/float(100))
print ""

print "3b."
cloudy_count = 0
cloudy = 0
rain_count = 0
for i in range(50):
	if samples[i*2] < 0.5:
		if samples[i*2 + 1] < 0.8:
			cloudy_count += 1
			rain_count += 1
	elif samples[i*2 + 1] < 0.2:
			rain_count += 1
print cloudy_count/float(rain_count)
print ""

print "3c."
sp_count = 0
wet_count = 0
sample_i = 0
while sample_i < 99:
	# c: True
	if samples[sample_i] < 0.5:
		sample_i += 1
		# c: True, sp: True
		if samples[sample_i] < 0.1:
			sample_i += 1
			# c: True, sp: True, r: True
			if samples[sample_i] < 0.8:
				sample_i += 1
				# c: True, sp: True, r: True, wet: True
				if samples[sample_i] < 0.99:
					sample_i += 1
					sp_count += 1
					wet_count += 1
				# c: True, sp: True, r: True, wet: False
				else:
					sample_i += 1
			# c: True, sp: True, r: False
			else:
				sample_i += 1
				# c: True, sp: True, r: False, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					sp_count += 1
					wet_count += 1
				# c: True, sp: True, r: False, wet: False
				else:
					sample_i += 1
		# c: True, sp: False
		else:
			sample_i += 1
			# c: True, sp: False, r: True
			if samples[sample_i] < 0.8:
				sample_i += 1
				# c: True, sp: False, r: True, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					wet_count += 1
				# c: True, sp: False, r: True, wet: False
				else:
					sample_i += 1
			# c: True, sp: False, r: False
			else:
				sample_i += 2
	# c: False
	else:
		sample_i += 1
		# c: False, sp: True
		if samples[sample_i] < 0.5:
			sample_i += 1
			# c: False, sp: True, r: True
			if samples[sample_i] < 0.2:
				sample_i += 1
				# c: False, sp: True, r: True, wet: True
				if samples[sample_i] < 0.99:
					sample_i += 1
					sp_count += 1
					wet_count += 1
				# c: False, sp: True, r: True, wet: False
				else:
					sample_i +=1
			# c: False, sp: True, r: False
			else:
				sample_i += 1
				# c: False, sp: True, r: False, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					sp_count += 1
					wet_count += 1
				# c: False, sp: True, r: False, wet: False
				else:
					sample_i += 1
		# c: False, sp: False
		else:
			sample_i += 1
			# c: False, sp: False, r: True
			if samples[sample_i] < 0.2:
				sample_i += 1
				# c: False, sp: False, r: True, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					wet_count += 1
				# c: False, sp: False, r: True, wet: False
				else:
					sample_i += 1
			# c: False, sp: False, r: False
			else:
				sample_i += 2

print sp_count/float(wet_count)
print ""

print "3d."
sp_count = 0
wet_count = 0
sample_i = 0
while sample_i < 97:
	# c: True
	if samples[sample_i] < 0.5:
		sample_i += 1
		# c: True, sp: True
		if samples[sample_i] < 0.1:
			sample_i += 1
			# c: True, sp: True, r: True
			if samples[sample_i] < 0.8:
				sample_i += 1
				# c: True, sp: True, r: True, wet: True
				if samples[sample_i] < 0.99:
					sample_i += 1
					sp_count += 1
					wet_count += 1
				# c: True, sp: True, r: True, wet: False
				else:
					sample_i += 1
			# c: True, sp: True, r: False
			else:
				sample_i += 1
				# c: True, sp: True, r: False, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					sp_count += 1
					wet_count += 1
				# c: True, sp: True, r: False, wet: False
				else:
					sample_i += 1
		# c: True, sp: False
		else:
			sample_i += 1
			# c: True, sp: False, r: True
			if samples[sample_i] < 0.8:
				sample_i += 1
				# c: True, sp: False, r: True, wet: True
				if samples[sample_i] < 0.9:
					sample_i += 1
					wet_count += 1
				# c: True, sp: False, r: True, wet: False
				else:
					sample_i += 1
			# c: True, sp: False, r: False
			else:
				sample_i += 1
	# c: False
	else:
		sample_i += 1


print sp_count/float(wet_count)




