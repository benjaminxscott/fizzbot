#!/usr/bin/env python3

# Interactive python client for fizzbot

import json
import sys
import urllib.request
import urllib.error

BASE_DOMAIN = 'https://api.noopschallenge.com'

def fizzer(question_json):
    rules = question_json.get('rules')
    nums = question_json.get('numbers')
    out_list = []
    for num in nums:
        result = ""
        for rule in rules:
            if num % rule.get('number') == 0:
                result += rule.get('response')

        if not result:
            result = str(num)
        out_list.append(result)

    return " ".join(out_list)


# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    body = json.dumps({ 'answer': answer })
    try:
        req = urllib.request.Request(BASE_DOMAIN + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        response = json.load(res)
        return response

    except urllib.error.HTTPError as error:
        print(error)
        sys.exit(1)

# keep trying answers until a correct one is given
def get_correct_answer(question_url, question_json, first):
    if first:
        answer = "python"
    else:
        answer = fizzer(question_json)

    response = try_answer(question_url, answer)

    if response.get('result') == 'interview complete':
        print(f"completed in {response.get('elapsedSeconds')}s")
        return

    if response.get('result') == 'correct':
        return response.get('nextQuestion')

# do the next question
def do_question(domain, question_url, first = False):
    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_json = json.load(request)

    next_question = question_json.get('nextQuestion')

    if next_question:
        return next_question
    return get_correct_answer(question_url, question_json, first)

def main():
    question_url = '/fizzbot/questions/1'
    first = True
    while question_url:
        question_url = do_question(BASE_DOMAIN, question_url, first)
        first = False

if __name__ == '__main__':
    main()
