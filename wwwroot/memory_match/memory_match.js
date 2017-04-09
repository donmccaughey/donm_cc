'use strict';

var numbersFaceSet = [
    ['0', 'zero'],
    ['1', 'one'],
    ['2', 'two'],
    ['3', 'three'],
    ['4', 'four'],
    ['5', 'five'],
    ['6', 'six'],
    ['7', 'seven'],
    ['8', 'eight'],
    ['9', 'nine'],
];
var romanCapitalLettersFaceSet = [
    ['A', 'capital A'],
    ['B', 'capital B'],
    ['C', 'capital C'],
    ['D', 'capital D'],
    ['E', 'capital E'],
    ['F', 'capital F'],
    ['G', 'capital G'],
    ['H', 'capital H'],
    ['I', 'capital I'],
    ['J', 'capital J'],
    ['K', 'capital K'],
    ['L', 'capital L'],
    ['M', 'capital M'],
    ['N', 'capital N'],
    ['O', 'capital O'],
    ['P', 'capital P'],
    ['Q', 'capital Q'],
    ['R', 'capital R'],
    ['S', 'capital S'],
    ['T', 'capital T'],
    ['U', 'capital U'],
    ['V', 'capital V'],
    ['W', 'capital W'],
    ['X', 'capital X'],
    ['Y', 'capital Y'],
    ['Z', 'capital Z'],
];
var romanSmallLettersFaceSet = [
    ['a', 'small A'],
    ['b', 'small B'],
    ['c', 'small C'],
    ['d', 'small D'],
    ['e', 'small E'],
    ['f', 'small F'],
    ['g', 'small G'],
    ['h', 'small H'],
    ['i', 'small I'],
    ['j', 'small J'],
    ['k', 'small K'],
    ['l', 'small L'],
    ['m', 'small M'],
    ['n', 'small N'],
    ['o', 'small O'],
    ['p', 'small P'],
    ['q', 'small Q'],
    ['r', 'small R'],
    ['s', 'small S'],
    ['t', 'small T'],
    ['u', 'small U'],
    ['v', 'small V'],
    ['w', 'small W'],
    ['x', 'small X'],
    ['y', 'small Y'],
    ['z', 'small Z'],
];
var greekCapitalLettersFaceSet = [
    ['\u0391', 'capital alpha'],
    ['\u0392', 'capital beta'],
    ['\u0393', 'capital gamma'],
    ['\u0394', 'capital delta'],
    ['\u0395', 'capital epsilon'],
    ['\u0396', 'capital zeta'], 
    ['\u0397', 'capital eta'], 
    ['\u0398', 'capital theta'], 
    ['\u0399', 'capital iota'], 
    ['\u039A', 'capital kappa'], 
    ['\u039B', 'capital lamda'], 
    ['\u039C', 'capital mu'], 
    ['\u039D', 'capital nu'], 
    ['\u039E', 'capital xi'], 
    ['\u039F', 'capital omicron'], 
    ['\u03A0', 'capital pi'], 
    ['\u03A1', 'capital rho'], 
    ['\u03A3', 'capital sigma'], 
    ['\u03A4', 'capital tau'],
    ['\u03A5', 'capital upsilon'], 
    ['\u03A6', 'capital phi'], 
    ['\u03A7', 'capital chi'], 
    ['\u03A8', 'capital psi'], 
    ['\u03A9', 'capital omega'], 
];
var greekSmallLettersFaceSet = [
    ['\u03B1', 'small alpha'], 
    ['\u03B2', 'small beta'], 
    ['\u03B3', 'small gamma'], 
    ['\u03B4', 'small delta'], 
    ['\u03B5', 'small epsilon'], 
    ['\u03B6', 'small zeta'], 
    ['\u03B7', 'small eta'], 
    ['\u03B8', 'small theta'], 
    ['\u03B9', 'small iota'], 
    ['\u03BA', 'small kappa'], 
    ['\u03BB', 'small lamda'], 
    ['\u03BC', 'small mu'], 
    ['\u03BD', 'small nu'], 
    ['\u03BE', 'small xi'], 
    ['\u03BF', 'small omicron'], 
    ['\u03C0', 'small pi'], 
    ['\u03C1', 'small rho'], 
    ['\u03C3', 'small sigma'], 
    ['\u03C2', 'small final sigma'], 
    ['\u03C4', 'small tau'], 
    ['\u03C5', 'small upsilon'], 
    ['\u03C6', 'small phi'], 
    ['\u03C7', 'small chi'], 
    ['\u03C8', 'small psi'], 
    ['\u03C9', 'small omega'], 
];
var foodEmojiFaceSet = [
    ['\uD83C\uDF47', 'grapes'], // '\u{1F347}'
    ['\uD83C\uDF48', 'melon'], // '\u{1F348}'
    ['\uD83C\uDF49', 'watermelon'], // '\u{1F349}'
    ['\uD83C\uDF4A', 'tangerine'], // '\u{1F34A}'
    ['\uD83C\uDF4B', 'lemon'], // '\u{1F34B}'
    ['\uD83C\uDF4C', 'banana'], // '\u{1F34C}'
    ['\uD83C\uDF4D', 'pineapple'], // '\u{1F34D}'
    ['\uD83C\uDF4E', 'red apple'], // '\u{1F34E}'
    ['\uD83C\uDF4F', 'green apple'], // '\u{1F34F}'
    ['\uD83C\uDF50', 'pear'], // '\u{1F350}'
    ['\uD83C\uDF51', 'peach'], // '\u{1F351}'
    ['\uD83C\uDF52', 'cherries'], // '\u{1F352}'
    ['\uD83C\uDF53', 'strawberry'], // '\u{1F353}'
    ['\uD83C\uDF45', 'tomato'], // '\u{1F345}'
    ['\uD83C\uDF46', 'aubergine'], // '\u{1F346}'
    ['\uD83C\uDF3D', 'ear of maize'], // '\u{1F33D}'
    ['\uD83C\uDF36', 'hot pepper'], // '\u{1F336}'
    ['\uD83C\uDF44', 'mushroom'], // '\u{1F344}'
    ['\uD83C\uDF30', 'chestnut'], // '\u{1F330}'
    ['\uD83C\uDF5E', 'bread'], // '\u{1F35E}'
    ['\uD83E\uDDC0', 'cheese wedge'], // '\u{1F9C0}'
    ['\uD83C\uDF56', 'meat on bone'], // '\u{1F356}'
    ['\uD83C\uDF57', 'poultry leg'], // '\u{1F357}'
    ['\uD83C\uDF54', 'hamburger'], // '\u{1F354}'
    ['\uD83C\uDF5F', 'french fries'], // '\u{1F35F}'
    ['\uD83C\uDF55', 'slice of pizza'], // '\u{1F355}'
    ['\uD83C\uDF2D', 'hot dog'], // '\u{1F32D}'
    ['\uD83C\uDF2E', 'taco'], // '\u{1F32E}'
    ['\uD83C\uDF2F', 'burrito'], // '\u{1F32F}'
    ['\uD83C\uDF73', 'cooking'], // '\u{1F373}'
    ['\uD83C\uDF72', 'pot of food'], // '\u{1F372}'
    ['\uD83C\uDF7F', 'popcorn'], // '\u{1F37F}'
    ['\uD83C\uDF71', 'bento box'], // '\u{1F371}'
    ['\uD83C\uDF58', 'rice cracker'], // '\u{1F358}'
    ['\uD83C\uDF59', 'rice ball'], // '\u{1F359}'
    ['\uD83C\uDF5A', 'cooked rice'], // '\u{1F35A}'
    ['\uD83C\uDF5B', 'curry and rice'], // '\u{1F35B}'
    ['\uD83C\uDF5C', 'steaming bowl'], // '\u{1F35C}'
    ['\uD83C\uDF5D', 'spaghetti'], // '\u{1F35D}'
    ['\uD83C\uDF60', 'roasted sweet potato'], // '\u{1F360}'
    ['\uD83C\uDF62', 'oden'], // '\u{1F362}'
    ['\uD83C\uDF63', 'sushi'], // '\u{1F363}'
    ['\uD83C\uDF64', 'fried shrimp'], // '\u{1F364}'
    ['\uD83C\uDF65', 'fish cake with swirl design'], // '\u{1F365}'
    ['\uD83C\uDF61', 'dango'], // '\u{1F361}'
    ['\uD83C\uDF66', 'soft ice cream'], // '\u{1F366}'
    ['\uD83C\uDF67', 'shaved ice'], // '\u{1F367}'
    ['\uD83C\uDF68', 'ice cream'], // '\u{1F368}'
    ['\uD83C\uDF69', 'doughnut'], // '\u{1F369}'
    ['\uD83C\uDF6A', 'cookie'], // '\u{1F36A}'
    ['\uD83C\uDF82', 'birthday cake'], // '\u{1F382}'
    ['\uD83C\uDF70', 'shortcake'], // '\u{1F370}'
    ['\uD83C\uDF6B', 'chocolate bar'], // '\u{1F36B}'
    ['\uD83C\uDF6C', 'candy'], // '\u{1F36C}'
    ['\uD83C\uDF6D', 'lollipop'], // '\u{1F36D}'
    ['\uD83C\uDF6E', 'custard'], // '\u{1F36E}'
    ['\uD83C\uDF6F', 'honey pot'], // '\u{1F36F}'
    ['\uD83C\uDF7C', 'baby bottle'], // '\u{1F37C}'
    ['\u2615', 'hot beverage'],
    ['\uD83C\uDF75', 'teacup without handle'], // '\u{1F375}'
    ['\uD83C\uDF76', 'sake bottle and cup'], // '\u{1F376}'
    ['\uD83C\uDF7E', 'bottle with popping cork'], // '\u{1F37E}'
    ['\uD83C\uDF77', 'wine glass'], // '\u{1F377}'
    ['\uD83C\uDF78', 'cocktail glass'], // '\u{1F378}'
    ['\uD83C\uDF79', 'tropical drink'], // '\u{1F379}'
    ['\uD83C\uDF7A', 'beer mug'], // '\u{1F37A}'
    ['\uD83C\uDF7B', 'clinking beer mugs'], // '\u{1F37B}'
    ['\uD83C\uDF7D', 'fork and knife with plate'], // '\u{1F37D}'
    ['\uD83C\uDF74', 'fork and knife'], // '\u{1F374}'
];
var animalsAndNatureEmojiFaceSet = [
    ['\uD83D\uDE48', 'see-no-evil monkey'], // '\u{1F648}'
    ['\uD83D\uDE49', 'hear-no-evil monkey'], // '\u{1F649}'
    ['\uD83D\uDE4A', 'speak-no-evil monkey'], // '\u{1F64A}'
    ['\uD83D\uDCA6', 'splashing sweat symbol'], // '\u{1F4A6}'
    ['\uD83D\uDCA8', 'dash symbol'], // '\u{1F4A8}'
    ['\uD83D\uDC35', 'monkey face'], // '\u{1F435}'
    ['\uD83D\uDC12', 'monkey'], // '\u{1F412}'
    ['\uD83D\uDC36', 'dog face'], // '\u{1F436}'
    ['\uD83D\uDC15', 'dog'], // '\u{1F415}'
    ['\uD83D\uDC29', 'poodle'], // '\u{1F429}'
    ['\uD83D\uDC3A', 'wolf face'], // '\u{1F43A}'
    ['\uD83D\uDC31', 'cat face'], // '\u{1F431}'
    ['\uD83D\uDC08', 'cat'], // '\u{1F408}'
    ['\uD83E\uDD81', 'lion face'], // '\u{1F981}'
    ['\uD83D\uDC2F', 'tiger face'], // '\u{1F42F}'
    ['\uD83D\uDC05', 'tiger'], // '\u{1F405}'
    ['\uD83D\uDC06', 'leopard'], // '\u{1F406}'
    ['\uD83D\uDC34', 'horse face'], // '\u{1F434}'
    ['\uD83D\uDC0E', 'horse'], // '\u{1F40E}'
    ['\uD83E\uDD84', 'unicorn face'], // '\u{1F984}'
    ['\uD83D\uDC2E', 'cow face'], // '\u{1F42E}'
    ['\uD83D\uDC02', 'ox'], // '\u{1F402}'
    ['\uD83D\uDC03', 'water buffalo'], // '\u{1F403}'
    ['\uD83D\uDC04', 'cow'], // '\u{1F404}'
    ['\uD83D\uDC37', 'pig face'], // '\u{1F437}'
    ['\uD83D\uDC16', 'pig'], // '\u{1F416}'
    ['\uD83D\uDC17', 'boar'], // '\u{1F417}'
    ['\uD83D\uDC3D', 'pig nose'], // '\u{1F43D}'
    ['\uD83D\uDC0F', 'ram'], // '\u{1F40F}'
    ['\uD83D\uDC11', 'sheep'], // '\u{1F411}'
    ['\uD83D\uDC10', 'goat'], // '\u{1F410}'
    ['\uD83D\uDC2A', 'dromedary camel'], // '\u{1F42A}'
    ['\uD83D\uDC2B', 'bactrian camel'], // '\u{1F42B}'
    ['\uD83D\uDC18', 'elephant'], // '\u{1F418}'
    ['\uD83D\uDC2D', 'mouse face'], // '\u{1F42D}'
    ['\uD83D\uDC01', 'mouse'], // '\u{1F401}'
    ['\uD83D\uDC00', 'rat'], // '\u{1F400}'
    ['\uD83D\uDC39', 'hamster face'], // '\u{1F439}'
    ['\uD83D\uDC30', 'rabbit face'], // '\u{1F430}'
    ['\uD83D\uDC07', 'rabbit'], // '\u{1F407}'
    ['\uD83D\uDC3F', 'chipmunk'], // '\u{1F43F}'
    ['\uD83D\uDC3B', 'bear face'], // '\u{1F43B}'
    ['\uD83D\uDC28', 'koala'], // '\u{1F428}'
    ['\uD83D\uDC3C', 'panda face'], // '\u{1F43C}'
    ['\uD83D\uDC3E', 'paw prints'], // '\u{1F43E}'
    ['\uD83E\uDD83', 'turkey'], // '\u{1F983}'
    ['\uD83D\uDC14', 'chicken'], // '\u{1F414}'
    ['\uD83D\uDC13', 'rooster'], // '\u{1F413}'
    ['\uD83D\uDC23', 'hatching chick'], // '\u{1F423}'
    ['\uD83D\uDC24', 'baby chick'], // '\u{1F424}'
    ['\uD83D\uDC25', 'front-facing baby chick'], // '\u{1F425}'
    ['\uD83D\uDC26', 'bird'], // '\u{1F426}'
    ['\uD83D\uDC27', 'penguin'], // '\u{1F427}'
    ['\uD83D\uDD4A', 'dove of peace'], // '\u{1F54A}'
    ['\uD83D\uDC38', 'frog face'], // '\u{1F438}'
    ['\uD83D\uDC0A', 'crocodile'], // '\u{1F40A}'
    ['\uD83D\uDC22', 'turtle'], // '\u{1F422}'
    ['\uD83D\uDC0D', 'snake'], // '\u{1F40D}'
    ['\uD83D\uDC32', 'dragon face'], // '\u{1F432}'
    ['\uD83D\uDC09', 'dragon'], // '\u{1F409}'
    ['\uD83D\uDC33', 'spouting whale'], // '\u{1F433}'
    ['\uD83D\uDC0B', 'whale'], // '\u{1F40B}'
    ['\uD83D\uDC2C', 'dolphin'], // '\u{1F42C}'
    ['\uD83D\uDC1F', 'fish'], // '\u{1F41F}'
    ['\uD83D\uDC20', 'tropical fish'], // '\u{1F420}'
    ['\uD83D\uDC21', 'blowfish'], // '\u{1F421}'
    ['\uD83D\uDC19', 'octopus'], // '\u{1F419}'
    ['\uD83D\uDC1A', 'spiral shell'], // '\u{1F41A}'
    ['\uD83E\uDD80', 'crab'], // '\u{1F980}'
    ['\uD83D\uDC0C', 'snail'], // '\u{1F40C}'
    ['\uD83D\uDC1B', 'bug'], // '\u{1F41B}'
    ['\uD83D\uDC1C', 'ant'], // '\u{1F41C}'
    ['\uD83D\uDC1D', 'honeybee'], // '\u{1F41D}'
    ['\uD83D\uDC1E', 'lady beetle'], // '\u{1F41E}'
    ['\uD83D\uDD77', 'spider'], // '\u{1F577}'
    ['\uD83D\uDD78', 'spider web'], // '\u{1F578}'
    ['\uD83E\uDD82', 'scorpion'], // '\u{1F982}'
    ['\uD83D\uDC90', 'bouquet'], // '\u{1F490}'
    ['\uD83C\uDF38', 'cherry blossom'], // '\u{1F338}'
    ['\uD83D\uDCAE', 'white flower'], // '\u{1F4AE}'
    ['\uD83C\uDFF5', 'rosette'], // '\u{1F3F5}'
    ['\uD83C\uDF39', 'rose'], // '\u{1F339}'
    ['\uD83C\uDF3A', 'hibiscus'], // '\u{1F33A}'
    ['\uD83C\uDF3B', 'sunflower'], // '\u{1F33B}'
    ['\uD83C\uDF3C', 'blossom'], // '\u{1F33C}'
    ['\uD83C\uDF37', 'tulip'], // '\u{1F337}'
    ['\uD83C\uDF31', 'seedling'], // '\u{1F331}'
    ['\uD83C\uDF32', 'evergreen tree'], // '\u{1F332}'
    ['\uD83C\uDF33', 'deciduous tree'], // '\u{1F333}'
    ['\uD83C\uDF34', 'palm tree'], // '\u{1F334}'
    ['\uD83C\uDF35', 'cactus'], // '\u{1F335}'
    ['\uD83C\uDF3E', 'ear of rice'], // '\u{1F33E}'
    ['\uD83C\uDF3F', 'herb'], // '\u{1F33F}'
    ['\u2618', 'shamrock'],
    ['\uD83C\uDF40', 'four leaf clover'], // '\u{1F340}'
    ['\uD83C\uDF41', 'maple leaf'], // '\u{1F341}'
    // ['\u{}', ''],
];

