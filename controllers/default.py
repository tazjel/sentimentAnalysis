# -*- coding: utf-8 -*-

def index():
    form = FORM(
            TEXTAREA(_name='sentence', requires=IS_NOT_EMPTY()),
            INPUT(_type='submit')
        ).process()
    if form.accepted:
        redirect(URL('sentence_analyser',vars=dict(sentence=form.vars.sentence)))
    return dict(form=form)

def sentence_analyser():
    import requests
    import json

    text = request.vars.sentence
    text = text.split('_')
    text = ' '.join(text)

    url = 'http://text-processing.com/api/sentiment/'
    data = {'text': text}

    r = requests.post(url, data=data)

    binary = r.content
    output = json.loads(binary)
    if output["label"] == 'neg':
        label = 'Negative'
    elif output["label"] == 'pos':
        label = 'Positive'
    else:
        label = 'Neutral'
    print output["probability"]["neg"]
    return dict(text=text,
                label=label,
                neg_prob=round(float(output["probability"]["neg"])*100),
                neutral_prob=round(float(output["probability"]["neutral"])*100),
                pos_prob=round(float(output["probability"]["pos"])*100))