import csv
import logging
from pathlib import Path

from src.path import get_path


def write_trip_survey_csv(
	trip_id: str,
	payload: dict,
	output_dir: Path | None = None,
) -> Path:
	if output_dir is None:
		output_dir = Path(get_path('surveys', 'logs'))
	output_dir.mkdir(parents=True, exist_ok=True)
	file_path = output_dir / f'{trip_id}.csv'

	sus = payload.get('sus', {})
	subjective = payload.get('subjective', {})
	sus_answers = sus.get('answers', [])
	subjective_answers = subjective.get('answers', [])

	fieldnames = [
		'trip_id',
		'submitted_at',
		'updated_at',
		'sus_score',
		'csat',
		'nps',
		'subjective_avg',
	]
	fieldnames += [f'sus_q{i + 1}' for i in range(10)]
	fieldnames += [f'subjective_q{i + 1}' for i in range(len(subjective_answers))]

	row = {
		'trip_id': trip_id,
		'submitted_at': payload.get('submitted_at'),
		'updated_at': payload.get('updated_at'),
		'sus_score': sus.get('score'),
		'csat': payload.get('csat'),
		'nps': payload.get('nps'),
		'subjective_avg': payload.get('subjective_avg'),
	}
	for idx, value in enumerate(sus_answers):
		row[f'sus_q{idx + 1}'] = value
	for idx, value in enumerate(subjective_answers):
		row[f'subjective_q{idx + 1}'] = value

	try:
		with open(file_path, 'w', newline='', encoding='utf-8') as handle:
			writer = csv.DictWriter(handle, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerow(row)
	except Exception as exc:
		logging.exception('Failed to write survey CSV: %s', exc)

	return file_path
