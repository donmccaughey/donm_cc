from markup import Section, H1, P, Ul, H2
from resources import IndexPage
from website.links import link


def rust_and_wasm():
    with IndexPage('Rust and Wasm'):
        with Section(class_names=['overview']):
            H1('Rust and Wasm (WebAssembly)')
            P("""
                <em>Rust</em> is a modern, strongly-typed, compiled language with
                strict safety guarantees focused on building high performance
                systems.
             """)
            P("""
                <em>Wasm</em> (WebAssembly) is a binary instruction format for a
                stack-based virtual machine that runs in modern JavaScript 
                execution environments.
             """)
            P("""
                Together, Rust and Wasm open up new ways to write web clients,
                new ways to share code between client and server, and allow web
                clients to tackle problems that were previously impractical in
                JavaScript.
            """)
        with Section(class_names=['links']):
            H1('Rust')
            with Ul():
                link('site', 'The Rust Programming Language site',
                     'https://www.rust-lang.org')
                link('book', 'The Rust Programming Language book',
                     'https://doc.rust-lang.org/book/')
                link('book', 'Rust by Example',
                     'https://doc.rust-lang.org/rust-by-example/')
        with Section(class_names=['links']):
            H1('Wasm')
            with Ul():
                link('site', 'WebAssembly site', 'https://webassembly.org')
                link('docs', 'WebAssembly MDN web docs',
                     'https://developer.mozilla.org/docs/WebAssembly')
                link('blog',
                     "WebAssembly's post-MVP future: A cartoon skill tree",
                     'https://hacks.mozilla.org/2018/10/webassemblys-post-mvp-future/',
                     date='2018-10-22')
        with Section(class_names=['links']):
            H1('Rust and Wasm')
            with Ul():
                link('repo',
                     '<code>wasm-bindgen</code>: Import JavaScript things into Rust and export Rust things to JavaScript',
                     'https://github.com/rustwasm/wasm-bindgen')
                link('book', 'Rust and WebAssembly book',
                     'https://rustwasm.github.io/book/')
                link('blog', 'Rust and JavaScript Interop',
                     'https://blog.ryanlevick.com/posts/wasm-bindgen-interop/',
                     date='2018-09-12')
                link('blog', 'WebAssembly and Rust: A Web Love Story',
                     'https://github.com/raphamorim/wasm-and-rust',
                     date='2018-07-24')
            H2('Web Client Frameworks')
            with Ul():
                link('repo', 'stdweb', 'https://github.com/koute/stdweb')
                link('repo', 'Percy', 'https://github.com/chinedufn/percy')
                link('repo', 'Yew', 'https://github.com/DenisKolodin/yew')
                link('repo', 'Ruuhk', 'https://github.com/csharad/ruukh')
                link('repo', 'Draco', 'https://github.com/utkarshkukreti/draco')
                link('repo', 'Seed', 'https://github.com/David-OConnor/seed')
            H2('Libraries')
            with Ul():
                link('blog',
                     'Fast, Bump-Allocated Virtual DOMs with Rust and Wasm',
                     'https://hacks.mozilla.org/2019/03/fast-bump-allocated-virtual-doms-with-rust-and-wasm/')
                link('repo',
                     'Dodrio: A fast, bump-allocated virtual DOM library for Rust and WebAssembly.',
                     'https://github.com/fitzgen/dodrio')
            H2('Experience Reports')
            with Ul():
                link('blog',
                     'Lessons learned on writing web applications completely in Rust',
                     'https://medium.com/@saschagrunert/lessons-learned-on-writing-web-applications-completely-in-rust-2080d0990287',
                     date='2018-10-03')
                link('blog', 'Isomorphic Desktop Apps with Rust',
                     'https://speice.io/2018/09/isomorphic-apps.html',
                     date='2018-09-15')
                link('blog',
                     'A static web app in Rust: A three day tour of Yew and WASM in Rust',
                     'https://bluejekyll.github.io/blog/rust/2018/07/22/static-web-app-rust.html',
                     date='2018-07-22')
                link('blog', 'A web application completely in Rust',
                     'https://medium.com/@saschagrunert/a-web-application-completely-in-rust-6f6bdb6c4471',
                     date='2018-07-07')