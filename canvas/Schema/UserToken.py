import	dataset

class UserToken:
	USERNAME = None			# Required - True		# Type -> String
	TOKEN = None			# Required - True		# Type -> String (uuid)
	EXPIRATION = None		# Required - True		# Type -> String (date - time)


	def __init__(self, username, token, expiration):
		self.USERNAME = username
		self.TOKEN = token
		self.EXPIRATION = expiration


	"""
	API Defined
	"""

	# Admin
	# Lists all UserTokens currently present in the system.
	# Return -> All the UserTokens.
	# Type -> set of UserToken
	def list(self, userToken):
		return 254
