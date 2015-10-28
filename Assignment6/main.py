import getopt, sys
pollution_val = 0.9
smoker_val = 0.3
cancer_dict = {("high",True):0.05, ("high",False):0.02, ("low",True):0.03, ("low",False):0.001}
xray_dict = {True:0.9, False:0.2}
dyspnoea_dict = {True:0.65, False:0.3}
pollution = None
smoking = None
cancer = None
xray = None
dys = None

class Node:
	def __init__(self, name, parents):
		self.name = name
		self.parents = parents
		self.children = []
		self.marginal = 0.0
		self.conditionals = {}

	def add_child(self, child):
		self.children.append(child)

	def __str__(self):
		return "%s: marginal - %f" % (self.name, self.marginal)

class BayesNet:
	def __init__(self):
		self.nodes = {}

	def create_network(self):
		pollution = Node("pollution", None)
		smoker = Node("smoker", None)

		cancer = Node("cancer", [pollution, smoker])
		pollution.add_child(cancer)
		smoker.add_child(cancer)

		xray = Node("xray", [cancer])
		cancer.add_child(xray)

		dyspnoea = Node("dyspnoea", [cancer])
		dyspnoea.add_child(dyspnoea)

		# Define marginal from info
		pollution.marginal = 0.9
		smoker.marginal = 0.3
		
		# Define conditionals from table
		cancer.conditionals["ps"] = 0.03
		cancer.conditionals["~ps"] = 0.05
		cancer.conditionals["p~s"] = 0.001
		cancer.conditionals["~p~s"] = 0.02

		xray.conditionals["c"] = 0.9
		xray.conditionals["~c"] = 0.2

		dyspnoea.conditionals["c"] = 0.65
		dyspnoea.conditionals["~c"] = 0.3

		for n in [pollution, smoker, cancer, xray, dyspnoea]:
			self.nodes[n.name] = n

		return self.nodes

def false(true_p):
	return 1-true_p

def parse_joint(args):
	parsed = []
	arg_len = len(args)
	next_has_tilde = False
	for i in range(0,arg_len):
		if args[i] is "~":
			next_has_tilde = True
		else:
			if next_has_tilde:
				parsed.append("~"+args[i])
				next_has_tilde = False
			else:
				parsed.append(args[i])
	return parsed

def set_prior(net, variable, new_value):
	# Set a marginal probability for smoking or pollution
	print "Setting prior for variable {0} to {1}".format(variable, new_value)
	if variable is "P":
		net.nodes["pollution"].marginal = new_value
	elif variable is "S":
		net.nodes["smoker"].marginal = new_value

	# Either way return the new net
	return net

def calc_marginal(net, arg):
	# Takes in bayes net and the arg given (which var we want the marginal for)
	print "Calculating marginal probability for variable {0}".format(arg)

	if arg is "P" or arg is "p":
		return net.nodes["pollution"]

	elif arg is "S" or arg is "s":
		return net.nodes["smoker"]

	elif arg is "C" or arg is "c":
		# We have to actually calculate this time
		pollution = net.nodes["pollution"]
		smoker = net.nodes["smoker"]

		cancer = net.nodes["cancer"]
		# Sum over all possibilities of p and s
		cancer.marginal = cancer.conditionals["ps"]*pollution.marginal + cancer.conditionals["~ps"]*(1-pollution.marginal)*(smoker.marginal) + cancer.conditionals["p~s"]*pollution.marginal*(1-smoker.marginal) + cancer.conditionals["~p~s"]*(1-pollution.marginal)*(1-smoker.marginal)
		return cancer

	elif arg is "D" or arg is "d":
		dyspnoea = net.nodes["dyspnoea"]
		# Calculate cancers marginal if we don't have it
		cancer = net.nodes["cancer"]
		if not cancer.marginal or cancer.marginal is 0:
			net.nodes["cancer"] = calc_marginal(net, "C")
			cancer = net.nodes["cancer"]
		
		dyspnoea.marginal = dyspnoea.conditionals["c"]*cancer.marginal + dyspnoea.conditionals["~c"]*(1-cancer.marginal)
		return dyspnoea

	elif arg is "X" or arg is "x":
		xray = net.nodes["xray"]
		# Calculate cancers marginal if we don't have it
		cancer = net.nodes["cancer"]
		if not cancer.marginal or cancer.marginal is 0:
			net.nodes["cancer"] = calc_marginal(net, "C")
			cancer = net.nodes["cancer"]
		xray.marginal = xray.conditionals["c"]*cancer.marginal + xray.conditionals["~c"]*(1-cancer.marginal)

		return xray

