use std::fs;
use std::path::{Path, PathBuf};
use pulldown_cmark::{html, Options, Parser};
use regex::Regex;

#[derive(Debug, serde::Deserialize)]
struct FrontMatter {
    title: Option<String>,
}

#[derive(Debug, serde::Deserialize)]
struct Config {
    page_order: Option<Vec<serde_yaml::Value>>,
    navbar_order: Option<Vec<serde_yaml::Value>>,  // New: allows manual ordering including dropdowns
    dropdowns: Option<std::collections::HashMap<String, serde_yaml::Value>>,
}

fn extract_frontmatter(content: &str) -> (Option<FrontMatter>, &str) {
    if content.starts_with("---\n") {
        if let Some(end) = content[4..].find("---\n") {
            let frontmatter_str = &content[4..end + 4];
            let markdown_content = &content[end + 8..];
            
            match serde_yaml::from_str::<FrontMatter>(frontmatter_str) {
                Ok(fm) => (Some(fm), markdown_content),
                Err(_) => (None, content),
            }
        } else {
            (None, content)
        }
    } else {
        (None, content)
    }
}

fn protect_math_expressions(markdown: &str) -> (String, Vec<String>) {
    let mut protected = markdown.to_string();
    let mut math_blocks = Vec::new();
    let mut block_id = 0;
    
    // Protect display math blocks: $$...$$
    let display_dollar_pattern = Regex::new(r"\$\$[\s\S]*?\$\$").unwrap();
    let mut positions: Vec<(usize, usize, String)> = Vec::new();
    
    for mat in display_dollar_pattern.find_iter(&protected) {
        positions.push((mat.start(), mat.end(), mat.as_str().to_string()));
    }
    
    // Replace from end to start to preserve indices
    for (start, end, math_content) in positions.iter().rev() {
        let placeholder = format!("\n\nMATH_BLOCK_{}\n\n", block_id);
        math_blocks.push(math_content.clone());
        protected.replace_range(*start..*end, &placeholder);
        block_id += 1;
    }
    
    // Protect display math blocks: \[...\]
    let display_bracket_pattern = Regex::new(r"\\\[[\s\S]*?\\\]").unwrap();
    let mut positions: Vec<(usize, usize, String)> = Vec::new();
    
    for mat in display_bracket_pattern.find_iter(&protected) {
        positions.push((mat.start(), mat.end(), mat.as_str().to_string()));
    }
    
    // Replace from end to start to preserve indices
    for (start, end, math_content) in positions.iter().rev() {
        let placeholder = format!("\n\nMATH_BLOCK_{}\n\n", block_id);
        math_blocks.push(math_content.clone());
        protected.replace_range(*start..*end, &placeholder);
        block_id += 1;
    }
    
    // Protect inline math: $...$ (but not $$)
    // Use a simple pattern and filter out $$ matches manually
    let inline_pattern = Regex::new(r"\$[^$\n]+?\$").unwrap();
    let mut inline_positions: Vec<(usize, usize, String)> = Vec::new();
    
    for mat in inline_pattern.find_iter(&protected) {
        let math_str = mat.as_str();
        // Skip if it starts with $$ (already handled as display math)
        if !math_str.starts_with("$$") {
            inline_positions.push((mat.start(), mat.end(), math_str.to_string()));
        }
    }
    
    // Replace from end to start
    for (start, end, math_content) in inline_positions.iter().rev() {
        let placeholder = format!("MATH_INLINE_{}", block_id);
        math_blocks.push(math_content.clone());
        protected.replace_range(*start..*end, &placeholder);
        block_id += 1;
    }
    
    (protected, math_blocks)
}

