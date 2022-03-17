use maze::{generate_maze, generate_seed};

fn main() {
    let seed = generate_seed();
    let maze = generate_maze(20, 12, seed,"unicode");
    println!("{}", maze);
}
