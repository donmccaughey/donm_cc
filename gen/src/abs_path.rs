use std::convert;
use std::default;
use std::env;
use std::fmt;
use std::fs;
use std::io;
use std::ops;
use std::path::Component;
use std::path::Path;
use std::path::PathBuf;


#[derive(Clone, Debug)]
pub struct AbsPath {
    display: String,
    path_buf: PathBuf,
}

impl AbsPath {
    pub fn current_dir() -> io::Result<AbsPath> {
        let cwd = env::current_dir()?;
        Ok(AbsPath {
            display: ".".into(),
            path_buf: cwd,
        })
    }

    pub fn new<P>(path: P) -> io::Result<AbsPath>
        where P: convert::AsRef<Path>
    {
        let cwd = env::current_dir()?;
        Ok(Self::new_relative_to(path, &cwd))
    }

    pub fn new_relative_to_root<P>(path: P, root: &AbsPath) -> AbsPath
        where P: convert::AsRef<Path>
    {
        let path = path.as_ref();
        let display_path_buf = relative_path(&root, path);
        let path_buf = normalize_relative_to(path, root);
        AbsPath {
            display: display_path_buf.to_string_lossy().into(),
            path_buf,
        }
    }

    pub fn new_relative_to<P, U>(path: P, relative_to: U) -> AbsPath
        where P: convert::AsRef<Path>,
              U: convert::AsRef<Path>
    {
        let path = path.as_ref();
        let relative_to = relative_to.as_ref();
        assert!(relative_to.is_absolute());
        let path_buf = normalize_relative_to(path, relative_to);
        AbsPath {
            display: String::from(path.to_string_lossy()),
            path_buf,
        }
    }

    pub fn join<P>(&self, path: P) -> AbsPath
        where P: convert::AsRef<Path>
    {
        // TODO: test and fix up display field
        AbsPath::new_relative_to(path, &self)
    }
}

impl convert::AsRef<Path> for AbsPath {
    fn as_ref(&self) -> &Path {
        &self.path_buf
    }
}

impl convert::From<fs::DirEntry> for AbsPath {
    fn from(dir_entry: fs::DirEntry) -> Self {
        AbsPath::new(&dir_entry.path()).expect("DirEntry path is not absolute")
    }
}

impl default::Default for AbsPath {
    fn default() -> Self {
        let default_path = "/";
        AbsPath {
            display: String::from(default_path),
            path_buf: PathBuf::from(default_path),
        }
    }
}

impl fmt::Display for AbsPath {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.display)
    }
}

impl ops::Deref for AbsPath {
    type Target = Path;

    fn deref(&self) -> &Self::Target {
        &self.path_buf
    }
}


fn normalize_relative_to<P, U>(path: P, relative_to: U) -> PathBuf
    where P: convert::AsRef<Path>,
          U: convert::AsRef<Path>
{
    if path.as_ref().is_absolute() {
        normalize(path)
    } else {
        normalize(&relative_to.as_ref().join(path))
    }
}

fn normalize<P>(path: P) -> PathBuf
    where P: convert::AsRef<Path>
{
    let path = path.as_ref();
    assert!(path.is_absolute());
    // TODO: handle invalid cases like "/../foo"
    let mut components: Vec<Component> = path.components().collect();
    let mut i = components.len() - 1;
    let mut parent_dir_count = 0;
    while i > 0 {
        match components[i] {
            Component::ParentDir => {
                components.remove(i);
                parent_dir_count += 1;
                i -= 1;
            },
            Component::Normal(_) => {
                if parent_dir_count > 0 {
                    components.remove(i);
                    parent_dir_count -= 1;
                }
                i -= 1;
            },
            _ => panic!("Unexpected Component: {:?}", components[i]),
        }
    }
    assert!(parent_dir_count == 0);
    components.iter().collect()
}

fn relative_path<P, U>(root_path: P, other_path: U) -> PathBuf
    where P: convert::AsRef<Path>,
          U: convert::AsRef<Path>
{
    let root_path = root_path.as_ref();
    let other_path = other_path.as_ref();
    assert!(root_path.is_absolute());
    assert!(other_path.is_absolute());
    let root_path_buf = normalize(root_path);
    let other_path_buf = normalize(other_path);
    let root_components: Vec<Component> = root_path_buf.components().collect();
    let other_components: Vec<Component> = other_path_buf.components().collect();

    let mut relative_components: Vec<Component> = Vec::new();
    let first_component = match root_components.len() {
        0 => panic!("Expected root_components to contain at least Component::RootDir"),
        1 => Component::RootDir,
        _ => Component::CurDir,
    };
    relative_components.push(first_component);

    let mut i = 0;
    let mut j = 0;
    while j < other_components.len()
        && i < root_components.len()
        && root_components[i] == other_components[j]
    {
        i += 1;
        j += 1;
    }
    for _ in i .. root_components.len() {
        relative_components.push(Component::ParentDir);
    }
    while j < other_components.len() {
        relative_components.push(other_components[i]);
        i += 1;
        j += 1;
    }

    if relative_components.len() > 1 {
        if let [Component::CurDir, Component::ParentDir] = relative_components[0 ..= 1] {
            relative_components.remove(0);
        }
    }

    relative_components.iter().collect()
}