function faceSet(includeSets) {
    var faceSet = [];
    faceSet.merge(numbersFaceSet);
    var letterSet = nextRandomIntegerLessThan(2);
    if (letterSet == 0) {
        faceSet.merge(romanCapitalLettersFaceSet);
        faceSet.merge(romanSmallLettersFaceSet);
    } else {
        faceSet.merge(greekCapitalLettersFaceSet);
        faceSet.merge(greekSmallLettersFaceSet);
    }
    faceSet.merge(foodEmojiFaceSet);
    faceSet.merge(animalsAndNatureEmojiFaceSet);
    return faceSet;
}

function formatElapsedSeconds(elapsedSeconds) {
    var minutes = Math.trunc(elapsedSeconds / 60);
    var seconds = Math.trunc(elapsedSeconds % 60);
    return zeroPadded(minutes, 2) + ':' + zeroPadded(seconds, 2);
}

function em(value) {
    return '' + value + 'em';
}

function id(value) {
    return '#' + value;
}

function isOdd(number) {
    return number % 2;
}

// Uniform random integer if a good random integer source is available
function nextRandomIntegerLessThan(exclusiveUpperBound) {
    if (window.crypto && window.crypto.getRandomValues && Uint32Array) {
        var max = 0xffffffff;
        var min = 0;
        var count = max - min + 1;
        var moduloBias = count % exclusiveUpperBound;
        var uniformMax = max - moduloBias;
        var next = new Uint32Array(1);
        do {
            window.crypto.getRandomValues(next);
        } while (next[0] > uniformMax);
        return next[0] % exclusiveUpperBound;
    } else {
        return Math.floor(Math.random() * exclusiveUpperBound);
    }
}

