use structopt::StructOpt;
use std::ffi::OsStr;
use std::ffi::OsString;
use std::path::PathBuf;

use crate::abs_path::AbsPath;


fn get_abs_path(path: &OsStr) -> Result<AbsPath, OsString> {
    let path_buf = PathBuf::from(path);
    AbsPath::new(&path_buf).map_err(|e| {
        OsString::from(format!("{:?}", e))
    })
}


#[derive(StructOpt, Debug)]
#[structopt()]
/// Generate https://donm.cc
pub struct Options {
    #[structopt(short = "o", long = "output", parse(try_from_os_str = "get_abs_path"), default_value = "./tmp")]
    /// The directory to generated HTML files in
    pub output_dir: AbsPath,

    #[structopt(long = "overwrite")]
    /// Replace existing HTML files without warning
    pub overwrite: bool,

    #[structopt(name = "SITE_ROOT", parse(try_from_os_str = "get_abs_path"))]
    /// Path to the site content root folder
    pub site_root: AbsPath,

    #[structopt(short, long, parse(from_occurrences))]
    /// Be verbose, show each step in the generation process.
    /// Specify twice for additional logging.
    pub verbose: u8,
}

impl Options {
    pub fn new() -> Options {
        Options::from_args()
    }
}
