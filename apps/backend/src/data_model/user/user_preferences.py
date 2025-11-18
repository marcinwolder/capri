import json
from dataclasses import InitVar, dataclass, field
from typing import Any, Literal, TypeAlias

Need: TypeAlias = Literal[
	'wheelchairAccessible',
	'goodForGroups',
	'vegan',
	'children',
	'alcohol',
	'allowsDogs',
]


@dataclass
class UserPreferences:
	"""User preferences data model."""

	price_level: int
	categories: list[str]
	subcategories: dict[str, list[str]]
	restaurant_categories: list[str]

	needs: InitVar[list[Need] | None] = None

	accessibility_options: bool = False
	good_for_groups: bool = False
	serves_vegetarian_food: bool = False
	children: bool = False
	alcohol: bool = False
	allows_dogs: bool = False

	def __post_init__(
		self,
		needs: list[Need] | None,
	):
		needs_list: list[Need] = [] if needs is None else needs
		self.accessibility_options: bool = 'wheelchairAccessible' in needs_list
		self.good_for_groups: bool = 'goodForGroups' in needs_list

		self.serves_vegetarian_food: bool = 'vegan' in needs_list
		self.children: bool = 'children' in needs_list
		self.alcohol: bool = 'alcohol' in needs_list
		self.allows_dogs: bool = 'allowsDogs' in needs_list
		self._handle_places_of_worship()

	def _handle_places_of_worship(self):
		"""Handle places of worship."""
		if 'place_of_worship' not in self.categories:
			return
		self.categories.remove('place_of_worship')
		pow: list[str] = self.subcategories.pop('place_of_worship')
		if len(pow) == 0:
			pow: list[str] = ['church', 'mosque', 'synagogue']
		for cat in pow:
			if cat == 'church':
				self.categories.append('church')
				self.subcategories['church'] = []
			elif cat == 'mosque':
				self.categories.append('mosque')
				self.subcategories['mosque'] = []
			elif cat == 'synagogue':
				self.categories.append('synagogue')
				self.subcategories['synagogue'] = []

	def to_json(self):
		return json.dumps(self.to_dict())

	def cat_weights(self):
		weights = dict.fromkeys(self.categories, 0)
		for key, _ in weights.items():
			weights[key] = len(self.subcategories[key])
		return weights

	def to_dict(self) -> dict[str, Any]:
		return {
			'priceLevel': self.price_level,
			'wheelchairAccessible': self.accessibility_options,
			'good_for_groups': self.good_for_groups,
			'vegan': self.serves_vegetarian_food,
			'children': self.children,
			'alcohol': self.alcohol,
			'allowsDogs': self.allows_dogs,
			'restaurant': self.restaurant_categories,
		}
