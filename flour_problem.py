# https://scipy-lectures.org/advanced/mathematical_optimization/#optimization-with-constraints

import numpy as np
import scipy.optimize

#https://www.fqmc.org/vivre-sans-gluten/infolettres-anterieures/valentin-2018/farines-sans-gluten
#https://tools.myfooddata.com/nutrition-facts/172023/100g/1

#Assume water ~ 100% - sum of all the rest
#Minerals = magnesium, potassium, phosphore
#Ash not included in this model
#                [Starch,  Sugars, Fiber, Proteins,    Fat, Minerals ]
wheat           = [  0.7,    0.02,  0.03,    0.115,  0.013, 0.0055]
brown_rice      = [ 0.76,  0.0066, 0.046,   0.0723, 0.0278, 0.0074]
white_rice      = [ 0.80,  0.0012, 0.024,   0.0595, 0.0142, 0.0021]
tapioca         = [ 0.89,  0.0002,    0.,   0.0006,     0.,     0.] 
potato          = [ 0.80,   0.035,  0.06,    0.007,  0.003, 0.0106]
arrowroot       = [0.875,      0., 0.031,       0.,     0., 0.0002]
almond          = [ 0.16,    0.04,  0.12,      0.2,   0.47, 0.0134]
banana          = [ 0.82,      0.,  0.07,    0.036,     0., 0.0035]
chickpea        = [ 0.47,    0.11,  0.11,     0.22,   0.07, 0.0139]
psyllium        = [ 0.88,      0.,  0.85,     0.02,     0., 0.0060] #mineral content unsure
quinoa          = [0.648,   0.029, 0.065,    0.118,  0.059, 0.0015] #mineral content unsure
oat             = [0.733,      0., 0.133,    0.133,   0.05, 0.0048] #mineral content unsure
teff            = [0.707,      0., 0.122,    0.122,  0.037, 0.0025] #mineral content unsure
sorghum         = [0.074,    0.01,   0.1,     0.11,  0.035, 0.0074]
millet          = [0.734,   0.017, 0.035,    0.108,  0.043, 0.0065]
cassava         = [0.886,      0., 0.057,       0.,     0., 0.0046] #mineral content unsure
pea_protein     = [   0.,      0.,    0.,     0.84,   0.15, 0.0050] #mineral content unsure
pumpkin_protein = [ 0.11,      0.,   0.1,     0.65,   0.08, 0.0020] #mineral content unsure


A  = np.array([ brown_rice, 
	            white_rice, 
	            tapioca,
	            potato,
	            arrowroot,
	            almond,
	            banana,
	            chickpea,
	            psyllium,
	            quinoa,
	            oat,
	            teff,
	            sorghum,
	            millet,
	            cassava,
	            pea_protein,
	            pumpkin_protein ]) 

#Function to optimize
def f(x):
	#C  = A x 
	# norm(Ax - Cd)**2
	# Cd = np.array(wheat)
	diff = (np.dot(np.transpose(A), np.transpose(x))) - np.array(wheat)
	return np.dot(np.transpose(diff), diff)

#Inequality constraint
def constraint(x):
	return np.sum(x) - 1


def print_results(x, desired_flour_grams):

	for idx in range(0, len(x)):
		if x[idx] < 1.e-10:
			x[idx] = 0 
		else:
			x[idx] = round(x[idx] * desired_flour_grams, 1)
	print "Desired flour amounts for a total of", str(desired_flour_grams), "g:"
	print "brown rice: ", x[ 0], " g"
	print "white rice: ", x[ 1], " g"
	print "tapioca   : ", x[ 2], " g"
	print "potato    : ", x[ 3], " g"
	print "arrowroot : ", x[ 4], " g"
	print "almond    : ", x[ 5], " g"
	print "banana    : ", x[ 6], " g"
	print "chickpea  : ", x[ 7], " g"
	print "psyllium  : ", x[ 8], " g"
	print "quinoa    : ", x[ 9], " g"
	print "oat       : ", x[10], " g"
	print "teff      : ", x[11], " g"
	print "sorghum   : ", x[12], " g"
	print "millet    : ", x[13], " g"
	print "cassava   : ", x[14], " g"
	print "pea       : ", x[15], " g"
	print "pumpkin   : ", x[16], " g"


x0 = np.zeros(np.shape(A)[0])

x = scipy.optimize.minimize(f, 
							x0, 
							bounds = ((0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.)), 
							constraints={"fun": constraint, "type": "eq"})

print "         composition:   [ Starch,  Sugars, Fiber, Proteins, Fat, Minerals ]"
print "Target   composition:  ", str(wheat)
print "Obtained composition:  ", str(np.dot(np.transpose(A), np.transpose(x.x)))

print_results(x.x, 115)