function px(value) {
    return '' + value + 'px';
}

function toInt(value) {
    var i = parseInt(value);
    return isNaN(i) ? undefined : i;
}

function zeroPadded(value, length) {
    var stringValue = '' + value;
    if (stringValue.length >= length) return stringValue;

    var paddingLength = length - stringValue.length;
    var padding = Array(paddingLength).fill('0').join('');
    return padding + stringValue;
}

if (!Array.prototype.fill) {
  Object.defineProperty(Array.prototype, 'fill', {
    value: function(value) {

      // Steps 1-2.
      if (this == null) {
        throw new TypeError('this is null or not defined');
      }

      var O = Object(this);

      // Steps 3-5.
      var len = O.length >>> 0;

      // Steps 6-7.
      var start = arguments[1];
      var relativeStart = start >> 0;

      // Step 8.
      var k = relativeStart < 0 ?
        Math.max(len + relativeStart, 0) :
        Math.min(relativeStart, len);

      // Steps 9-10.
      var end = arguments[2];
      var relativeEnd = end === undefined ?
        len : end >> 0;

      // Step 11.
      var final = relativeEnd < 0 ?
        Math.max(len + relativeEnd, 0) :
        Math.min(relativeEnd, len);

      // Step 12.
      while (k < final) {
        O[k] = value;
        k++;
      }

      // Step 13.
      return O;
    }
  });
}

