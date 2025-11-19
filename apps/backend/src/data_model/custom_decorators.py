def dict_behavior(cls):
	def __getitem__(self, key):
		if hasattr(self, key):
			return getattr(self, key)
		raise KeyError(key)

	def __iter__(self):
		return iter(vars(self))

	def keys(self):
		return vars(self).keys()

	cls.__getitem__ = __getitem__
	cls.__iter__ = __iter__
	cls.keys = keys

	return cls
