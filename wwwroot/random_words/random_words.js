'use strict';


function initializeForm(query) {
    const countInput = document.querySelector('#count');
    countInput.value = query.count;

    const formatSentenceRadio = document.querySelector('#format_sentence');
    formatSentenceRadio.checked = query.isFormatSentence;

    const formatListRadio = document.querySelector('#format_list');
    formatListRadio.checked = query.isFormatList;

    const ol = document.querySelector('#random_words');
    ol.classList.add(query.format);
    ol.innerHTML = '';

    for (let i = 0; i < query.count; ++i) {
        pickWord().then(function(word) {
            const li = document.createElement('li');
            li.innerText = word;
            ol.appendChild(li);
        });
    }
}


function pickWord() {
    const resource = './words.table'
    const rowCount = 264097;
    const rowWidth = 46;

    const index = uniformRandomValue(rowCount);
    const firstBytePosition = rowWidth * index;
    const lastBytePosition = firstBytePosition + rowWidth - 1;

    return fetch(resource, {
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

        const format = parameters['format'] || 'list';
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

