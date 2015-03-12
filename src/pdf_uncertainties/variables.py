variables = ["bdt_sig_bg", "cos_theta", "pdfweight"]
variables.extend(["scale", "id1", "id2", "x1", "x2"])

ranges = {}
ranges["bdt_sig_bg"] = (30, -1, 1)
ranges["cos_theta"] = (48, -1, 1)
ranges["pdfweight"] = (100, -200, 200)
ranges["scale"] = (100, 150, 500)
ranges["id1"] = (13, -6.5, 6.5)
ranges["id2"] = (13, -6.5, 6.5)
ranges["x1"] = (25, 0, 1)
ranges["x2"] = (25, 0, 1)

channels = ["mu", "ele"]
jettag = ["2j1t", "2j0t", "3j1t", "3j2t"]
