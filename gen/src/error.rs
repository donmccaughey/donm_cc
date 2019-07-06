use std::error;
use std::fmt;
use std::path::PathBuf;


#[derive(Debug)]
pub enum Error {
    OutputDirIsRoot(String),
    PageExists(String, PathBuf),
}


impl error::Error for Error {}


impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            Error::PageExists(ref title, ref path) => {
                let path = path.to_string_lossy();
                write!(f, "File for page \"{}\" already exists at {}", title, path)
            },
            Error::OutputDirIsRoot(ref title) => {
                write!(f, "Output directory for page \"{}\" is '/'", title)
            },
        }
    }
}
