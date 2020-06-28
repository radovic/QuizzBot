import re
import linecache

# decoder of letters from Serbo-Croatian language in case-insenitive way
def sh_decoder1(ans):
    for i in range(len(ans)):
        if (ans[i].encode() == b'\xc5\xa1') | (ans[i].encode() == b'\xc5\xa0'):
            ans = ans[:i] + "s" + ans[i + 1:]
        elif ((ans[i].encode() == b'\xc4\x8c') | (ans[i].encode() == b'\xc4\x8d')) | ((ans[i].encode() == b'\xc4\x86')
                | (ans[i].encode() == b'\xc4\x87')):
            ans = ans[:i] + "c" + ans[i + 1:]
        elif (ans[i].encode() == b'\xc5\xbe') | (ans[i].encode() == b'\xc5\xbd'):
            ans = ans[:i] + "z" + ans[i + 1:]
        elif (ans[i].encode() == b'\xc4\x90') | (ans[i].encode() == b'\xc4\x91'):
            ans = ans[:i] + "dj" + ans[i + 1:]
    return ans

# decoder of letters from Serbo-Croatian language in case-sensitive way
def sh_decoder2(ans):
    for i in range(len(ans)):
        if ans[i].encode() == b'\xc5\xa0':
            b = b'\xc5\xa1'
            ans = ans[:i] + b.decode() + ans[i + 1:]
        elif ans[i].encode() == b'\xc4\x8c':
            b = b'\xc4\x8d'
            ans = ans[:i] + b.decode() + ans[i + 1:]
        elif ans[i].encode() == b'\xc4\x86':
            b = b'\xc4\x87'
            ans = ans[:i] + b.decode() + ans[i + 1:]
        elif ans[i].encode() == b'\xc5\xbd':
            b = b'\xc5\xbe'
            ans = ans[:i] + b.decode() + ans[i + 1:]
        elif ans[i].encode() == b'\xc4\x90':
            b = b'\xc4\x91'
            ans = ans[:i] + b.decode() + ans[i + 1:]
        else:
            ans = ans[:i] + ans[i].lower() + ans[i+1:]
    return ans

# formatting input line that is not case-sensitive
def format_line(line):
    ans = line[line.find('[') + 1:line.find(']')]
    ans = sh_decoder1(ans)
    ans = ans.lower()
    return ans

# formatting input line that is case-sensitive
def format_line_sensitive(line):
    ans = line[line.find('[') + 1:line.find(']')]
    ans = sh_decoder2(ans)
    return ans

# evaluation of submitted answers
def the_questions_game(name_submission, name_answer):
    submission = open(name_submission, mode="r")
    answer = open(name_answer, "r")
    answers = []
    for not_formatted_line in submission:
        word = format_line(not_formatted_line)
        answers.append(word)
    counter = 0
    message = ""
    for not_formatted_line in answer:
        if not_formatted_line.find('[') == -1:
            continue
        word = format_line(not_formatted_line)
        message += "Team has answered " +answers[counter] + ".\n"
        if word == answers[counter]:
            message += "Correct answer.\n"
        else:
            message += "Incorrect answer. The correct answer is " + word + ".\n"
        counter = counter + 1
    return message

# calculating points for number game
def calculate_line(used, permitted, expression, ans, correct_answer):
    for i in range(len(used)):
        if used[i] not in permitted:
            return "You have used number " + str(used[i]) + " even if it is not offered.\n"
        elif permitted[used[i]] == 0:
            return "You have used number " + str(used[i]) + " more times than it is possible.\n"
        else:
            permitted[used[i]] = permitted[used[i]] - 1
    print(correct_answer)
    points = 16
    if correct_answer-ans == 0:
        points = 20
    points = points - abs(correct_answer - ans)
    if points < 0:
        points = 0
    return "The expression " + expression + "=" + str(ans) + " is admitted. You won " + str(points) + " points.\n"

# calculate points
def the_number_game(name_submission, name_answer):
    submission = open(name_submission, "r")
    num = 1
    answer = ""
    for not_formatted_line in submission:
        if not_formatted_line.find('[') == -1:
            continue
        configuration_line = linecache.getline(name_answer, num)
        correct_answer = linecache.getline(name_answer, num + 3)
        correct_answer = int(correct_answer)
        temp = re.findall(r'\d+', configuration_line)
        set_of_numbers = list(map(int, temp))
        permitted = dict()
        for i in range(len(set_of_numbers)):
            if set_of_numbers[i] not in permitted:
                permitted[set_of_numbers[i]] = 1
            else:
                permitted[set_of_numbers[i]] = permitted[set_of_numbers[i]] + 1
        expression = format_line(not_formatted_line)
        ans = 0
        try:
            ans = eval(expression)
        except:
            num = num + 1
            answer = answer + "Incorrect expression!"
        temp = re.findall(r'\d+', expression)
        used = list(map(int, temp))
        answer = answer + calculate_line(used, permitted, expression, ans, correct_answer)
        num = num + 1
    return answer

def the_word_game(name_submission, name_answer):
    answer = ""
    submission = open(name_submission, "r")
    num = 1
    for not_formatted_line in submission:
        if not_formatted_line.find('[') == -1:
            continue
        line = format_line_sensitive(not_formatted_line)
        offered = sh_decoder2(linecache.getline(name_answer, 1))
        offered_r = dict()
        for elem in offered.split():
            if elem not in offered_r:
                offered_r[elem] = 1
            else:
                offered_r[elem] = offered_r[elem] + 1
        mistake = False
        for elem in line.split():
            if elem not in offered_r:
                answer = answer + "In word " + line.replace(" ", "") + " you have used letter" + elem \
                          + " which is not offered.\n"
                num = num + 1
                mistake = True
                break
            else:
                if offered_r[elem] == 0:
                    answer = answer + "In word " + line.replace(" ", "") + " you have used letter " + elem \
                          + " more times than it is offered.\n"
                    num = num + 1
                    mistake = True
                    break
                else:
                    offered_r[elem] = offered_r[elem] - 1
        if mistake:
            continue
        else:
            points = 20
            if len(line.split()) == 11:
                points = 16
            elif len(line.split()) < 11:
                points = len(line.split())
            answer = answer + "Your word " + line.replace(" ", "") + " is correct. Potentially you can win as much as "\
                      + str(points) + " points.\n"
    return answer


