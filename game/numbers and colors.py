
if __name__ == '__main__':
	import random

	class Colors:
		colors = [
			["\033[1;32;40m", "Black", "\033[1;0;40m"],
			["\033[1;32;40m", "Blue", "\033[1;0;40m"],
			["\033[1;32;40m", "Green", "\033[1;0;40m"],
			["\033[1;32;40m", "Aqua", "\033[1;0;40m"],
			["\033[1;32;40m", "Red", "\033[1;0;40m"],
			["\033[1;32;40m", "Purple", "\033[1;0;40m"],
			["\033[1;32;40m", "Pink", "\033[1;0;40m"],
			["\033[1;32;40m", "Yellow", "\033[1;0;40m"],
			["\033[1;32;40m", "White", "\033[1;0;40m"],
			["\033[1;32;40m", "Gray", "\033[1;0;40m"]
		]
	while True:
		what_color = Colors.colors[random.randint(0, len(Colors.colors) - 1)][1]
		what_number = random.randint(0, 9)
		tell_correct = " is correct!"
		tell_incorrect = " is not correct."

		color_prompt = "Pick a color:\n"
		user_color = input(color_prompt)
		user_color = "nothing" if len(user_color) == 0 else user_color
		message = tell_correct if user_color.lower() == what_color.lower() else tell_incorrect
		print("The color is {c}. ".format(c=what_color) + user_color + message)

		number_prompt = "Pick a number:\n"
		user_number = input(number_prompt)
		user_number = "nothing" if len(user_number) == 0 else user_number
		message = tell_correct if user_number == str(what_number) else tell_incorrect
		print("The number is {n}. ".format(n=str(what_number)) + str(user_number) + message)
