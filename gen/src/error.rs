use std::error;
use std::fmt;
use std::path::PathBuf;

use crate::abs_path::AbsPath;


#[derive(Debug)]
pub enum Error {
    NotADirectory(AbsPath),
    OutputDirIsRoot(String),
    PageExists(String, PathBuf),
    PathContainsInvalidUnicode(PathBuf),
    Unexpected(String),
}


impl error::Error for Error {}


impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            Error::NotADirectory(ref abs_path) => {
                write!(f, "Expected \"{}\" to be a directory", abs_path)
            }
            Error::PageExists(ref title, ref path_buf) => {
                let path = path_buf.to_string_lossy();
                write!(f, "File for page \"{}\" already exists at {}", title, path)
            }
            Error::OutputDirIsRoot(ref title) => {
                write!(f, "Output directory for page \"{}\" is '/'", title)
            },
            Error::PathContainsInvalidUnicode(ref path_buf) => {
                let path = path_buf.to_string_lossy();
                write!(f, "The path \"{}\" contains invalid Unicode", path)
            }
            Error::Unexpected(ref message) => {
                write!(f, "Unexpected error: \"{}\"", message)
            },
        }
    }
}
