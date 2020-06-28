# QuizzBot
QuizzBot is a Discord bot which purpose is to facilitate organization of quizzes online.
## Setup
1. Clone the QuizzBot repository and install Python3.8 or higher.
2. Install the dependencies by running the command: 
<br> `pip install -r requirements.txt` in CMD with administrator permission, Windows.
<br> `sudo pip3 install -r requirements.txt` in terminal, Linux.
3. Create your own Discord bot, get its token and add it to your server. You can do it in following way:
go to [bot portal](https://discordapp.com/developers/applications/), log in, create new application, open Bot extension, reveal the 
token and save it. You can add your bot to your server by going to this address `https://discordapp.com/oauth2/authorize?client_id=CLIENTID&scope=bot`
where you should replace CLIENTID with Client ID that you can find in General Informations of yout bot.
4. Configure the configuration.txt file in the following way:
<br> 4.1. Replace <> in the first line with your User ID.
<br> 4.2. Replace <> in the second line with your bot's token.
<br> 4.3. Each of the following line should contain 2 informations, the first one is the number that 
identify the type of the game and the second one should be the path of file with 
correct answers of the game. You can find more information about games in Games section
of README.md file. Example of correct line: `1 Answers1.txt`.
5. Once you prepared your bot, every time you create new quizz you will have to modify only
part 4.3. Once you are ready you can start the bot by running command:
<br> `python main.py` in CMD, Windows.
<br> `python3 main.py` in terminal, Linux.
## Quizz organization
After you installed QuizzBot, you can proceed to organization of your quizz. The people who take
part in quizz are divided on competitors and quizzmasters. 
<br> The quizzmasters are organizators of quizz and they can decide if they want to 
start a game or to stop it. A game is started using the `!start (number_of_game) 
(seconds)` command where the number of game is equal to _(the line of the game in 
configuration.txt file) - 2_. If they start game accidentally or want to stop it, 
they run `!stop` command. 
<br> The competitors are all organized in groups, 
and each group should have its channel that is role-restricted to that group.
The competitors are able only to use `!submit` command when they want to submit an
answer to the current game. When using `!submit` command they should attach the file with
the answers to the message.
## Games
Quizzbot has the following types of games implemented(each type has a number that should be used for configuration.txt
file):
<br>**(1) The question game**: This type of game can be widely used for many games like standard questions,
associations etc. Answer file should have in each line two square brackets that contain 
inside them answer to the query. Example: `ans 1 = [the answer goes here]`. The part outside
of the brackets is not important.
<br>**(2) The number game**: This type of game is about giving the competitors a set of numbers on which they
can make mathematical operations in order to get a requested number. The configuration answer
file should contain a set of numbers divided by blanks in the first n lines and in the next
n lines it should contain the results of games so for every i-th line in the first n lines the result is
located in n+i line. The competitors answer with file that contains n lines, where each one contains
a mathematical expression corispondent to query. For example if for numbers 
`1 5  4 7 15 100` you have to find the closest number to `143` you can submit `100+15+7*4`.
<br>**(3) The word game**: In this type of game the quizzmaster gives to user a set of letters and the
user has to find the longest word composed from these letters. If the word made by user is 
legal(f.e. it doesn't use a letter that is not offered) the answer is sent to quizzmaster to check
the existence of that words. The answer configuration file contains in n lines set of words that can
be used for the game corrispondent to a line and the competitor answer file contains n lines with
words made up from letters corrispondent to the line.
## Note
This repository was made for educational purposes by its owner and the high performance is not guaranteed,
being tested just several times by himself.
