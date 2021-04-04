from markup import Section, H1, P, Form, Label, Input, Button, Text, A, Ul, Li
from resources import Directory, Page


def random_words():
    with Directory('random_words'):
        with Page('Random Words', name='index') as page:
            page.add_stylesheet('random_words.css')
            page.add_script('random_words.js')
            with Section(class_names=['overview']):
                H1('Random Words')
                P("""
                    <em>Random Words</em> is a small program that chooses random
                    entries from <a href=https://github.com/elasticdog/yawl>YAWL</a>,
                    a public domain list of 264,097 English words.
                 """)
            with Section(class_names=['generator']):
                H1('Results')
                P(id='random_words')
                with Form(action='./', method='GET'):
                    with P():
                        Label('Number of Words:', for_id='count')
                        Input(id='count', type='number', value='0')
                    with P():
                        Label('Format:')
                        Input(id='format_sentence', name='format', type='radio',
                              value='sentence', checked=True)
                        Label('Sentence', for_id='format_sentence')
                        Input(id='format_list', name='format', type='radio',
                              value='list')
                        Label('List', for_id='format_list')
                    with P():
                        Button('Go')
            with Section(id='implementation'):
                H1('Implementation')
                with P():
                    Text("""
                        <em>Random Words</em> is written in JavaScript and runs in the
                        browser.  To avoid the need to fetch the whole 2.7 MB YAWL
                        <a href=word.list><code>word.list</code></a> file, I've converted
                        <code>word.list</code> into a <a href=words.table>table</a> where 
                        each word is padded with spaces to 45 characters, the length of the
                     """)
                    A(
                        'https://en.wikipedia.org/wiki/Pneumonoultramicroscopicsilicovolcanoconiosis',
                        'longest word')
                    Text("""
                        in the list.
                     """)
                with P():
                    Text("""
                        The program uses the
                     """)
                    A(
                        'https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues',
                        '<code>getRandomValues()</code>')
                    Text("""
                        function to generate a random number in the range [0, 264097) to 
                        select a word, then uses the HTTP
                     """)
                    A('https://tools.ietf.org/html/rfc7233#section-3.1',
                      'Range header')
                    Text("""
                        to fetch only that word from the table.
                     """)
                with P():
                    with Ul():
                        with Li():
                            A('random_words.js', 'The JavaScript code')
                        with Li():
                            A('word.list', 'The YAWL word list')
                        with Li():
                            A('make_table.py',
                              'The Python script to generate the words table')
                        with Li():
                            A('words.table', 'The table of padded words')