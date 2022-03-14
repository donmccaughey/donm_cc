use maze::generate_maze;

fn main() {
    let maze = generate_maze(20, 8);
    println!("{}", maze);
}