Array.prototype.merge = function(array) {
    Array.prototype.push.apply(this, array);
}

// Fisher–Yates shuffle
// https://en.wikipedia.org/wiki/Fisher–Yates_shuffle
Array.prototype.shuffle = function() {
    for (var i = this.length - 1; i > 0; --i) {
        var j = nextRandomIntegerLessThan(i + 1);
        var temp = this[i];
        this[i] = this[j];
        this[j] = temp;
    }
}

Array.prototype.shuffled = function() {
    var copy = this.slice();
    copy.shuffle();
    return copy;
}

Date.nowInSeconds = function() {
    return Math.trunc(Date.now() / 1000);
}

Math.trunc = Math.trunc || function(x) {
  if (isNaN(x)) {
    return NaN;
  }
  if (x > 0) {
    return Math.floor(x);
  }
  return Math.ceil(x);
};

Location.prototype.splitQueryParameters = function() {
    var queryString = this.search.substring(1);
    var pairs = queryString.split('&');
    var parameters = {};
    pairs.forEach(function(pair) {
        var parts = pair.split('=', 2);
        var name = decodeURIComponent(parts[0]);
        var value = (parts.length == 2) ? decodeURIComponent(parts[1]) : undefined;
        parameters[name] = value;
    }); 
    return parameters;
}

