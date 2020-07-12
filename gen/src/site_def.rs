use std::error::Error;
use std::path::PathBuf;

use crate::abs_path::AbsPath;
use crate::content_folder::ContentFolder;
use crate::report::Report;
use crate::site_file::SiteFile;


#[derive(Debug)]
pub struct SiteDef {
    pub content_root: ContentFolder,
    pub name: String,
}

impl SiteDef {
    pub fn read(site_root: &AbsPath, report: &Report) -> Result<SiteDef, Box<dyn Error>> {
        report.will_read_site(&site_root);

        let site_file_path = site_root.join("./_site.yaml");
        let site_file = SiteFile::read(&site_file_path, &report)?;

        let cwd = AbsPath::current_dir().expect("Unable to get current working directory");
        let content_root = ContentFolder::read(&site_root, &cwd, &report)?;

        let site_def = SiteDef {
            content_root,
            name: site_file.name,
        };

        report.did_read_site(&site_def);
        Ok(site_def)
    }
}
