use std::error::Error;
use std::fs;

use crate::abs_path::AbsPath;
use crate::error::Error::NotADirectory;
use crate::report::Report;


#[derive(Debug)]
pub struct ContentFolder {
    pub abs_path: AbsPath,
    pub folders: Vec<ContentFolder>,
}

impl ContentFolder {
    pub fn read(abs_path: &AbsPath, working_dir: &AbsPath, report: &Report) -> Result<ContentFolder, Box<dyn Error>> {
        report.will_scan_content_folder(&abs_path);

        let metadata = fs::metadata(&abs_path)?;
        if !metadata.is_dir() {
            return Err(Box::new(NotADirectory(abs_path.clone())));
        }

        let mut folders = Vec::new();
        for dir_entry in fs::read_dir(&abs_path)? {
            let dir_entry = dir_entry?;
            let metadata = dir_entry.metadata()?;
            if metadata.is_dir() {
                let abs_path = AbsPath::new_relative_to_root(&dir_entry.path(), working_dir);
                let folder = ContentFolder::read(&abs_path, working_dir, &report)?;
                folders.push(folder);
            }
        }

        let folder = ContentFolder {
            abs_path: abs_path.clone(),
            folders,
        };

        report.did_scan_content_folder(&folder);

        Ok(folder)
    }
}
