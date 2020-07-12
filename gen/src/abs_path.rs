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

    pub fn new(path: &Path) -> io::Result<AbsPath> {
        let cwd = env::current_dir()?;
        Ok(Self::new_relative_to(path, &cwd))
    }

    pub fn new_relative_to_root(path: &Path, root: &AbsPath) -> AbsPath {
        let display_path_buf = relative_path(&root, path);
        let path_buf = normalize_relative_to(path, root);
        AbsPath {
            display: display_path_buf.to_string_lossy().into(),
            path_buf,
        }
    }

    pub fn new_relative_to(path: &Path, relative_to: &Path) -> AbsPath {
        assert!(relative_to.is_absolute());
        let path_buf = normalize_relative_to(path, relative_to);
        AbsPath {
            display: String::from(path.to_string_lossy()),
            path_buf,
        }
    }

    pub fn join(&self, path: &Path) -> AbsPath {
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


fn normalize_relative_to(path: &Path, relative_to: &Path) -> PathBuf {
    if path.is_absolute() {
        normalize(path)
    } else {
        normalize(&relative_to.join(path))
    }
}

fn normalize(path: &Path) -> PathBuf {
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

fn relative_path(root_path: &Path, other_path: &Path) -> PathBuf {
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
    while j < other_components.len() {
        if i < root_components.len() && root_components[i] == other_components[j] {
            i += 1;
            j += 1;
            continue;
        }
        for _ in i .. root_components.len() {
            relative_components.push(Component::ParentDir);
        }
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
        let path_buf = PathBuf::from("/foo/bar/baz");
        assert_eq!(normalize(&path_buf), path_buf);

        // removes "."

        let path_buf = PathBuf::from("/./foo/bar/baz");
        assert_eq!(normalize(&path_buf), PathBuf::from("/foo/bar/baz"));

        let path_buf = PathBuf::from("/foo/./bar/baz");
        assert_eq!(normalize(&path_buf), PathBuf::from("/foo/bar/baz"));

        let path_buf = PathBuf::from("/foo/bar/./baz");
        assert_eq!(normalize(&path_buf), PathBuf::from("/foo/bar/baz"));

        let path_buf = PathBuf::from("/foo/bar/baz/.");
        assert_eq!(normalize(&path_buf), PathBuf::from("/foo/bar/baz"));

        // resolves ".."

        let path_buf = PathBuf::from("/foo/../bar/baz");
        assert_eq!(normalize(&path_buf), PathBuf::from("/bar/baz"));

        let path_buf = PathBuf::from("/foo/bar/../baz");
        assert_eq!(normalize(&path_buf), PathBuf::from("/foo/baz"));

        let path_buf = PathBuf::from("/foo/bar/baz/..");
        assert_eq!(normalize(&path_buf), PathBuf::from("/foo/bar"));

        let path_buf = PathBuf::from("/foo/bar/baz/../..");
        assert_eq!(normalize(&path_buf), PathBuf::from("/foo"));

        let path_buf = PathBuf::from("/foo/bar/baz/../../..");
        assert_eq!(normalize(&path_buf), PathBuf::from("/"));

        let path_buf = PathBuf::from("/foo/../bar/../baz/..");
        assert_eq!(normalize(&path_buf), PathBuf::from("/"));

        let path_buf = PathBuf::from("/foo/../bar/baz/..");
        assert_eq!(normalize(&path_buf), PathBuf::from("/bar"));
    }

    #[test]
    fn test_new_for_abs_path() {
        let abs_path = AbsPath::new(&PathBuf::from("/foo/bar"));
        assert!(abs_path.is_ok());
        let abs_path = abs_path.unwrap();
        assert_eq!(PathBuf::from("/foo/bar"), abs_path.path_buf);
        assert_eq!("/foo/bar", abs_path.display);
    }

    #[test]
    fn test_new_for_relative_path() {
        let abs_path = AbsPath::new(&PathBuf::from("./foo/bar"));
        let cwd = env::current_dir().unwrap();
        assert!(abs_path.is_ok());
        let abs_path = abs_path.unwrap();
        assert!(abs_path.path_buf.starts_with(cwd));
        assert!(abs_path.path_buf.ends_with("foo/bar"));
        assert!(abs_path.path_buf.to_string_lossy().ends_with("/foo/bar"));
        assert!(!abs_path.path_buf.to_string_lossy().ends_with("./foo/bar"));
        assert_eq!("./foo/bar", abs_path.display);
    }

    #[test]
    fn test_new_relative_to_for_abs_path() {
        let abs_path = AbsPath::new_relative_to(&PathBuf::from("/foo/bar"), &PathBuf::from("/usr/local"));
        assert_eq!(PathBuf::from("/foo/bar"), abs_path.path_buf);
        assert_eq!("/foo/bar", abs_path.display);
    }

    #[test]
    fn test_new_relative_to_for_relative_path() {
        let abs_path = AbsPath::new_relative_to(&PathBuf::from("./foo/bar"), &PathBuf::from("/usr/local"));
        assert_eq!(PathBuf::from("/usr/local/foo/bar"), abs_path.path_buf);
        assert_eq!("./foo/bar", abs_path.display);
    }

    #[test]
    fn test_relative_path_for_child_path() {
        let root_path = PathBuf::from("/foo/bar");
        let other_path = PathBuf::from("/foo/bar/baz");
        let relative_path = relative_path(&root_path, &other_path);
        assert_eq!(relative_path, PathBuf::from("./baz"));
    }

    #[test]
    fn test_relative_path_for_sibling_path() {
        let root_path = PathBuf::from("/foo/bar/baz");
        let other_path = PathBuf::from("/foo/bar/fid");
        let relative_path = relative_path(&root_path, &other_path);
        assert_eq!(relative_path, PathBuf::from("../fid"));
    }

    #[test]
    fn test_relative_path_for_root() {
        let root_path = PathBuf::from("/");
        let other_path = PathBuf::from("/foo/bar/baz");
        let relative_path = relative_path(&root_path, &other_path);
        assert_eq!(relative_path, PathBuf::from("/foo/bar/baz"));
    }

    #[test]
    fn test_relative_path_for_root_to_root() {
        let root_path = PathBuf::from("/");
        let other_path = PathBuf::from("/");
        let relative_path = relative_path(&root_path, &other_path);
        assert_eq!(relative_path, PathBuf::from("/"));
    }
}
