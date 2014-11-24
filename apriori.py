import sys
import helper
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


class Apriori(object):
	"""Class to implement Apriori Algorithm"""	


	def __init__(self, inFile = sys.stdin, minSupport = 0.15 , minConfidence = 0.6):
		
		self.inFile = inFile
		self.minSupport = minSupport
		self.minConfidence = minConfidence
		self.toRetItems = []
		self.toRetRules = []
    	

	def returnItemsWithMinSupport(self, itemSet, transactionList, freqSet):
		"""calculates the support for items in the itemSet and returns a subset
	   	of the itemSet each of whose elements satisfies the minimum support"""
		_itemSet = set()
		localSet = defaultdict(int)
	    
		for item in itemSet:
			for transaction in transactionList:
				if item.issubset(transaction):
					freqSet[item] += 1
					localSet[item] += 1

		for item, count in localSet.items():
			support = float(count)/len(transactionList)
			if support >= self.minSupport:
				_itemSet.add(item)

		return _itemSet


	def getItemSetTransactionList(self):

		data_iterator = self.inFile
		transactionList = list()
		itemSet = set()
		for record in data_iterator:
			transaction = frozenset(record)
			transactionList.append(transaction)
			for item in transaction:
				itemSet.add(frozenset([item]))              # Generate 1-itemSets
		return itemSet, transactionList


	def runApriori(self):

		"""
		run the apriori algorithm. data_iter is a record iterator
		Return both:
		- items (tuple, support)
		- rules ((pretuple, posttuple), confidence)
		"""

		itemSet, transactionList = self.getItemSetTransactionList()

		freqSet = defaultdict(int)
		largeSet = dict()
		# Global dictionary which stores (key=n-itemSets,value=support)
		# which satisfy minSupport

		assocRules = dict()
		# Dictionary which stores Association Rules

		oneCSet = self.returnItemsWithMinSupport(itemSet, transactionList, freqSet)

		currentLSet = oneCSet
		k = 2
		while(currentLSet != set([])):
			largeSet[k-1] = currentLSet
			currentLSet = helper.joinSet(currentLSet, k)
			currentCSet = self.returnItemsWithMinSupport(currentLSet, transactionList, freqSet)
			currentLSet = currentCSet
			k = k + 1

		def getSupport(item):
			"""local function which Returns the support of an item"""
			return float(freqSet[item])/len(transactionList)

		self.toRetItems = []
		for key, value in largeSet.items():
			self.toRetItems.extend([(tuple(item), getSupport(item))
		                   for item in value])

		self.toRetRules = []
		for key, value in largeSet.items()[1:]:
			for item in value:
			    	_subsets = map(frozenset, [x for x in helper.subsets(item)])
			    	for element in _subsets:
			        	remain = item.difference(element)
			        	if len(remain) > 0:
			            		confidence = getSupport(item)/getSupport(element)
			            		if confidence >= self.minConfidence:
			                		self.toRetRules.append(((tuple(element), tuple(remain)),
			                                   confidence))


	def printResults(self):
		"""prints the generated itemsets and the confidence rules"""
		for item, support in self.toRetItems:
			print "item: %s , %.3f" % (str(item), support)
			print "\n------------------------ RULES:"
		for rule, confidence in self.toRetRules:
			pre, post = rule
			print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)


filename = "INTEGRATED-DATASET.csv"
inFile = helper.dataFromFile(filename)
a = Apriori(inFile)
a.runApriori()
a.printResults()
