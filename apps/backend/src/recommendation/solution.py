class Solution:
	def __init__(self, data):
		self.data = data

	def recommend(self, user):
		return self.data[user]
