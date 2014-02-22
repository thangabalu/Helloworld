from termcolor import colored

"""
https://pypi.python.org/pypi/termcolor
#colored(text, color=None, on_color=None, attrs=None)

Text colors:

grey
red
green
yellow
blue
magenta
cyan
white

Text highlights:

on_grey
on_red
on_green
on_yellow
on_blue
on_magenta
on_cyan
on_white

Attributes:

bold
dark
underline
blink
reverse
concealed


"""


def main():
    print colored('Printing in red with attrs- blink', 'red', attrs =['blink'])
    print colored('Printing in grey with on_color=on_yellow', 'grey', 'on_yellow')
    print colored('Printing in blue with attrs = underline', 'blue', attrs=['underline'])
    print colored('Printing in cyan with attrs = blink', 'cyan', attrs=['blink'])
    print colored('Printing in white with attrs = reverse', 'white', attrs=['reverse'])



if __name__ == "__main__":
    main()