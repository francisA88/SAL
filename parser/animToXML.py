''''''
'''
  All code under the StickMan project are written by me, Francis.'''
'''
A little code to convert .anim files to xml. Anim file was the previous data format created by me used for stickman animation instructions but I switched to xml instead'''

from xml.etree.ElementTree import XML, tostring

def _handle_sync(begin, lines:list):
	newtag = XML("<null/>").makeelement("Sync", {})
	diff = len(lines) #Will be used if no endsync tag is found
	for j in range(begin+1, len(lines)):
		if lines[j].replace(" ",'') == "endsync:":
			diff = j - begin+1
			break
		if lines[j].lstrip()[0] == "#": continue
		sm_tagline = lines[j].lstrip().split(" ")
		attr, prop = sm_tagline[0].split(".")
		value = sm_tagline[-1]
		chtag = newtag.makeelement(attr, {prop:value})
		newtag.append(chtag)
	return newtag, diff
	
def convert(string, out=None):
	root = XML("<StickMan></StickMan>")
	lines = string.splitlines()
	lines = [l for l in lines if l.replace(" ","")]
	last_speed = 1
	i = 0
	while i<len(lines):
		line = lines[i].lstrip()
		if not line.replace(" ",""):
			i+=i
		if line[0] == "#":
			i+=1
			continue
		if ":" in line:
			parts = list(map(lambda x:x.replace(" ",""),line.split(":")))
			if parts[0] == "sync":
				newtag, diff = _handle_sync(i, lines)
				root.append(newtag)
				i+=diff
			elif parts[0] == "speed":
				newtag = root.makeelement("speed", {"speed":parts[1]})
				root.append(newtag)
				i+=1
			elif parts[0] == "flip":
				newtag = root.makeelement("flip", {})
				root.append(newtag)
				i+=1
			elif parts[0] == "loop":
				newtag = root.makeelement("Loop", {"n":parts[1]})
				k = i+1
				while k<len(lines):
					if lines[k].replace(" ","") == "endloop:":
						i+=k+1
						break
					if lines[k].replace(" ","") == "sync:":
						elem, diff= _handle_sync(k, lines)
						newtag.append(elem)
						k+=diff
					else:
						sp = lines[k].lstrip().split(" ")
						attr, prop = sp[0].split(".")
						value = sp[-1]
						ch = root.makeelement(attr, {prop:value})
						newtag.append(ch)
				root.append(newtag)
		else:
			spl = lines[i].lstrip().split(" ")
			attr, prop = spl[0].split(".")
			value = spl[-1]
			ch = root.makeelement(attr, {prop:value})
			root.append(ch)
			i+=1
	
	xml_output = tostring(root, "unicode")
	HEADER = f'''
<!--Autogenerated by animToXML.py in minified form. For now there is no option for specifying whether to output in minified form or not but this might change in the future-->'''
	if out:
		import os
		if os.path.exists(out):
			res = input(f"Do you want to overwrite file '{out}'?[y/n]\n")
			if res.lower() == "y":
				open(out, "w").write(HEADER+xml_output)
			elif res.lower() == "n":
				print("Failed to write to output file!")
		else: open(out, "w").write(xml_output)
	return xml_output
	
def convertFile(source, out=None):
	return convert(open(source).read(), out)
	
if __name__ == "__main__":
	print(convertFile("../animations/backflip_hand2.anim", "../animations/backflip_hand2.xml"))
