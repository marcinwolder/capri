import pathlib


def get_path(name: str, folder: str):
	"""Function that returns the path to the file, creating the specified folder above the 'src' directory."""
	current_path = pathlib.Path(__file__)

	src_path = current_path
	while src_path.name != 'src' and src_path.parent != src_path:
		src_path = src_path.parent

	if src_path.name != 'src':
		raise FileNotFoundError(
			"The 'src' directory could not be found in the path hierarchy."
		)

	project_root = src_path.parent

	folder_path = project_root / folder

	folder_path.mkdir(parents=True, exist_ok=True)

	file_path = folder_path / name

	return file_path