def calc_conditional(net, var, given):
	print "Calculating conditional probability of {0} given {1}".format(var, given)
	if var is given:
		return 1
	else:
		# Now our given probability is 1, so we can calculate a marginal with the first var certain 
		net = set_prior(net, given, 1)
		return calc_marginal(net, var)

	return None

def calc_joint(net, vars):
	print "Calculating joint probability for {0}".format(vars)

	dyspnoea = net.nodes["dyspnoea"]
	xray = net.nodes["xray"]
	cancer = net.nodes["cancer"]
	pollution = net.nodes["pollution"]
	smoker = net.nodes["smoker"]
	# if dys == True:
	# 	if cancer == True:
	# 		return dyspnoea
	# 	elif cancer == False:
	# 	else:
	# 		cancer
	# elif
	# elif pollution == True:
	# 	return pollution.marginal
	# elif pollution == False:
	# 	return (1-pollution.marginal)
	# elif smoking == True:
	# 	return smoker.marginal
	# elif smoking == False:
	# 	return (1-smoker.marginal)
	# else
	# 	print "Error"

	if "P" in vars and "S" in vars and "C" in vars:
		print "P(P,S,C) " + str(cancer.conditionals["ps"] * pollution.marginal * smoker.marginal)
		print "P(P,S,~C) " + str(cancer.conditionals["p~s"] * pollution.marginal * (1 - smoker.marginal))
		print "P(~P,~S,C) " + str(cancer.conditionals["~ps"] * (1 - pollution.marginal) * smoker.marginal)
		print "P(~P,~S,C) " + str(cancer.conditionals["~p~s"] * (1 - pollution.marginal) * (1 - smoker.marginal))

		print "P(P,S,~C) " + str((1-cancer.conditionals["ps"]) * pollution.marginal * smoker.marginal)
		print "P(P,~S,~C) " + str((1-cancer.conditionals["p~s"]) * pollution.marginal * (1 - smoker.marginal))
		print "P(~P,S,~C) " + str((1-cancer.conditionals["~ps"]) * (1 - pollution.marginal) * smoker.marginal)
		print "P(~P,~S,~C) " + str((1-cancer.conditionals["~p~s"]) * (1 - pollution.marginal) * (1 - smoker.marginal))

	elif "p" in vars and "s" in vars and "c" in vars:
		print "P(P,S,C) " + str(cancer.conditionals["ps"] * pollution.marginal * smoker.marginal)

	elif "~p" in vars and "~s" in vars and "~c" in vars:
		print "P(~P,~S,~C) " + str((1-cancer.conditionals["~p~s"]) * (1 - pollution.marginal) * (1 - smoker.marginal))

if __name__ == "__main__":
	net = BayesNet()
	net.create_network()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
			# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			# Split into two values, then set the prior in the bayes net
			(variable, new_value) = a.split('=')
			net = set_prior(net, variable, float(new_value))
		elif o in ("-m"):
			print calc_marginal(net, a)
		elif o in ("-g"):
			print a
			(var, given) = a.split('/')
			print calc_conditional(net, var, given) 
		elif o in ("-j"):
			parsed_args = parse_joint(a)
			calc_joint(net, parsed_args)
		else:
			assert False, "unhandled option"