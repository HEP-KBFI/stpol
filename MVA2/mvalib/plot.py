import ROOT

_absvars = ['eta_lj']

def _find_minmax(trees, var):
	minv = float('inf')
	maxv = float('-inf')
	for tree in trees:
		minv = min(tree.GetMinimum(var), minv)
		maxv = max(tree.GetMaximum(var), maxv)
	return (0.0,max(abs(minv),abs(maxv))) if var in _absvars else (minv,maxv)

def calc_ROC(signals, backgrounds, var, nbins = 100):
	"""signals and backgrounds are dictionaries with keys the trees to plot and values weights"""
	minval,maxval = _find_minmax(map(lambda x: x.tree, signals+backgrounds), var)
	sh = ROOT.TH1F('sh_'+var, var+' distribution for signal', nbins, minval, maxval)
	bh = ROOT.TH1F('bh_'+var, var+' distribution for background', nbins, minval, maxval)
	print var,minval,maxval

	histvar = 'abs({0})'.format(var) if var in _absvars else var
	for sg in signals:
		sg.tree.Draw('{0} >>+ sh_{1}'.format(histvar, var), str(sg.lumiScaleFactor()))
	for bg in backgrounds:
		bg.tree.Draw('{0} >>+ bh_{1}'.format(histvar, var), str(bg.lumiScaleFactor()))

	graph = ROOT.TGraph(nbins+2)

	# total counts
	nsg = sh.GetSumOfWeights()
	nbg = bh.GetSumOfWeights()

	graph.SetPoint(0, 1.0, 0.0)
	graph.SetPoint(nbins+1, 0.0, 1.0)
	# accumulating sums
	ssg = 0.0
	sbg = 0.0
	print 'Max:',nsg,nbg
	for i in range(nbins):
		ssg += float(sh.GetBinContent(i))
		sbg += float(bh.GetBinContent(i))
		graph.SetPoint(i+1, 1.0-(ssg/nsg), sbg/nbg)

	return graph

def plot_ROC(signals, backgrounds, variables, nbins = 100, name='noname', title='MVA ROC plot'):
	"""plots the ROC curve for for the trees in signals vs trees in backgrounds for variables"""
	graph = {}
	for var in variables:
		graph[var] = calc_ROC(signals, backgrounds, var, nbins)

	canvas = ROOT.TCanvas("canv_"+name, "ROC curves", 650, 650)
	canvas.SetGrid()
	canvas.SetTicks()

	index = {}
	ngraph = 0
	for var in variables:
		ngraph += 1
		index[var] = ngraph
		graph[var].SetLineColor(ngraph)
		graph[var].SetLineWidth(2)
		if ngraph == 1:
			graph[var].Draw('AL')
			graph[var].GetXaxis().SetTitle('signal efficiency')
			graph[var].GetYaxis().SetTitle('background rejection')
			graph[var].GetXaxis().CenterTitle()
			graph[var].GetYaxis().CenterTitle()
			graph[var].SetTitle(title)
		else:
			graph[var].Draw('L SAME')

	legend = ROOT.TLegend(0.13, 0.13, 0.35, 0.35)
	for var in variables:
		legend.AddEntry(graph[var], var, 'LP')
	legend.Draw()

	img = ROOT.TImage.Create()
	img.FromPad(canvas)
	img.WriteImage('ROC_'+name+'.png')
