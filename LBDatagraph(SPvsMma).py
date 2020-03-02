import os.path
import math
import csv
import matplotlib.pyplot as plt
# column numbers: [0] time, [1] Bpos,
# [2] Bspd, [3] areacm, [4] Mma, [5] sp1 [6] sp2
filenames = []
plotnames = []
productnames = []
Nameofplot = ''
maxx = []
maxy = []
FC = 0

#function for rounding to nearest 10
def round_up(n):
    return int(math.ceil(n/10.0)) * 10

#function to check if file exists
def File_Exist():
	while True:
		File = input('Name file: ')
		if os.path.isfile(File):
			return File
			break
		elif File == 'exit' or File == 'Exit':
			exit()
		else:
			print ('File does not exist, type exit to exit')

# iterates over the entered filenames after and plot on a single graph.
# x and y max are the largest x and y value found from every submitted file
def Imposedplot():
	#opens and reads the file
	for k in filenames:
		x = []
		y = []
		with open(k, 'r') as file:
			csv_reader = csv.reader(file, dialect="excel-tab")
			for row in csv_reader:
				x.append(float(row[4]))
				y.append(float(row[5]))
		maxx.append(max(x))
		maxy.append(max(y))
		position = filenames.index(k)
		plt.plot(x, y, label = 	productnames[position])
	# sets maximum found x and y value and rounds to the nearest 10
	xy = round_up(max(maxx))
	yx = round_up(max(maxy))

	# Plotting
	plt.axis([0, xy, 0, yx])
	plt.suptitle(Nameofplot)
	plt.ylabel('SP [mN/m]')
	plt.xlabel('Mean Molecular Area [Å]\N{SUPERSCRIPT TWO}')
	plt.legend(loc="upper right" )

# function to create stacked figures.
# first three are created below each other
# four are generate as a 2x2 matrix
def StackedPlot():
	linecolours = ['b', 'g', 'r','k','m']
	fc = int(FC)
	if fc < 4:
		pltcnt = 0
		fig, axs = plt.subplots(fc, constrained_layout=True)
		for k in filenames:
			x = []
			y = []
			with open(k, 'r') as file:
				csv_reader = csv.reader(file, dialect="excel-tab")
				for row in csv_reader:
					x.append(float(row[4]))
					y.append(float(row[5]))
			Xmax = round_up(max(x))
			Ymax = round_up(max(y))
			position = filenames.index(k)
			axs[pltcnt].plot(x,y,linecolours[pltcnt], label = productnames[position])
			axs[pltcnt].axis([0, Xmax, 0, Ymax])
			axs[pltcnt].legend(loc='upper right')
			pltcnt = pltcnt + 1

		for ax in axs.flat:
			ax.set(xlabel='Mma [Å]\N{SUPERSCRIPT TWO}', ylabel='SP [mN/m]')
		fig.suptitle(Nameofplot)
	else:
		fig, axs = plt.subplots(2,2)
		pltcnt = 0
		for k in filenames:
			x = []
			y = []
			with open(k, 'r') as file:
				csv_reader = csv.reader(file, dialect="excel-tab")
				for row in csv_reader:
					x.append(float(row[4]))
					y.append(float(row[5]))
			Xmax = round_up(max(x))
			Ymax = round_up(max(y))
			position = filenames.index(k)
			plt.subplot(221 + pltcnt)
			plt.plot(x,y,linecolours[pltcnt], label = productnames[position])
			plt.axis([0, Xmax, 0, Ymax])
			plt.legend(loc='upper right')
			pltcnt = pltcnt + 1

		for ax in axs.flat:
			ax.set(xlabel='Mma [Å]\N{SUPERSCRIPT TWO}', ylabel='SP [mN/m]')
		plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95,
							hspace=0.25, wspace=0.35)
		fig.suptitle(Nameofplot)

# ------------------ MAIN SECTION --------------------------#
while True:
	FC =  input('How many files do you wish to load? (max 4): ')
	try:
		ValFC = int(FC)
		if ValFC <= 4:
			break
	except ValueError:
		print ('Input not valid')

i = 0

#Gets user imput for  file names and the legenda listed  products
while i < ValFC:
	j = File_Exist()
	i = i + 1
	Nameofplot = ''
	Product = ''
	# Plot detail input
	while Product == '':
		Product = input('Product(legend): ')
	productnames = productnames + [Product]
	filenames = filenames + [j]

while Nameofplot == '':
	Nameofplot = input('Name your plot: ')

while True:
    FC = int(FC)
    FigC = input('Stacked or superimposed?: ')
    if FigC == 'stacked' or FigC == 'Stacked':
        if FC == 1:
            Imposedplot()
            break
        elif FC >= 2:
            StackedPlot()
            break
    elif FigC == 'superimposed' or FigC == 'Superimposed':
        Imposedplot()
        break

# saving and closing
figname = input('Save figure as: ')
figname = figname + '.png'
plt.savefig(figname)
plt.close()
#----------------------MAIN SECTION ENDS----------------#