fn restore_math_expressions(html: &str, math_blocks: &[String]) -> String {
    let mut result = html.to_string();
    
    // Process in reverse order to preserve indices
    for (i, math_block) in math_blocks.iter().enumerate().rev() {
        let placeholder = if math_block.starts_with("$$") || math_block.starts_with("\\[") {
            format!("MATH_BLOCK_{}", i)
        } else {
            format!("MATH_INLINE_{}", i)
        };
        
        // For display math, remove paragraph wrapping if present
        if math_block.starts_with("$$") || math_block.starts_with("\\[") {
            // Try various patterns that might wrap the math
            let patterns = vec![
                format!("<p>{}</p>", placeholder),
                format!("<p>\n{}\n</p>", placeholder),
                format!("{}\n", placeholder),
                format!("\n{}\n", placeholder),
                format!("\n\n{}\n\n", placeholder),
                placeholder.clone(),
            ];
            
            let mut replaced = false;
            for pattern in &patterns {
                if result.contains(pattern) {
                    result = result.replace(pattern, &math_block);
                    replaced = true;
                    break;
                }
            }
            
            if !replaced {
                result = result.replace(&placeholder, &math_block);
            }
        } else {
            // For inline math, just replace the placeholder
            result = result.replace(&placeholder, math_block);
        }
    }
    
    result
}

