use std::error::Error;
use std::fs::create_dir_all;
use std::fs::write;
use std::path::PathBuf;

use crate::options::Options;
use crate::report::Report;
use std::path::Component::RootDir;


#[derive(Debug, Deserialize)]
pub struct Page {
    pub path: PathBuf,
    pub title: String,

    #[serde(default)]
    pub children: Vec<Page>,
}

impl Page {
    pub fn generate(&self, options: &Options, report: &Report)
        -> Result<(), Box<dyn Error>>
    {
        report.will_generate_page(self);

        let relative_path = match self.path.strip_prefix(RootDir) {
            Ok(stripped_path) => stripped_path,
            Err(_) => &self.path,
        };

        let mut output_path = options.output_dir.clone();
        output_path.push(relative_path);

        let output_dir = output_path.parent().ok_or("Path is root")?;
        create_dir_all(output_dir)?;

        let title = format!("<title>{}</title>", self.title);
        write(output_path, title)?;

        report.did_generate_page(self);

        for child in self.children.iter() {
            child.generate(options, report)?;
        }

        Ok(())
    }
}