String.prototype.asArray = function() {
    return this.split('');
}

function View() {}

View.prototype.$ = function() {
    return $(id(this.id));
}

View.prototype.isHidden = function() {
    return this.$().css('display') == 'none';
}

View.prototype.isVisible = function() {
    return this.$().css('display') != 'none';
}

View.prototype.hide = function() {
    this.$().css( {display: 'none'} );
}

View.prototype.show = function() {
    this.$().css( {display: 'block'} );
}

View.prototype.toggleDisplay = function() {
    if (this.isHidden()) {
        this.show();
    } else {
        this.hide();
    }
}

function Board(container, width, height) {
    this.id = 'board';
    $('<div/>')
        .attr( {id: this.id} )
        .css({
            background: 'silver',
            border: '1pt solid black',
            height: em(height), 
            margin: '0 auto',
            padding: 0,
            position: 'relative',
            width: em(width)
        })
        .appendTo(container.$());
}

Board.prototype = new View();

function Container(id, game) {
    this.id = id;
    var $container = this.$();
    $container.css({
        background: 'white',
        border: 0,
        color: 'black',
        font: '12pt Helvetica, Arial, sans-serif',
        margin: 0,
        padding: '1em'
    }).empty();
    $container
        .on('touchend', game.onBackgroundClicked.bind(game))
        .on('click', game.onBackgroundClicked.bind(game));
}

