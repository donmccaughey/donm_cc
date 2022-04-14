'use strict';

const { generate_seed, generate_maze } = wasm_bindgen;

function parse_seed_name(seed_name) {
        try {
            const parsed_seed = BigInt('0x' + seed_name);
            return BigInt.asUintN(64, parsed_seed);
        } catch (_) {
            return null;
        }
}

async function run() {
    await wasm_bindgen('maze_bg.wasm');

    let seed = null;
    let seed_name = '';
    const query = new URLSearchParams(location.search);
    if (query.has('seed')) {
        seed_name = query.get('seed');
        seed = parse_seed_name(seed_name);
    }

    if (seed == null) {
        seed = generate_seed();
        seed_name = seed.toString(16);
    }

    const state = {
        'seed': seed,
    }
    const title = 'Maze ' + seed_name;
    history.replaceState(state, title, './?seed=' + seed_name);

    const h1 = document.getElementById('maze_title');
    h1.textContent = title;

    const maze = generate_maze(20, 12, seed, 'unicode');
    const pre = document.getElementById('maze');
    pre.textContent = maze;

    const a = document.getElementById('next_maze');
    const next_seed = generate_seed();
    const next_seed_name = next_seed.toString(16);
    a.href = './?seed=' + next_seed_name;
}

run();
