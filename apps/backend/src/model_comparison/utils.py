def save(dir_name, model_name, loading_time, generation_time, word, result):
	output_file_path = dir_name + 'results_' + model_name + '.txt'
	with open(output_file_path, 'w', encoding='utf-8') as output_file:
		output_file.write(f'The model loading time: {loading_time:.2f} seconds\n')
		output_file.write(
			f'The result generation time: {generation_time:.2f} seconds\n'
		)
		if result:
			output_file.write(f"The most similar words to '{word}':\n")
			output_file.writelines(
				f'{similar_word} {similarity}\n' for similar_word, similarity in result
			)
		else:
			output_file.write(f"The word '{word}' is not present in the model.")

	print(f'The results have been saved to the file: {output_file_path}')
