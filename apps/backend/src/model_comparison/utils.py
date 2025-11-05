

def save(dir_name, model_name, loading_time, generation_time, word, result):
    output_file_path = dir_name + "results_" + model_name + ".txt"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("The model loading time: {:.2f} seconds\n".format(loading_time))
        output_file.write("The result generation time: {:.2f} seconds\n".format(generation_time))
        if result:
            output_file.write("The most similar words to '{}':\n".format(word))
            for similar_word, similarity in result:
                output_file.write("{} {}\n".format(similar_word, similarity))
        else:
            output_file.write("The word '{}' is not present in the model.".format(word))

    print("The results have been saved to the file: {}".format(output_file_path))