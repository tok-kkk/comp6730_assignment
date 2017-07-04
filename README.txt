# Program functions #

* We complish all levels of functionality in the assignment specification. 
* The program can check the file data whether follows the YXZ format.
* User can choose to set the mean vertical spacing and mean horizontal spacing mannually,
  otherwise the program will calculate them automatically from the data file
* The program will use both first and second approximation and report the results to user
* The program can calculate land area above certain sea level 
* The program can show the distribution of the land area percentage regarding the sea level by graph 
* The program is able to compute the number of separate connected land areas (islands) within the area covered by the data file at certain sea level.


# How to use it? #

* The user should input the file path of the data file.
* Then a menu will display like below:
	============================
	What would you like to do ?
	1. Calculate land area above certain sea level.
	2. See land area distribution.
	3. Calculate number of seperate land.
	0. Exit.
	============================
* Simply follow the message and type your choice.
* The result will display as the standard ouutput in shell.
* You won't exit the program until you type 0 in the main menu.


# ERROR NOTICE #

* Error message will rise when your input is invaid 
* The error message will tell why your input is invalid and help you find out what is the problem
  i.e. "The file is not YXZ formatted", "Please enter a number smaller 3"
* Usually the program will let you input again until it get a valid input/
* Most of the error handling functions are done in the checkers.py file
