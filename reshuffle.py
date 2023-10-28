import re
import random
import easygui

input_file_path = easygui.fileopenbox('Select Input File')
output_file_path = easygui.filesavebox('Save Output File')


def rearrange_and_write(question, output_file, q_index=None):
    question_text = (question)

    # Regular expression pattern to match the options
    pattern = r'([a-d]\))'

    # Split text using the regular expression pattern
    options = re.split(pattern, question_text)

    # Remove any empty strings and strip whitespaces
    options = [opt.strip() for opt in options if opt.strip()]
    options.remove('a)')
    options.remove('b)')
    options.remove('c)')
    options.remove('d)')

    question_tag = f"{options[0].split(':')[0].split()[0]} {q_index}) {options[0].split(':')[1]}"

    with open(output_file, 'a+') as file:
        file.write(f'{question_tag}\n')
        file.write(f'a) {options[1]}\n')
        file.write(f'b) {options[2]}\n')
        file.write(f'c) {options[3]}\n')
        file.write(f'd) {options[4]}\n\n')


def shuffle_questions(input_file, output_file_path, shuffle_options=True, shuffle_questions=False):
    # Read the content of the text file
    with open(input_file, 'r') as file:
        content = file.read()

    # Split the content into individual questions and options
    questions = re.split(r'(Question \d+: .*\n(?:[a-d]\) .*\n)+)', content)[1:]

    # Shuffle options for each question
    shuffled_questions_list = []
    for question in questions:
        question_lines = question.strip().split('\n')
        question_text = question_lines[0]
        options = question_lines[1:]

        correct_options = [option for option in options if '*' in option]
        other_options = [option for option in options if '*' not in option]

        if correct_options:
            correct_option = correct_options[0]
            random.shuffle(other_options)
            shuffled_options = [correct_option] + other_options
            random.shuffle(shuffled_options) if shuffle_options else None
            shuffled_question = question_text + '\n' + '\n'.join(shuffled_options) + '\n'
            shuffled_questions_list.append(shuffled_question)

        else:
            # Handle cases where there is no correct option marked with '*'
            shuffled_questions_list.append(question)
    # Shuffle the questions
    random.shuffle(shuffled_questions_list) if shuffle_questions else None
    # Remove redundant newline characters
    for i in shuffled_questions_list:
        if i == '\n':
            shuffled_questions_list.remove(i)
    # Write questions to output file
    question_number = 1
    for item in shuffled_questions_list:
        try:
            rearrange_and_write(item, output_file=output_file_path, q_index=question_number)
            question_number += 1
        except:
            print(f"An error occurred with this question: {item}")


if __name__ == '__main__':
    shuffle_questions(input_file=input_file_path, output_file_path=output_file_path, shuffle_options=True,
                      shuffle_questions=False)