Container.prototype = new View();

Container.prototype.setBottomMargin = function(cssHeight) {
    this.$().css( { marginBottom: cssHeight } );
}

function Options($container, width, horizontalTileCount, verticalTileCount) {
    this.id = 'options';
    var $options = $('<div/>')
        .attr( {id: this.id} )
        .css({
            background: 'white',
            border: '1pt solid black',
            display: 'none',
            margin: '1em',
            padding: '1em',
            position: 'absolute',
            textAlign: 'center',
            zIndex: 10,
        })
        .on('touchend', function(event) {
            event.stopPropagation();
        })
        .on('click', function(event) {
            event.stopPropagation();
        })
        .appendTo($container);

    $('<div>Options</div>')
        .css({
            fontWeight: 'bold',
            margin: '0 0 1em 0', 
            padding: 0
        })
        .appendTo($options);
    var $form = $('<form/>')
        .attr( {action: '.', method: 'GET'} )
        .css( {margin: 0, padding: 0} )
        .appendTo($options);
    var inputCss = {
        fontSize: '10pt',
        height: '2em',
        padding: '0 0.5em',
        width: '2.5em'
    };
    var $widthLabel = $('<label>width: </label>')
        .appendTo($form);
    $('<input/>')
        .attr( {name: 'width', type: 'number', value: horizontalTileCount} )
        .css(inputCss)
        .appendTo($widthLabel);
    $('<p/>').appendTo($form);
    var $heightLabel = $('<label>height: </label>')
        .appendTo($form);
    $('<input/>')
        .attr( {name: 'height', type: 'number', value: verticalTileCount} )
        .css(inputCss)
        .appendTo($heightLabel);
    $('<p/>').appendTo($form);
    $('<button>New Game</button>')
        .css({
            appearance: 'none',
            background: 'silver',
            border: '1px solid black',
            fontSize: '10pt',
            height: '4em',
            padding: '1em 2em'
        })
        .appendTo($form);
}

Options.prototype = new View();

function Status(container, width) {
    this.id = 'status';
    var $status = $('<div/>')
        .attr( {id: this.id} )
        .css({
            background: 'rgba(255, 255, 255, 0.9)', // white
            bottom: '0px',
            border: 0,
            borderTop: '1pt solid silver',
            left: '0px',
            margin: 0,
            padding: '0.5em',
            position: 'fixed',
            textAlign: 'center',
            width: '100%'
        })
        .appendTo(container.$());
    var tileLabelCss = {
            background: 'white',
            border: 0,
            display: 'inline-block',
            margin: 0,
            padding: '0 1em',
            position: 'absolute',
    };
    $('<div/>')
        .attr( {id: 'first_tile'} )
        .css(tileLabelCss)
        .css({
            left: '1em',
        })
        .appendTo($status);
    $('<div/>')
        .attr( {id: 'tries'} )
        .css({
            background: 'white',
            display: 'inline-block',
            padding: '0 1em',
        })
        .appendTo($status);
    $('<div/>')
        .attr( {id: 'clock'} )
        .css({
            background: 'white',
            display: 'inline-block',
            padding: '0 1em',
        })
        .appendTo($status);
    $('<div/>')
        .attr( {id: 'second_tile'} )
        .css(tileLabelCss)
        .css({
            right: '1em',
        })
        .appendTo($status);
    container.setBottomMargin(px($status.outerHeight()));
    this.setTries(0);
    this.setClock(0);
}

