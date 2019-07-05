use structopt::StructOpt;
use std::path::PathBuf;


#[derive(StructOpt, Debug)]
#[structopt()]
/// Generate https://donm.cc
pub struct Options {
    #[structopt(short = "o", long = "output", parse(from_os_str), default_value = "./tmp")]
    /// The directory to generated HTML files in
    pub output_dir: PathBuf,

    #[structopt(name = "SITE_DEF", parse(from_os_str))]
    /// The YAML file containing the site definition
    pub site_definition_file: PathBuf,
}

impl Options {
    pub fn new() -> Options {
        Options::from_args()
    }
}
