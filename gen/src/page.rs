use std::path::PathBuf;
use crate::report::Report;
use std::error::Error;


#[derive(Debug, Deserialize)]
pub struct Page {
    pub path: PathBuf,
    pub title: String,

    #[serde(default)]
    pub children: Vec<Page>,
}

impl Page {
    pub fn generate(&self, report: &Report) -> Result<(), Box<dyn Error>> {
        report.will_generate_page(self);

        report.did_generate_page(self);

        for child in self.children.iter() {
            child.generate(report)?;
        }

        Ok(())
    }
}