Status.prototype = new View();

Status.prototype.clearFirstTile = function() {
    $('#first_tile').empty();
}

Status.prototype.clearSecondTile = function() {
    $('#second_tile').empty();
}

Status.prototype.setFirstTile = function(tile) {
    $('#first_tile').text(tile.face[1]);
}

Status.prototype.setSecondTile = function(tile) {
    $('#second_tile').text(tile.face[1]);
}

Status.prototype.setTries = function(tries) {
    $('#tries').text('' + tries + ' tries');
}

Status.prototype.setClock = function(elapsedSeconds) {
    $('#clock').text(formatElapsedSeconds(elapsedSeconds));
}

function Tile(game, x, y, face) {
    this.face = face;
    this.faceDown = true;
    this.game = game;
    this.id = 'tile_' + x + '_' + y;

    var top = Tile.height * y + Tile.topPadding;
    var left = Tile.width * x + Tile.leftPadding;

    $('<div/>')
        .attr( {id: this.id} )
        .css({
            background: 'green',
            border: '1pt solid black',
            height: '4em',
            left: em(left),
            margin: '0.5em',
            textAlign: 'center',
            position: 'absolute',
            top: em(top), 
            width: '4em'
        })
        .on('touchend', this.onClick.bind(this))
        .on('click', this.onClick.bind(this))
        .appendTo(this.game.board.$());
}

Tile.height = 5;
Tile.width = 5;
Tile.topPadding = 2;
Tile.leftPadding = 2;

Tile.prototype = new View();

Tile.prototype.flipDown = function() {
    this.$().css( {backgroundColor: 'green'} ).empty();
    this.faceDown = true;
}

Tile.prototype.flipUp = function() {
    var $face = $('<span>')
        .css({
            border: 0,
            display: 'inline-block',
            font: 'bold 16px Verdana, Arial, sans-serif',
            lineHeight: px(32),
            margin: 0,
            padding: 0,
            position: 'absolute',
            transform: 'scale(2.67)'
        })
        .text(this.face[0]);
    var $tile = this.$();
    $tile
        .css( {backgroundColor: 'yellow'} )
        .append($face);
    var bottom = Math.trunc(($tile.innerHeight() - $face.outerHeight()) / 2);
    var left = Math.trunc(($tile.innerWidth() - $face.outerWidth()) / 2);
    $face.css( {bottom: px(bottom), left: px(left)} );
    this.faceDown = false;
}

Tile.prototype.matched = function() {
    this.$().remove();
}

Tile.prototype.onClick = function(event) {
    this.game.onTileClicked(this);
    event.stopPropagation();
    event.preventDefault();
}

function Title(container, game, width) {
    this.id = 'title';
    this.game = game;
    var $title = $('<div/>')
        .attr( {id: this.id} )
        .css({
            border: 0,
            margin: '0 auto 1em auto',
            padding: '0',
            position: 'relative',
            textAlign: 'center',
            width: em(width)
        })
        .appendTo(container.$());
    var $optionsButton = $('<img/>')
        .attr( {src: 'gear.png'} )
        .css({
            border: 0,
            height: '22px',
            left: '0px',
            margin: 0,
            padding: '10px',
            position: 'absolute',
            width: '22px'
        })
        .on('touchend', this.onOptionsButtonClick.bind(this))
        .on('click', this.onOptionsButtonClick.bind(this))
        .appendTo($title);
    $('<span/>')
        .css( {fontSize: '24pt'} )
        .text('Memory Match')
        .appendTo($title);
    var top = Math.trunc(($title.innerHeight() - $optionsButton.outerHeight()) / 2);
    $optionsButton.css( {top: px(top)} );
}

Title.prototype = new View();

Title.prototype.onOptionsButtonClick = function(event) {
    this.game.toggleOptions();
    event.stopPropagation();
    event.preventDefault();
}

function Game(containerID, horizontalTileCount, verticalTileCount) {
    var queryParameters = window.location.splitQueryParameters();
    
    this.horizontalTileCount = horizontalTileCount 
                            || toInt(queryParameters["width"]) 
                            || 4;
    this.verticalTileCount = verticalTileCount 
                          || toInt(queryParameters["height"]) 
                          || 4;
    this.faceSet = faceSet('all');
    this.faces = [];
    this.tiles = [];

    this.firstTile = null;
    this.secondTile = null;
    this.remainingTileCount = 0;
    this.onTileClicked = this.onNoneUp;
    this.tries = 0;
    this.clockIntervalID = null;
    this.clockStartInSeconds = null;
    this.clockCurrentInSeconds = null;

    this.createFaces();

    this.container = new Container(containerID, this);

    var width = this.horizontalTileCount * Tile.width + 2 * Tile.leftPadding;
    var height = this.verticalTileCount * Tile.height + 2 * Tile.topPadding;

    this.title = new Title(this.container, this, width);
    this.board = new Board(this.container, width, height);
    this.status = new Status(this.container, width);
    this.options = new Options(this.board.$(), width, 
                               this.horizontalTileCount, 
                               this.verticalTileCount);

    this.createTiles();
}

