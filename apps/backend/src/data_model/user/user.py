class User:
	id: str
	collaborative_filtering_dict: dict

	def __init__(self, id: str, collaborative_filtering_dict: dict = None):
		self.id = id
		self.collaborative_filtering_dict = collaborative_filtering_dict


def debug():
	trip_history_1 = [
		{
			'0': [
				{'id': 'ChIJ8-wGeU9gLxMR--zJtnpGod4'},
				{'id': 'ChIJK1-CN0xgLxMRZukH0_lPL70'},
				{'id': 'ChIJF0obe01gLxMR0JJHtlD0kMY'},
				{'id': 'ChIJzeDkbVJgLxMRf9wy9vdWbgw'},
				{'id': 'ChIJ1UCDJ1NgLxMRtrsCzOHxdvY'},
				{'id': 'ChIJr2C1NU1gLxMRAQ8Cfk1debk'},
				{'id': 'ChIJ412AG01gLxMR4T-4pwdIFSE'},
				{'id': 'ChIJ782pg7NhLxMR5n3swAdAkfo'},
				{'id': 'ChIJYevd8bJhLxMRvaa0jU2aqLE'},
			],
			'city_name': 'Rome',
			'1': [
				{'id': 'ChIJqUCGZ09gLxMRLM42IPpl0co'},
				{'id': 'ChIJLQGCLlBgLxMRuYQp8kv6syI', 'user_rating': 4.5},
				{'id': 'ChIJG6cU-09gLxMR8hkxk2gJcFI'},
				{'id': 'ChIJPRydwYNgLxMRSjOCLlYkV6M'},
				{'id': 'ChIJT8CVIAdhLxMR4_YveMMvc2Q'},
				{'id': 'ChIJZQ3ms1pgLxMRGnTxolu6mJE'},
				{'id': 'ChIJ0aTnEYeKJRMRiUF95xwRbDY'},
				{'id': 'ChIJWZsUt2FgLxMRg1KHzXfwS3I'},
			],
			'summary': '',
			'2': [
				{'id': 'ChIJvWOEp8GLJRMR26Pjt6rR3u4'},
				{'id': 'ChIJ24mMFhyLJRMRyTrm_FhBUZk'},
				{'id': 'ChIJb21z4RyLJRMRb5sqNSFqUe4'},
				{'id': 'ChIJEefbVB6LJRMR8e0oCpTC5SE'},
				{'id': 'ChIJswFN3_b1JRMRkQo7yHhbbY8'},
				{'id': 'ChIJ-8JXpCPzJRMRWH09GPdSqoA'},
			],
			'5': [
				{'id': 'ChIJGUmRfdyJJRMRthVKJHrrTl8'},
				{'id': 'ChIJuw_JEmdiLxMRYPhJoYzvmB0'},
				{'id': 'ChIJY-dxdmhiLxMRK7LAbMYIYKQ'},
			],
			'3': [{'id': 'ChIJ_4eBi6ViLxMRSsWuVaFl6g0'}],
			'4': [
				{'id': 'ChIJq-bXVgRhLxMRv3vgOXaktBs'},
				{'id': 'ChIJJ1C_JzhhLxMRBa83BNx-sXo'},
				{'id': 'ChIJP8ONNSVhLxMRlFtCgTWCcPA'},
				{'id': 'ChIJxcyMIv1gLxMRKAH_Dv2q8iw'},
				{'id': 'ChIJtdwDrgBhLxMRI9c93_OGqqI'},
				{'id': 'ChIJj1M8HQJhLxMRRI6D_z18Pes'},
				{'id': 'ChIJq8eXfgFhLxMR-M0hgvYjFMA'},
			],
			'city_id': 1380382862,
			'days_len': 6,
		}
	]