#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_normalize() {
        assert_eq!(normalize("/foo/bar/baz"), PathBuf::from("/foo/bar/baz"));

        // removes "."

        assert_eq!(normalize("/./foo/bar/baz"), PathBuf::from("/foo/bar/baz"));
        assert_eq!(normalize("/foo/./bar/baz"), PathBuf::from("/foo/bar/baz"));
        assert_eq!(normalize("/foo/bar/./baz"), PathBuf::from("/foo/bar/baz"));
        assert_eq!(normalize("/foo/bar/baz/."), PathBuf::from("/foo/bar/baz"));

        // resolves ".."

        assert_eq!(normalize("/foo/../bar/baz"), PathBuf::from("/bar/baz"));
        assert_eq!(normalize("/foo/bar/../baz"), PathBuf::from("/foo/baz"));
        assert_eq!(normalize("/foo/bar/baz/.."), PathBuf::from("/foo/bar"));
        assert_eq!(normalize("/foo/bar/baz/../.."), PathBuf::from("/foo"));
        assert_eq!(normalize("/foo/bar/baz/../../.."), PathBuf::from("/"));
        assert_eq!(normalize("/foo/../bar/../baz/.."), PathBuf::from("/"));
        assert_eq!(normalize("/foo/../bar/baz/.."), PathBuf::from("/bar"));
        assert_eq!(normalize("/foo/bar/baz/../../../one/two"), PathBuf::from("/one/two"));
        assert_eq!(normalize("/foo/bar/baz/../../../one/two/3/../../../do/re/mi"), PathBuf::from("/do/re/mi"));
    }

    #[test]
    fn test_new_for_abs_path() {
        let abs_path = AbsPath::new("/foo/bar");
        assert!(abs_path.is_ok());
        let abs_path = abs_path.unwrap();
        assert_eq!(abs_path.path_buf, PathBuf::from("/foo/bar"));
        assert_eq!(abs_path.display, "/foo/bar");
    }

    #[test]
    fn test_new_for_relative_path() {
        let abs_path = AbsPath::new("./foo/bar");
        let cwd = env::current_dir().unwrap();
        assert!(abs_path.is_ok());
        let abs_path = abs_path.unwrap();
        assert!(abs_path.path_buf.starts_with(cwd));
        assert!(abs_path.path_buf.ends_with("foo/bar"));
        assert!(abs_path.path_buf.to_string_lossy().ends_with("/foo/bar"));
        assert!(!abs_path.path_buf.to_string_lossy().ends_with("./foo/bar"));
        assert_eq!(abs_path.display, "./foo/bar");
    }

    #[test]
    fn test_new_relative_to_for_abs_path() {
        let abs_path = AbsPath::new_relative_to("/foo/bar", "/usr/local");
        assert_eq!(abs_path.path_buf, PathBuf::from("/foo/bar"));
        assert_eq!(abs_path.display, "/foo/bar");
    }

    #[test]
    fn test_new_relative_to_for_relative_path() {
        let abs_path = AbsPath::new_relative_to("./foo/bar", "/usr/local");
        assert_eq!(abs_path.path_buf, PathBuf::from("/usr/local/foo/bar"));
        assert_eq!(abs_path.display, "./foo/bar");
    }

    #[test]
    fn test_relative_path() {
        // same path
        assert_eq!(relative_path("/foo/bar", "/foo/bar"), PathBuf::from("."));
        // child path
        assert_eq!(relative_path("/foo/bar", "/foo/bar/baz"), PathBuf::from("./baz"));
        // sibling paths
        assert_eq!(relative_path("/foo/bar/baz", "/foo/bar/fid"), PathBuf::from("../fid"));
        assert_eq!(relative_path("/foo", "/do"), PathBuf::from("../do"));
        assert_eq!(relative_path("/foo/bar", "/do/re"), PathBuf::from("../../do/re"));
        assert_eq!(relative_path("/foo/bar/baz", "/do/re/mi/fa"), PathBuf::from("../../../do/re/mi/fa"));
        // relative to root
        assert_eq!(relative_path("/", "/foo/bar/baz"), PathBuf::from("/foo/bar/baz"));
        assert_eq!(relative_path("/", "/"), PathBuf::from("/"));
    }
}