Game.prototype.clearClock = function() {
    this.clockStartInSeconds = null;
    this.clockCurrentInSeconds = null;
}

Game.prototype.createFaces = function() {
    var faceSet = this.faceSet.shuffled();
    var faceCount = Math.trunc(this.horizontalTileCount * this.verticalTileCount / 2);
    var uniqueFaces = faceSet.slice(0, faceCount);
    this.faces = uniqueFaces.concat(uniqueFaces).shuffled();
}

Game.prototype.createTiles = function() {
    var skipCenter = isOdd(this.horizontalTileCount) 
                  && isOdd(this.verticalTileCount);
    var centerI = Math.trunc(this.horizontalTileCount / 2);
    var centerJ = Math.trunc(this.verticalTileCount / 2);
    var n = 0;
    var $board = this.board.$();
    for (var i = 0; i < this.horizontalTileCount; ++i) {
        for (var j = 0; j < this.verticalTileCount; ++j) {
            if (skipCenter && i == centerI && j == centerJ) continue;
            this.tiles.push(new Tile(this, i, j, this.faces[n]));
            ++n;
        }
    }
    this.remainingTileCount = this.tiles.length;
}

Game.prototype.hasMatch = function() {
    return this.firstTile.face == this.secondTile.face;
}

Game.prototype.onGameCompleted = function() {
    this.stopClock();
    this.options.show();
}

Game.prototype.onGameStarted = function() {
    this.startClock();
}

Game.prototype.onTilesMatched = function() {
    this.remainingTileCount -= 2;
}

Game.prototype.onTilesNotMatched = function() {
}

Game.prototype.onBackgroundClicked = function(event) {
    if (this.secondTile) {
        this.resolveMatch();
        this.onTileClicked = this.onNoneUp;
    }
    if (this.remainingTileCount == 0) {
        this.onGameCompleted();
    } else {
        this.options.hide();
    }
    event.stopPropagation();
    event.preventDefault();
}

Game.prototype.onNoneUp = function(tile) {
    if (!this.tries) this.onGameStarted();
    tile.flipUp();
    this.status.setFirstTile(tile);
    this.firstTile = tile;
    this.onTileClicked = this.onOneUp;
}

Game.prototype.onOneUp = function(tile) {
    if (tile != this.firstTile) {
        tile.flipUp();
        ++this.tries;
        this.status.setSecondTile(tile);
        this.status.setTries(this.tries);
        this.secondTile = tile;
        this.onTileClicked = this.onTwoUp;
        if (this.hasMatch()) {
            this.onTilesMatched();
        } else {
            this.onTilesNotMatched();
        }
    }
}

Game.prototype.onTwoUp = function(tile) {
    if (tile != this.firstTile && tile != this.secondTile) {
        this.resolveMatch();
        tile.flipUp();
        this.status.setFirstTile(tile);
        this.firstTile = tile;
        this.onTileClicked = this.onOneUp;
    }
}

Game.prototype.resolveMatch = function() {
    if (this.hasMatch()) {
        this.firstTile.matched();
        this.secondTile.matched();
    } else {
        this.firstTile.flipDown();
        this.secondTile.flipDown();
    }
    this.firstTile = this.secondTile = null;
    this.status.clearFirstTile();
    this.status.clearSecondTile();
}

Game.prototype.startClock = function() {
    this.clockStartInSeconds = Date.nowInSeconds();
    this.clockCurrentInSeconds = this.clockStartInSeconds;
    var game = this;
    var delayInMillis = 200;
    this.clockIntervalID = setInterval(function() {
        var nowInSeconds = Date.nowInSeconds();
        if (nowInSeconds > game.clockCurrentInSeconds) {
            game.clockCurrentInSeconds = nowInSeconds;
            game.updateClock();
        }
    }, delayInMillis);
}

Game.prototype.stopClock = function() {
    clearInterval(this.clockIntervalID);
}

Game.prototype.toggleOptions = function() {
    this.options.toggleDisplay();
}

Game.prototype.updateClock = function() {
    this.status.setClock(this.clockCurrentInSeconds - this.clockStartInSeconds);
}

$(function() {
    new Game('memory_match');
});

