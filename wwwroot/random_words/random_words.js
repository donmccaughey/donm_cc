'use strict';


// https://github.com/elasticdog/yawl
const yawl = {
    resource: './words.table',
    rowCount: 264097,
    rowWidth: 46
}


function initializeForm(query) {
    const countInput = document.querySelector('#count');
    countInput.value = query.count;

    const formatSentenceRadio = document.querySelector('#format_sentence');
    formatSentenceRadio.checked = query.isFormatSentence;

    const formatListRadio = document.querySelector('#format_list');
    formatListRadio.checked = query.isFormatList;

    const p = document.querySelector('#random_words');
    p.innerHTML = '';

    var container;
    var addWord;
    if (query.isFormatList) {
        const ol = document.createElement('ol');
        p.appendChild(ol);
        container = ol;
        addWord = addListWord;
    } else {
        container = p;
        addWord = addSentenceWord;
    }
    for (let i = 0; i < query.count; ++i) {
        pickWord().then(function(word) {
            addWord(container, word);
        });
    }
}


function addListWord(container, word) {
    const li = document.createElement('li');
    li.innerText = word;
    container.appendChild(li);
}


function addSentenceWord(container, word) {
    const span = document.createElement('span');
    span.innerText = word;
    container.appendChild(span);
    const space = document.createTextNode(' ');
    container.appendChild(space);
}


function pickWord() {
    const wordList = yawl;

    const index = uniformRandomValue(wordList.rowCount);
    const firstBytePosition = wordList.rowWidth * index;
    const lastBytePosition = firstBytePosition + wordList.rowWidth - 1;

    return fetch(wordList.resource, {
        headers: {
            Range: 'bytes=' + firstBytePosition + '-' + lastBytePosition
        }
    }).then((response) => {
        return response.text();
    }).then((text) => {
        return text.trim();
    });
}


function uniformRandomValue(exclusiveUpperBound) {
    const UINT32_MAX = 0xffffffff;
    const moduloBias = UINT32_MAX % exclusiveUpperBound;
    const largestMultiple = UINT32_MAX - moduloBias;
    const array = new Uint32Array(1);
    do {
        window.crypto.getRandomValues(array);
    } while (array[0] > largestMultiple);
    return array[0] % exclusiveUpperBound;
}


class Query {
    constructor(location) {
        const queryString = location.search.substring(1);
        const pairs = queryString.split('&');
        const parameters = {};
        for (const pair of pairs) {
            const parts = pair.split('=', 2);
            const name = decodeURIComponent(parts[0]);
            const value = (parts.length == 2) ? decodeURIComponent(parts[1]) : undefined;
            parameters[name] = value;
        }; 

        const count = parseInt(parameters['count'] || 3);
        this.count = isNaN(count) ? 3 : count;

        const format = parameters['format'] || 'sentence';
        this.format = ('sentence' == format.toLowerCase()) ? 'sentence' : 'list';
    }

    get isFormatList() {
        return 'list' == this.format;
    }

    get isFormatSentence() {
        return 'sentence' == this.format;
    }
}


function toInt(value) {
    const i = parseInt(value);
    return isNaN(i) ? undefined : i;
}


window.addEventListener('DOMContentLoaded', (event) => {
    const query = new Query(window.location);
    initializeForm(query);
});

