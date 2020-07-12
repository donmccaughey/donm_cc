use std::error::Error;
use std::fs::File;
use std::io::BufReader;

use crate::abs_path::AbsPath;
use crate::report::Report;


#[derive(Debug, Deserialize)]
pub struct SiteFile {
    pub name: String,
}

impl SiteFile {
    pub fn read(site_file_path: &AbsPath, report: &Report) -> Result<SiteFile, Box<dyn Error>> {
        report.will_read_site_file(&site_file_path);

        let file = File::open(site_file_path)?;
        let reader = BufReader::new(file);
        let site_file: SiteFile = serde_yaml::from_reader(reader)?;

        report.did_read_site_file(&site_file);
        Ok(site_file)
    }
}
