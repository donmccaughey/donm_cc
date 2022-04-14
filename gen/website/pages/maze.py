from markdown import inline_markdown_to_markup
from markup import Section, H1, Pre, P, Text, A
from resources import Directory, Page


def maze():
    with Directory('maze'):
        with Page('Maze', name='index') as page:
            page.add_stylesheet('maze.css')
            page.add_script('maze_bg.js')
            page.add_script('maze.js')
            with Section(class_names=['overview']):
                H1('Maze Generator')
                with P():
                    inline_markdown_to_markup('''
                        A simple maze generator using a [randomized depth-first 
                        search](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
                        algorithm.
                    ''')
            with Section(class_names=['generator']):
                H1('Maze', id='maze_title')
                Pre(id='maze')
                with P(class_names=['next_maze']):
                    Text('(Try a ')
                    A(href='.', text='different maze', id='next_maze')
                    Text('.)')
            with Section(class_names=['implementation']):
                H1('Implementation')
                with P():
                    inline_markdown_to_markup('''
                        The [maze generator](https://github.com/donmccaughey/donm_cc/blob/master/maze/src/lib.rs)
                        is written in Rust and compiled to web assembly.  I used
                        [`wasm-pack build`](https://rustwasm.github.io/docs/wasm-pack/commands/build.html)
                        with the [`--target no-modules`](https://rustwasm.github.io/docs/wasm-bindgen/examples/without-a-bundler.html#using-the-older---target-no-modules)
                        option to compile Rust to web assembly and generate 
                        JavaScript bindings.
                    ''')
                with P():
                    inline_markdown_to_markup('''
                        The `maze` library exposes a very simple public 
                        interface of two functions to web assembly.
                    ''')
                with P():
                    inline_markdown_to_markup('''
                        The `generate_seed()` function returns a random 64-bit 
                        unsigned integer used to seed the pseudorandom number
                        generator; it also serves as the maze title.
                    ''')
                with P():
                    inline_markdown_to_markup('''
                        The `generate_maze()` function takes parameters for
                        _width_, _height_, the _seed_ and output _format_.  The
                        function returns a string containing the generated maze
                        for display using a monospace font.  The supported
                        formats are `"unicode"`, using
                        [Unicode box drawing characters](https://en.wikipedia.org/wiki/Box-drawing_character#Box_Drawing)
                        and `"ascii"`, using `-`, `|` and `+`. 
                    ''')
