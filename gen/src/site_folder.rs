use crate::abs_path::AbsPath;


#[derive(Debug)]
pub struct SiteFolder {
    pub abs_path: AbsPath,
    pub folders: Vec<SiteFolder>,
}

impl SiteFolder {
    // pub fn new(content_folder: &ContentFolder, content_root: &AbsPath, output_dir: &AbsPath, working_dir: &AbsPath, report: &Report)
    //     -> SiteFolder
    // {
    //
    // }
}
