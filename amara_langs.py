import requests, json
from itertools import groupby
import amara_vids as av



stf = open("iana_subtag_registry.txt").read()
langlist = stf.split("\%\%")
codelangs = {}


#lpairs = [codelangs[x] = get_lang() for x in lls]


class AmaraInfoSet(object):
	"""Gets metrics for videos/translations, writes json"""
	def __init__(self,relvid): #relvid should be a RelevantVideos instance
		relvid.manage_links()
		self.baseurl = "http://www.amara.org/api2/partners/videos/{}/languages/?format=json" # structured for .format arg
		self.vid_ids = relvid.ids.keys()
		self.total_langs = 0
		self.lang_names = []
		self.langs = {}
		self.get_info()
		self.get_non_english_langs()

	def get_info(self):
		for i in self.vid_ids:
			#print i # debug
			try:
				t = json.loads(requests.get(self.baseurl.format(i)).text)
				self.total_langs += int(t["meta"]["total_count"])
				for ob in t["objects"]:
					if ob["language_code"]:
						if ob["language_code"] in self.langs:
							self.langs[ob["language_code"]] += 1
						else:
							self.langs[ob["language_code"]] = 1
					if ob["name"] != "english": # using for non-english languages, primary use case
						self.lang_names.append(ob["name"])
			except:
				continue

	def get_non_english_langs(self):
		self.non_eng_langs = []
		self.total_transls = 0 # maybe not necessary, TODO consider
		for k in self.langs:
			if k != "en":
				self.total_transls += self.langs[k]
				print self.langs[k]
				self.non_eng_langs.append(k)

	def __str__(self):
		self.get_info()
		self.get_non_english_langs()
		s = """
		Number of total languages including English: {}
		Total non-English translations: {}
		Languages:

		""".format(len(self.langs.keys()),self.total_transls)
		for l in sorted(self.langs.keys()):
			s += "- {} {}\n".format(l,self.langs[l])
		return s


if __name__ == '__main__':

	om_acct = av.AmaraAccount("openmichigan.video")
	kath_acct = av.AmaraAccount("kludewig")

	relvs = av.RelevantVideos(om_acct,kath_acct)

	total_info = AmaraInfoSet(relvs)
	print total_info

	# def print_vid_ids(tv):
	# 	f = open("vid_ids.txt","w")
	# 	for x in tv.vid_ids:
	# 		f.write(x + "\n")
	# 	f.close()
	# print_vid_ids(total_info)

#BELOW OLD CODE ABOVE NEW CODE
## here's stuff where I was printing data ad-hoc-ily

# print "lang dict",langs

# print "number of total languages including english:", total_langs

# non_eng_langs = []
# total_transls = 0
# for k in langs:
# 	if k != "en":
# 		total_transls += langs[k]
# 		non_eng_langs.append(k)

# print "total non-english translations", total_transls
# print
# print "list of language codes:\n"
# for i in non_eng_langs: print i
# print 
# print "list of language names:"
# # for i in set(lang_names):
# # 	print i
# print
# for k in langs:
# 	print k, langs[k]
# print
# lnms = set(sorted(lang_names))
# print lnms

# # this stuff -- is it different? do I need to include it??
# amts = [len(list(group)) for key,group in groupby(lnms)]
# print amts
# tog = zip(set(lnms),amts)
# print tog
# # print
# # for k,y in sorted(tog,key=lambda x: x[1],reverse=True):
# # 	print k,y

# # here's where we should return formatted data


