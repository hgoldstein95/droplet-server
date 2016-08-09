#!/usr/bin/python

import requests
from datetime import datetime
import sys

key = '7d534632a5284dd1ddc2377338a89fae'
token = 'f5950550252053fae57e9f1c3e18a802a3af6446c87ced07c707e0d5edde03df'


def url(query, params):

    url = 'https://api.trello.com/1/'
    url += query
    url += '?'

    params['key'] = key
    params['token'] = token
    for k, v in params.items():
        url += '&' + k + '=' + v

    return url


def create_card(name, label, due='null', board='Personal', lst='To Do'):
    try:
        r = requests.get(
            url('members/harrisongoldstein/boards', {'fields': 'name'}))
        board_id = next(elem for elem in r.json()
                        if elem['name'] == board)['id']

        r = requests.get(url('boards/' + board_id +
                             '/lists', {'fields': 'name'}))
        list_id = next(elem for elem in r.json() if elem['name'] == lst)['id']

        r = requests.get(url('boards/' + board_id +
                             '/labels', {'fields': 'name'}))
        label_id = next(elem for elem in r.json()
                        if elem['name'] == label)['id']

        requests.post(url('cards', {'name': name, 'due': due,
                                    'idList': list_id, 'idLabels': label_id}))
    except Exception as e:
        try:
            label_id = next(elem for elem in r.json()
                            if elem['name'] == 'Server')['id']

            desc = {'name': name, 'label': label,
                    'due': due, 'board': board, 'lst': lst}

            requests.post(url('cards', {'name': 'Fix Trello Error',
                                        'desc': str(desc),
                                        'due': 'null',
                                        'idList': list_id,
                                        'idLabels': label_id}))
        except:
            pass