fn convert_internal_links(html: &str, markdown_files: &std::collections::HashSet<String>) -> String {
    // Create a regex to match <a href="..."> tags
    let link_pattern = Regex::new(r#"<a\s+href="([^"]+)"([^>]*)>"#).unwrap();
    let mut result = html.to_string();
    
    // Find all matches and replace from end to start to preserve indices
    let mut replacements: Vec<(usize, usize, String)> = Vec::new();
    
    for cap in link_pattern.captures_iter(html) {
        let full_match = cap.get(0).unwrap();
        let href = cap.get(1).unwrap().as_str();
        let attrs = cap.get(2).unwrap().as_str();
        
        // Skip external links (http, https, mailto, etc.)
        if href.starts_with("http://") || href.starts_with("https://") || 
           href.starts_with("mailto:") || href.starts_with("#") ||
           href.starts_with("/") || href.contains("://") {
            continue;
        }
        
        // Split href into base and fragment/query
        let (base_href, fragment_query) = if let Some(pos) = href.find('#') {
            let (base, rest) = href.split_at(pos);
            (base, Some(rest))
        } else if let Some(pos) = href.find('?') {
            let (base, rest) = href.split_at(pos);
            (base, Some(rest))
        } else {
            (href, None)
        };
        
        let new_href = if base_href.ends_with(".md") {
            // Replace .md with .html
            let mut new = base_href.replace(".md", ".html");
            if let Some(fq) = fragment_query {
                new.push_str(fq);
            }
            new
        } else if !base_href.contains('.') && markdown_files.contains(base_href) {
            // Add .html extension for known markdown files
            let mut new = format!("{}.html", base_href);
            if let Some(fq) = fragment_query {
                new.push_str(fq);
            }
            new
        } else {
            // Not an internal link, skip
            continue;
        };
        
        let new_link = format!(r#"<a href="{}"{}>"#, new_href, attrs);
        replacements.push((full_match.start(), full_match.end(), new_link));
    }
    
    // Replace from end to start to preserve indices
    for (start, end, replacement) in replacements.iter().rev() {
        result.replace_range(*start..*end, replacement);
    }
    
    result
}

fn markdown_to_html(markdown: &str, markdown_files: &std::collections::HashSet<String>) -> String {
    let (protected_markdown, math_blocks) = protect_math_expressions(markdown);
    
    let options = Options::all();
    let parser = Parser::new_ext(&protected_markdown, options);
    let mut html_output = String::new();
    html::push_html(&mut html_output, parser);
    
    let html_with_math = restore_math_expressions(&html_output, &math_blocks);
    convert_internal_links(&html_with_math, markdown_files)
}

#[derive(Clone)]
enum NavbarItem {
    MarkdownFile(PathBuf, String),  // (path, title)
    ExternalLink(String, String),   // (url, text)
    Dropdown(String),                // (dropdown name)
}

fn generate_navbar(
    navbar_items: &[NavbarItem], 
    output_in_dist: bool,
    dropdowns: Option<&std::collections::HashMap<String, serde_yaml::Value>>,
    markdown_titles: &std::collections::HashMap<String, String>,
    current_page: Option<&str>,
) -> String {
    let mut nav = String::from("<nav style=\"background: #000; padding: 10px; margin-bottom: 20px; border-bottom: 2px solid #333;\">\n");
    nav.push_str("<style>
.dropdown {
    position: relative;
    display: inline-block;
}
.dropdown-content {
    display: none;
    position: absolute;
    background-color: #222;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.5);
    z-index: 1000;
    top: 100%;
    left: 0;
    margin-top: 0;
    padding-top: 5px;
    border: 1px solid #444;
}
.dropdown:hover .dropdown-content,
.dropdown-content:hover {
    display: block;
}
.dropdown-content::before {
    content: '';
    position: absolute;
    top: -5px;
    left: 0;
    right: 0;
    height: 5px;
    background: transparent;
}
.dropdown-content a {
    color: #fff;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    white-space: nowrap;
}
.dropdown-content a:link {
    color: #fff;
    text-decoration: none;
}
.dropdown-content a:visited {
    color: #fff;
    text-decoration: none;
}
.dropdown-content a:hover {
    background-color: #333;
    color: #8C6D2C;
    text-decoration: none;
}
.dropdown-content a:active {
    color: #fff;
    text-decoration: none;
}
.dropdown > a {
    color: #fff;
    text-decoration: none;
    font-weight: bold;
    cursor: pointer;
    padding: 5px 0;
    display: block;
    font-family: Arial, sans-serif;
    font-size: 1.25rem;
}
.nav-link {
    color: #fff;
    text-decoration: none;
    font-weight: bold;
    font-family: Arial, sans-serif;
    font-size: 1.25rem;
}
.nav-link:link {
    color: #fff;
    text-decoration: none;
}
.nav-link:visited {
    color: #fff;
    text-decoration: none;
}
.nav-link:hover {
    color: #8C6D2C;
    text-decoration: none;
}
.nav-link:active {
    color: #fff;
    text-decoration: none;
}
.nav-link.active {
    color: #8C6D2C !important;
    text-decoration: none;
}
.nav-link.active:visited {
    color: #8C6D2C !important;
    text-decoration: none;
}
.nav-link.active:hover {
    color: #8C6D2C !important;
    text-decoration: none;
}
</style>\n");
    nav.push_str("<ul style=\"list-style: none; margin: 0; padding: 0; display: flex; gap: 20px; align-items: center; font-size: 1.25rem;\">\n");
    
    // Always add logo/IDEEP link at the start
    let index_title = markdown_titles.get("index")
        .cloned()
        .unwrap_or_else(|| "IDEEP".to_string());
    let index_is_active = current_page.map(|cp| cp == "index").unwrap_or(false);
    let index_link_class = if index_is_active { "nav-link active" } else { "nav-link" };
    nav.push_str(&format!(
        "  <li><a href=\"index.html\" class=\"{}\" style=\"display: flex; align-items: center; gap: 10px;\"><img src=\"assets/logo-wide.png\" alt=\"Logo\" style=\"height: 40px; width: auto;\">{}</a></li>\n",
        index_link_class, index_title
    ));
    
    for item in navbar_items {
        match item {
            NavbarItem::MarkdownFile(path, title) => {
                let html_name = path.file_stem()
                    .and_then(|s| s.to_str())
                    .unwrap_or("index");
                let html_path = if output_in_dist {
                    format!("{}.html", html_name)
                } else {
                    format!("{}.html", html_name)
                };
                // Skip index since we already added it with logo at the start
                if html_name == "index" {
                    continue;
                }
                
                let is_active = current_page.map(|cp| cp == html_name).unwrap_or(false);
                let link_class = if is_active { "nav-link active" } else { "nav-link" };
                
                nav.push_str(&format!(
                    "  <li><a href=\"{}\" class=\"{}\">{}</a></li>\n",
                    html_path, link_class, title
                ));
            }
            NavbarItem::ExternalLink(url, text) => {
                nav.push_str(&format!(
                    "  <li><a href=\"{}\" class=\"nav-link\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a></li>\n",
                    url, text
                ));
            }
            NavbarItem::Dropdown(dropdown_name) => {
                // Render dropdown inline
                if let Some(dropdowns_map) = dropdowns {
                    if let Some(dropdown_value) = dropdowns_map.get(dropdown_name) {
                        nav.push_str("  <li class=\"dropdown\">\n");
                        nav.push_str(&format!("    <a>{}</a>\n", dropdown_name));
                        nav.push_str("    <div class=\"dropdown-content\">\n");
                        
                        // Handle different dropdown value types
                        match dropdown_value {
                            serde_yaml::Value::Mapping(map) => {
                                // For mappings like Syllabi: {index: url, stuff: url}
                                for (key, value) in map {
                                    let page_name = key.as_str().unwrap_or("");
                                    let url = value.as_str().unwrap_or("");
                                    let display_title = markdown_titles.get(page_name)
                                        .cloned()
                                        .unwrap_or_else(|| page_name.to_string());
                                    nav.push_str(&format!(
                                        "      <a href=\"{}\">{}</a>\n",
                                        url, display_title
                                    ));
                                }
                            }
                            serde_yaml::Value::Sequence(seq) => {
                                // For sequences like Resources: [math, programming] or [{url: "...", text: "..."}]
                                for item in seq {
                                    match item {
                                        serde_yaml::Value::String(page_name) => {
                                            // Simple string - treat as markdown file name
                                            let html_path = format!("{}.html", page_name);
                                            let display_title = markdown_titles.get(page_name)
                                                .cloned()
                                                .unwrap_or_else(|| page_name.clone());
                                            nav.push_str(&format!(
                                                "      <a href=\"{}\">{}</a>\n",
                                                html_path, display_title
                                            ));
                                        }
                                        serde_yaml::Value::Mapping(map) => {
                                            // Object with url and text fields
                                            let url = map.get(&serde_yaml::Value::String("url".to_string()))
                                                .and_then(|v| v.as_str())
                                                .unwrap_or("");
                                            let text = map.get(&serde_yaml::Value::String("text".to_string()))
                                                .and_then(|v| v.as_str())
                                                .unwrap_or("");
                                            if !url.is_empty() && !text.is_empty() {
                                                nav.push_str(&format!(
                                                    "      <a href=\"{}\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a>\n",
                                                    url, text
                                                ));
                                            }
                                        }
                                        _ => {}
                                    }
                                }
                            }
                            _ => {}
                        }
                        
                        nav.push_str("    </div>\n");
                        nav.push_str("  </li>\n");
                    }
                }
            }
        }
    }
    
    nav.push_str("</ul>\n</nav>\n");
    nav
}

fn generate_html(title: &str, content: &str, navbar: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mathjax_config = r#"<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [['$','$'], ['\\(','\\)']],
    displayMath: [['$$','$$'], ['\\[','\\]']],
    processEscapes: true
  }
});
</script>
<script src="assets/tex-svg.js" id="MathJax-script"></script>
<script>
window.addEventListener('load', function() {
    if (typeof MathJax !== 'undefined' && MathJax.Hub) {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    }
});
</script>"#;

    // Read footer.html
    let footer_path = Path::new("assets/footer.html");
    let footer_content = if footer_path.exists() {
        fs::read_to_string(footer_path)?
    } else {
        String::new()
    };

    Ok(format!(
        r#"<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
    <link rel="icon" type="image/png" href="assets/logo.png" />
    <link rel="stylesheet" href="assets/styles.css" type="text/css" />
    <script src="https://kit.fontawesome.com/1ffe760482.js" crossorigin="anonymous"></script>
    <style>
    body {{
        font-family: Arial, sans-serif;
        padding-bottom: 0;
        margin-bottom: 0;
    }}
    h1 {{
        font-family: Garamond, serif;
    }}
    #content {{
        font-family: Arial, sans-serif;
        margin-bottom: 40px;
    }}
    .blogbody {{
        font-family: Arial, sans-serif;
        padding-bottom: 20px;
    }}
    
    /* Mobile responsive styles */
    @media screen and (max-width: 768px) {{
        #content {{
            margin-left: 10px;
            margin-right: 10px;
            width: calc(100% - 20px);
            padding: 10px;
        }}
        
        nav ul {{
            flex-direction: column;
            gap: 10px !important;
            align-items: flex-start !important;
        }}
        
        nav li {{
            width: 100%;
        }}
        
        .nav-link {{
            display: block;
            padding: 10px 0;
        }}
        
        .dropdown {{
            width: 100%;
        }}
        
        .dropdown > a {{
            width: 100%;
            padding: 10px 0;
        }}
        
        .dropdown-content {{
            position: relative;
            width: 100%;
            box-shadow: none;
            border: none;
            margin-top: 5px;
        }}
        
        .blogbody {{
            font-size: 0.9rem;
            line-height: 1.6;
        }}
        
        h1 {{
            font-size: 1.8rem;
        }}
        
        h2 {{
            font-size: 1.4rem;
        }}
        
        h3 {{
            font-size: 1.2rem;
        }}
    }}
    
    @media screen and (max-width: 480px) {{
        nav {{
            padding: 5px;
        }}
        
        nav ul {{
            font-size: 1rem !important;
        }}
        
        .nav-link img {{
            height: 30px !important;
        }}
        
        #content {{
            margin-left: 5px;
            margin-right: 5px;
            width: calc(100% - 10px);
            padding: 5px;
        }}
        
        .blogbody {{
            font-size: 0.85rem;
        }}
        
        h1 {{
            font-size: 1.5rem;
        }}
    }}
    </style>
    {}
