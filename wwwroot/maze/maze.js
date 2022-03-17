const { generate_seed, generate_maze } = wasm_bindgen;

async function run() {
    await wasm_bindgen('maze_bg.wasm');

    const seed = generate_seed();
    const h1 = document.getElementById('maze_title');
    h1.textContent = 'Maze ' + seed.toString(16);

    const maze = generate_maze(20, 12, seed, 'unicode');
    const pre = document.getElementById('maze');
    pre.textContent = maze;
}

run();
