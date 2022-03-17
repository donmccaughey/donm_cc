use maze::generate_maze;

fn main() {
    let maze = generate_maze(20, 12, "unicode");
    println!("{}", maze);
}