</head>
<body>
    {}
    <div id="content">
        <div class="blogbody">
            {}
        </div>
    </div>
    {}
</body>
</html>"#,
        title, mathjax_config, navbar, content, footer_content
    ))
}

fn copy_assets_to_dist() -> Result<(), Box<dyn std::error::Error>> {
    let assets_dir = Path::new("assets");
    let dist_assets_dir = Path::new("dist/assets");
    
    // Create dist/assets directory if it doesn't exist
    if !dist_assets_dir.exists() {
        fs::create_dir_all(dist_assets_dir)?;
    }
    
    // Copy all files from assets to dist/assets
    if assets_dir.exists() {
        for entry in fs::read_dir(assets_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() {
                let filename = path.file_name().unwrap();
                let dest_path = dist_assets_dir.join(filename);
                fs::copy(&path, &dest_path)?;
                println!("Copied: {} -> {}", path.display(), dest_path.display());
            }
        }
    }
    
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let content_dir = Path::new("content");
    let dist_dir = Path::new("dist");
    
    // Create content directory if it doesn't exist
    if !content_dir.exists() {
        fs::create_dir_all(content_dir)?;
    }
    
    // Create dist directory if it doesn't exist
    if !dist_dir.exists() {
        fs::create_dir_all(dist_dir)?;
    }
    
    let mut markdown_files: Vec<(PathBuf, String)> = Vec::new();

    // Find all markdown files in content directory
    if content_dir.exists() {
        for entry in fs::read_dir(content_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("md") {
                // Skip README.md files (case-insensitive)
                if let Some(filename) = path.file_stem().and_then(|s| s.to_str()) {
                    if filename.eq_ignore_ascii_case("README") {
                        continue;
                    }
                }
                
                let content = fs::read_to_string(&path)?;
                
                // Skip files that are already HTML (not markdown)
                if content.trim_start().starts_with("<!DOCTYPE") || content.trim_start().starts_with("<html") {
                    continue;
                }
                
                let (frontmatter, _) = extract_frontmatter(&content);
                let title = frontmatter
                    .and_then(|fm| fm.title)
                    .unwrap_or_else(|| {
                        path.file_stem()
                            .and_then(|s| s.to_str())
                            .unwrap_or("Untitled")
                            .to_string()
                    });
                markdown_files.push((path.clone(), title));
            }
        }
    }

    // Build a map of markdown file names to titles
    let mut markdown_titles: std::collections::HashMap<String, String> = std::collections::HashMap::new();
    for (path, title) in &markdown_files {
        let filename = path.file_stem()
            .and_then(|s| s.to_str())
            .unwrap_or("");
        markdown_titles.insert(filename.to_string(), title.clone());
    }

    // Load config file if it exists
    let config_path = Path::new("config.yaml");
    let (page_order, navbar_order, dropdowns) = if config_path.exists() {
        match fs::read_to_string(config_path) {
            Ok(content) => {
                match serde_yaml::from_str::<Config>(&content) {
                    Ok(config) => (config.page_order, config.navbar_order, config.dropdowns),
                    Err(e) => {
                        eprintln!("Warning: Failed to parse config.yaml: {}", e);
                        (None, None, None)
                    }
                }
            }
            Err(e) => {
                eprintln!("Warning: Failed to read config.yaml: {}", e);
                (None, None, None)
            }
        }
    } else {
        (None, None, None)
    };

    // Sort markdown files according to config or alphabetically
    if let Some(ref order) = page_order {
        // Separate index from other pages
        let mut index_file: Option<(PathBuf, String)> = None;
        let mut other_files: Vec<(PathBuf, String)> = Vec::new();
        
        for file in markdown_files {
            let filename = file.0.file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("");
            if filename == "index" {
                index_file = Some(file);
            } else {
                other_files.push(file);
            }
        }
        
        // Sort other files according to config order
        other_files.sort_by(|a, b| {
            let a_name = a.0.file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("");
            let b_name = b.0.file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("");
            
            let a_pos = order.iter().position(|x| {
                if let Some(page_name) = x.as_str() {
                    page_name == a_name
                } else {
                    false
                }
            });
            let b_pos = order.iter().position(|x| {
                if let Some(page_name) = x.as_str() {
                    page_name == b_name
                } else {
                    false
                }
            });
            
            match (a_pos, b_pos) {
                (Some(a_idx), Some(b_idx)) => a_idx.cmp(&b_idx),
                (Some(_), None) => std::cmp::Ordering::Less,
                (None, Some(_)) => std::cmp::Ordering::Greater,
                (None, None) => a_name.cmp(b_name), // Alphabetical fallback for unlisted files
            }
        });
        
        // Reconstruct with index first
        let mut sorted_files = Vec::new();
        if let Some(index) = index_file {
            sorted_files.push(index);
        }
        sorted_files.extend(other_files);
        markdown_files = sorted_files;
    } else {
        // Default: sort alphabetically, but keep index first
        markdown_files.sort_by(|a, b| {
            let a_name = a.0.file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("");
            let b_name = b.0.file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("");
            
            match (a_name == "index", b_name == "index") {
                (true, false) => std::cmp::Ordering::Less,
                (false, true) => std::cmp::Ordering::Greater,
                _ => a_name.cmp(b_name),
            }
        });
    }

    // Filter out pages that are in sequence dropdowns (like Resources) from the regular navbar
    // Pages in mapping dropdowns (like Syllabi) should still appear in navbar
    let mut pages_in_dropdowns: std::collections::HashSet<String> = std::collections::HashSet::new();
    if let Some(ref dropdowns_map) = dropdowns {
        for dropdown_value in dropdowns_map.values() {
            match dropdown_value {
                serde_yaml::Value::Sequence(seq) => {
                    // For sequences (like Resources), the items are page names that should be hidden
                    for item in seq {
                        if let Some(page_name) = item.as_str() {
                            pages_in_dropdowns.insert(page_name.to_string());
                        }
                    }
                }
                // For mappings (like Syllabi), we don't hide the pages - they're just for linking to syllabi
                _ => {}
            }
        }
    }
    
    // Build navbar items from navbar_order, page_order, or markdown files
    let mut navbar_items: Vec<NavbarItem> = Vec::new();
    
    if let Some(ref order) = navbar_order {
        // Use navbar_order if specified - allows full control including dropdowns
        for item in order {
            match item {
                serde_yaml::Value::String(page_name) => {
                    // Check if it's a dropdown name
                    if let Some(ref dropdowns_map) = dropdowns {
                        if dropdowns_map.contains_key(page_name) {
                            navbar_items.push(NavbarItem::Dropdown(page_name.clone()));
                            continue;
                        }
                    }
                    // Otherwise treat as markdown file name
                    if let Some((path, title)) = markdown_files.iter()
                        .find(|(p, _)| {
                            p.file_stem()
                                .and_then(|s| s.to_str())
                                .map(|s| s == page_name)
                                .unwrap_or(false)
                        })
                        .cloned()
                    {
                        let filename = path.file_stem()
                            .and_then(|s| s.to_str())
                            .unwrap_or("");
                        // Skip index (already added with logo)
                        if filename != "index" {
                            navbar_items.push(NavbarItem::MarkdownFile(path, title));
                        }
                    }
                }
                serde_yaml::Value::Mapping(map) => {
                    // Check for dropdown reference
                    if let Some(dropdown_name) = map.get(&serde_yaml::Value::String("dropdown".to_string()))
                        .and_then(|v| v.as_str())
                    {
                        navbar_items.push(NavbarItem::Dropdown(dropdown_name.to_string()));
                    }
                    // Check for external link
                    else {
                        let url = map.get(&serde_yaml::Value::String("url".to_string()))
                            .and_then(|v| v.as_str())
                            .map(|s| s.to_string());
                        let text = map.get(&serde_yaml::Value::String("text".to_string()))
                            .and_then(|v| v.as_str())
                            .map(|s| s.to_string());
                        if let (Some(url), Some(text)) = (url, text) {
                            navbar_items.push(NavbarItem::ExternalLink(url, text));
                        }
                    }
                }
                _ => {}
            }
        }
    } else if let Some(ref order) = page_order {
        // Fall back to page_order if navbar_order not specified
        for item in order {
            match item {
                serde_yaml::Value::String(page_name) => {
                    // Simple string - find matching markdown file
                    if let Some((path, title)) = markdown_files.iter()
                        .find(|(p, _)| {
                            p.file_stem()
                                .and_then(|s| s.to_str())
                                .map(|s| s == page_name)
                                .unwrap_or(false)
                        })
                        .cloned()
                    {
                        let filename = path.file_stem()
                            .and_then(|s| s.to_str())
                            .unwrap_or("");
                        // Only add if not in dropdowns (but always include index)
                        if filename == "index" || !pages_in_dropdowns.contains(filename) {
                            navbar_items.push(NavbarItem::MarkdownFile(path, title));
                        }
                    }
                }
                serde_yaml::Value::Mapping(map) => {
                    // Object with url and text fields
                    let url = map.get(&serde_yaml::Value::String("url".to_string()))
                        .and_then(|v| v.as_str())
                        .map(|s| s.to_string());
                    let text = map.get(&serde_yaml::Value::String("text".to_string()))
                        .and_then(|v| v.as_str())
                        .map(|s| s.to_string());
                    if let (Some(url), Some(text)) = (url, text) {
                        navbar_items.push(NavbarItem::ExternalLink(url, text));
                    }
                }
                _ => {}
            }
        }
        // Add dropdowns at the end if using page_order
        if let Some(ref dropdowns_map) = dropdowns {
            for dropdown_name in dropdowns_map.keys() {
                navbar_items.push(NavbarItem::Dropdown(dropdown_name.clone()));
            }
        }
    } else {
        // Default: use all markdown files (filtered), then dropdowns
        for (path, title) in &markdown_files {
            let filename = path.file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("");
            if filename == "index" || !pages_in_dropdowns.contains(filename) {
                navbar_items.push(NavbarItem::MarkdownFile(path.clone(), title.clone()));
            }
        }
        // Add dropdowns at the end
        if let Some(ref dropdowns_map) = dropdowns {
            for dropdown_name in dropdowns_map.keys() {
                navbar_items.push(NavbarItem::Dropdown(dropdown_name.clone()));
            }
        }
    }

    // Build a HashSet of markdown file names (without extension) for link conversion
    let markdown_file_names: std::collections::HashSet<String> = markdown_files.iter()
        .map(|(path, _)| {
            path.file_stem()
                .and_then(|s| s.to_str())
                .map(|s| s.to_string())
                .unwrap_or_default()
        })
        .collect();

    // Process each markdown file
    for (path, title) in &markdown_files {
        let content = fs::read_to_string(path)?;
        let (_, markdown_content) = extract_frontmatter(&content);
        let html_content = markdown_to_html(markdown_content, &markdown_file_names);
        
        let html_filename = path.file_stem()
            .and_then(|s| s.to_str())
            .unwrap_or("index");
        
        // Generate navbar HTML with current page highlighted
        let navbar = generate_navbar(&navbar_items, true, dropdowns.as_ref(), &markdown_titles, Some(html_filename));
        
        let html_output = generate_html(title, &html_content, &navbar)?;
        
        let html_path = dist_dir.join(format!("{}.html", html_filename));
        
        fs::write(&html_path, html_output)?;
        println!("Generated: {}", html_path.display());
    }

    // Copy assets to dist after building
    copy_assets_to_dist()?;

    Ok(())
}

