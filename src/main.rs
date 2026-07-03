use std::fs;
use std::path::{Path, PathBuf};
use pulldown_cmark::{html, Event, Options, Parser};
use regex::Regex;
use katex::{Opts, OutputType};
use rusqlite::{params, Connection};

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

fn katex_opts(display: bool) -> Opts {
    katex::Opts::builder()
        .display_mode(display)
        .throw_on_error(false)
        .output_type(OutputType::HtmlAndMathml)
        .build()
        .unwrap()
}

fn preprocess_math(md: &str) -> String {
    let mut result = String::with_capacity(md.len() * 2);
    let mut chars = md.chars().peekable();
    
    while let Some(ch) = chars.next() {
        if ch == '$' {
            // Check for display math: $$
            if chars.peek() == Some(&'$') {
                chars.next(); // consume second $
                let mut tex = String::new();
                let mut found_end = false;
                while let Some(c) = chars.next() {
                    if c == '$' && chars.peek() == Some(&'$') {
                        chars.next(); // consume second $
                        found_end = true;
                        break;
                    }
                    tex.push(c);
                }
                if found_end {
                    let html = katex::render_with_opts(tex.trim(), katex_opts(true))
                        .unwrap_or_else(|_| format!(r#"<pre class="math-error">{}</pre>"#, tex));
                    result.push_str(&html);
                } else {
                    // Not a valid display math, put it back
                    result.push('$');
                    result.push('$');
                    result.push_str(&tex);
                }
            } else {
                // Inline math: $...$
                let mut tex = String::new();
                let mut found_end = false;
                while let Some(c) = chars.next() {
                    if c == '$' {
                        found_end = true;
                        break;
                    }
                    if c == '\n' {
                        // Inline math can't span lines, put it back
                        result.push('$');
                        result.push_str(&tex);
                        result.push(c);
                        tex.clear();
                        break;
                    }
                    tex.push(c);
                }
                if found_end && !tex.is_empty() {
                    let html = katex::render_with_opts(tex.trim(), katex_opts(false))
                        .unwrap_or_else(|_| format!(r#"<code class="math-error">{}</code>"#, tex));
                    result.push_str(&html);
                } else {
                    result.push('$');
                    result.push_str(&tex);
                }
            }
        } else if ch == '\\' {
            // Check for \( or \[
            if let Some(&next) = chars.peek() {
                if next == '(' {
                    chars.next(); // consume (
                    let mut tex = String::new();
                    let mut found_end = false;
                    while let Some(c) = chars.next() {
                        if c == '\\' && chars.peek() == Some(&')') {
                            chars.next(); // consume )
                            found_end = true;
                            break;
                        }
                        tex.push(c);
                    }
                    if found_end {
                        let html = katex::render_with_opts(tex.trim(), katex_opts(false))
                            .unwrap_or_else(|_| format!(r#"<code class="math-error">{}</code>"#, tex));
                        result.push_str(&html);
                    } else {
                        result.push('\\');
                        result.push('(');
                        result.push_str(&tex);
                    }
                } else if next == '[' {
                    chars.next(); // consume [
                    let mut tex = String::new();
                    let mut found_end = false;
                    while let Some(c) = chars.next() {
                        if c == '\\' && chars.peek() == Some(&']') {
                            chars.next(); // consume ]
                            found_end = true;
                            break;
                        }
                        tex.push(c);
                    }
                    if found_end {
                        let html = katex::render_with_opts(tex.trim(), katex_opts(true))
                            .unwrap_or_else(|_| format!(r#"<pre class="math-error">{}</pre>"#, tex));
                        result.push_str(&html);
                    } else {
                        result.push('\\');
                        result.push('[');
                        result.push_str(&tex);
                    }
                } else {
                    result.push(ch);
                }
            } else {
                result.push(ch);
            }
        } else {
            result.push(ch);
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
        } else if !base_href.contains('.') {
            // Check if it matches a markdown file (by exact match or filename match)
            let matched_path = markdown_files.iter()
                .find(|path| {
                    path.as_str() == base_href || path.ends_with(&format!("/{}", base_href))
                });
            
            if let Some(matched) = matched_path {
                let mut new = format!("{}.html", matched);
                if let Some(fq) = fragment_query {
                    new.push_str(fq);
                }
                new
            } else {
                // Not an internal link, skip
                continue;
            }
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
    // Pre-process math expressions: render them server-side with KaTeX
    let processed_markdown = preprocess_math(markdown);
    
    let options = Options::all();
    let parser = Parser::new_ext(&processed_markdown, options);
    let mut html_output = String::new();
    html::push_html(&mut html_output, parser);
    
    convert_internal_links(&html_output, markdown_files)
}

#[derive(Clone)]
enum NavbarItem {
    MarkdownFile(PathBuf, String),  // (path, title)
    ExternalLink(String, String),   // (url, text)
    Dropdown(String),                // (dropdown name)
    InternalPage(String, String, String), // (html path base, label, active key)
}

fn generate_navbar(
    navbar_items: &[NavbarItem], 
    output_in_dist: bool,
    dropdowns: Option<&std::collections::HashMap<String, serde_yaml::Value>>,
    markdown_titles: &std::collections::HashMap<String, String>,
    current_page: Option<&str>,
    asset_prefix: &str,
) -> String {
    let mut nav = String::from("<nav class=\"site-nav\" aria-label=\"Primary\">\n");
    nav.push_str("<ul class=\"nav-list\">\n");

    // Always add logo/IDEEP link at the start
    let index_title = markdown_titles.get("index")
        .cloned()
        .unwrap_or_else(|| "IDEEP".to_string());
    let index_is_active = current_page.map(|cp| cp == "index").unwrap_or(false);
    let index_link_class = if index_is_active { "nav-link nav-logo active" } else { "nav-link nav-logo" };
    // Calculate relative path to index.html from current page
    let index_path = if asset_prefix.is_empty() {
        "index.html".to_string()
    } else {
        format!("{}index.html", asset_prefix)
    };
    nav.push_str(&format!(
        "  <li class=\"nav-item\"><a href=\"{}\" class=\"{}\"><img class=\"nav-logo-img\" src=\"{}assets/logo-wide.png\" alt=\"IDEEEP home\">{}</a></li>\n",
        index_path, index_link_class, asset_prefix, index_title
    ));
    
    for item in navbar_items {
        match item {
            NavbarItem::MarkdownFile(relative_path, title) => {
                // Convert relative path to HTML path (e.g., "math/sir.md" -> "math/sir.html")
                let html_path_base = relative_path.with_extension("html")
                    .to_string_lossy()
                    .replace('\\', "/");
                let html_path = format!("{}{}", asset_prefix, html_path_base);
                let rel_key = relative_path.with_extension("")
                    .to_string_lossy()
                    .replace('\\', "/");
                
                // Skip index since we already added it with logo at the start
                if rel_key == "index" {
                    continue;
                }
                
                let is_active = current_page.map(|cp| cp == &rel_key || cp == relative_path.file_stem().and_then(|s| s.to_str()).unwrap_or("")).unwrap_or(false);
                let link_class = if is_active { "nav-link active" } else { "nav-link" };
                
                nav.push_str(&format!(
                    "  <li class=\"nav-item\"><a href=\"{}\" class=\"{}\">{}</a></li>\n",
                    html_path, link_class, title
                ));
            }
            NavbarItem::ExternalLink(url, text) => {
                nav.push_str(&format!(
                    "  <li class=\"nav-item\"><a href=\"{}\" class=\"nav-link\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a></li>\n",
                    url, text
                ));
            }
            NavbarItem::InternalPage(path_base, label, key) => {
                let href = format!("{}{}", asset_prefix, path_base);
                let is_active = current_page.map(|cp| cp == key).unwrap_or(false);
                let link_class = if is_active { "nav-link active" } else { "nav-link" };
                nav.push_str(&format!(
                    "  <li class=\"nav-item\"><a href=\"{}\" class=\"{}\">{}</a></li>\n",
                    href, link_class, label
                ));
            }
            NavbarItem::Dropdown(dropdown_name) => {
                // Render dropdown inline
                if let Some(dropdowns_map) = dropdowns {
                    if let Some(dropdown_value) = dropdowns_map.get(dropdown_name) {
                        nav.push_str("  <li class=\"nav-item dropdown\">\n");
                        nav.push_str(&format!("    <a class=\"nav-link dropdown-toggle\" tabindex=\"0\">{}</a>\n", dropdown_name));
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
                                            // Simple string - treat as markdown file name or path
                                            // If markdown_titles contains this key, use it to construct HTML path
                                            let html_path_base = if markdown_titles.contains_key(page_name) {
                                                format!("{}.html", page_name)
                                            } else {
                                                // Try to find a match by filename
                                                let found_key = markdown_titles.keys()
                                                    .find(|k| k.as_str() == page_name || k.ends_with(&format!("/{}", page_name)));
                                                if let Some(key) = found_key {
                                                    format!("{}.html", key)
                                                } else {
                                                    format!("{}.html", page_name)
                                                }
                                            };
                                            let html_path = format!("{}{}", asset_prefix, html_path_base);
                                            let display_title = markdown_titles.get(page_name)
                                                .or_else(|| {
                                                    markdown_titles.keys()
                                                        .find(|k| k.as_str() == page_name || k.ends_with(&format!("/{}", page_name)))
                                                        .and_then(|k| markdown_titles.get(k))
                                                })
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

fn generate_html(title: &str, content: &str, navbar: &str, asset_prefix: &str) -> Result<String, Box<dyn std::error::Error>> {
    let katex_css = format!(r#"<link rel="stylesheet" href="{}assets/vendor/katex/katex.min.css" type="text/css" />"#, asset_prefix);

    // Preload the self-hosted Nunito Sans faces so text paints without a swap flash.
    let font_preload = format!(
        "<link rel=\"preload\" href=\"{p}assets/fonts/nunito-sans-latin.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>\n    <link rel=\"preload\" href=\"{p}assets/fonts/nunito-sans-latin-italic.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>",
        p = asset_prefix
    );

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
    <link rel="icon" type="image/png" href="{}assets/logo.png" />
    <link rel="stylesheet" href="{}assets/styles.css" type="text/css" />
    {}
    <script src="https://kit.fontawesome.com/1ffe760482.js" crossorigin="anonymous"></script>
    <!-- Highlight.js for code syntax highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/julia.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/r.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/rust.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/go.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/typescript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/java.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/cpp.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/c.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/sql.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/yaml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/json.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/xml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/markdown.min.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        hljs.highlightAll();
    }});
    </script>
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
        title, asset_prefix, asset_prefix, font_preload, katex_css, navbar, content, footer_content
    ))
}

fn calculate_asset_prefix(relative_path: &Path) -> String {
    // Count how many directory components are in the path (excluding the filename)
    let depth = relative_path.parent()
        .map(|p| p.components().count())
        .unwrap_or(0);
    
    // Generate the prefix: "../" repeated depth times
    if depth == 0 {
        String::new()
    } else {
        "../".repeat(depth)
    }
}

fn calculate_relative_link_path(from_path: &Path, to_path: &str) -> String {
    // If to_path is "index", it's always at the root
    if to_path == "index" {
        let depth = from_path.parent()
            .map(|p| p.components().count())
            .unwrap_or(0);
        if depth == 0 {
            "index.html".to_string()
        } else {
            format!("{}index.html", "../".repeat(depth))
        }
    } else {
        // For other paths, calculate relative path
        let from_dir = from_path.parent().unwrap_or(Path::new(""));
        let to_path_buf = Path::new(to_path);
        
        // If they're in the same directory
        if from_dir == to_path_buf.parent().unwrap_or(Path::new("")) {
            format!("{}.html", to_path)
        } else {
            // Need to go up to common ancestor, then down to target
            let depth = from_dir.components().count();
            if depth == 0 {
                format!("{}.html", to_path)
            } else {
                format!("{}{}.html", "../".repeat(depth), to_path)
            }
        }
    }
}

fn copy_assets_to_dist() -> Result<(), Box<dyn std::error::Error>> {
    let assets_dir = Path::new("assets");
    let dist_assets_dir = Path::new("dist/assets");
    
    // Create dist/assets directory if it doesn't exist
    if !dist_assets_dir.exists() {
        fs::create_dir_all(dist_assets_dir)?;
    }
    
    // Recursively copy all files and directories from assets to dist/assets
    if assets_dir.exists() {
        copy_directory_recursive(assets_dir, dist_assets_dir)?;
    }
    
    Ok(())
}

fn copy_directory_recursive(src: &Path, dst: &Path) -> Result<(), Box<dyn std::error::Error>> {
    for entry in fs::read_dir(src)? {
        let entry = entry?;
        let path = entry.path();
        let file_name = path.file_name().unwrap();
        let dest_path = dst.join(file_name);
        
        if path.is_dir() {
            // Create destination directory and recurse
            fs::create_dir_all(&dest_path)?;
            copy_directory_recursive(&path, &dest_path)?;
        } else {
            // Copy file
            fs::copy(&path, &dest_path)?;
            println!("Copied: {} -> {}", path.display(), dest_path.display());
        }
    }
    
    Ok(())
}

fn find_markdown_files(dir: &Path, base_dir: &Path, files: &mut Vec<(PathBuf, PathBuf, String)>) -> Result<(), Box<dyn std::error::Error>> {
    if !dir.exists() {
        return Ok(());
    }
    
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();
        
        if path.is_dir() {
            // Recursively search subdirectories
            find_markdown_files(&path, base_dir, files)?;
        } else if path.extension().and_then(|s| s.to_str()) == Some("md") {
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
            
            // Calculate relative path from base_dir
            let relative_path = path.strip_prefix(base_dir)
                .unwrap_or(&path)
                .to_path_buf();
            
            files.push((path.clone(), relative_path, title));
        }
    }
    
    Ok(())
}

/// Extract plain, searchable text from a Markdown document. Math delimiters and
/// formatting are dropped; text and code spans are concatenated so the FTS index
/// holds readable prose rather than HTML.
fn extract_search_text(markdown: &str) -> String {
    let options = Options::all();
    let parser = Parser::new_ext(markdown, options);
    let mut text = String::new();
    for event in parser {
        match event {
            Event::Text(t) | Event::Code(t) => {
                text.push_str(&t);
                text.push(' ');
            }
            Event::SoftBreak | Event::HardBreak => text.push(' '),
            _ => {}
        }
    }
    // Collapse runs of whitespace so snippets read cleanly.
    let whitespace_re = Regex::new(r"\s+").unwrap();
    whitespace_re.replace_all(&text, " ").trim().to_string()
}

/// Build a client-loadable FTS4 SQLite index (`dist/search.db`) over every page.
/// One row per page: title, extracted content, relative URL, category, date.
/// The browser queries this with SQL.js (see `generate_search_page`).
fn build_search_index(
    markdown_files: &[(PathBuf, PathBuf, String)],
    dist_dir: &Path,
) -> Result<(), Box<dyn std::error::Error>> {
    let db_path = dist_dir.join("search.db");

    // Rebuild from scratch each run so stale entries never linger.
    if db_path.exists() {
        fs::remove_file(&db_path)?;
    }

    let conn = Connection::open(&db_path)?;

    // FTS4 is more widely supported by SQL.js builds than FTS5.
    conn.execute(
        "CREATE VIRTUAL TABLE search_index USING fts4(
            title,
            content,
            url,
            type,
            date
        )",
        [],
    )?;

    for (full_path, relative_path, title) in markdown_files {
        let rel_key = relative_path
            .with_extension("")
            .to_string_lossy()
            .replace('\\', "/");

        // The 404 page is not useful as a search hit.
        if rel_key.eq_ignore_ascii_case("404") {
            continue;
        }

        let content = fs::read_to_string(full_path)?;
        let (_, markdown_content) = extract_frontmatter(&content);
        let content_text = extract_search_text(markdown_content);

        // URL relative to the dist root, where search.html lives.
        let url = format!("{}.html", rel_key);

        // Category = top-level directory (e.g. "math", "programming"); root-level
        // pages fall back to "page".
        let category = relative_path
            .parent()
            .and_then(|p| p.components().next())
            .map(|c| c.as_os_str().to_string_lossy().to_string())
            .filter(|s| !s.is_empty())
            .unwrap_or_else(|| "page".to_string());

        conn.execute(
            "INSERT INTO search_index (title, content, url, type, date) VALUES (?1, ?2, ?3, ?4, ?5)",
            params![title, content_text, url, category, ""],
        )?;
    }

    // Merge the FTS b-trees for faster queries and a smaller file.
    conn.execute("INSERT INTO search_index(search_index) VALUES('optimize')", [])?;

    println!("Built search index at {}", db_path.display());
    Ok(())
}

/// The interactive search page body: a form plus the SQL.js loader that fetches
/// `search.db` and runs FTS queries entirely in the browser. `asset_prefix` is
/// "" because the page is emitted at the dist root.
fn search_page_content() -> String {
    r#"<h1>Search</h1>
<p class="lead">Search across all pages: math, programming, syllabi, and research content.</p>

<div class="search-container">
  <form id="search-form" class="search-form">
    <input
      type="search"
      id="search-input"
      placeholder="Enter search terms..."
      autocomplete="off"
      autofocus
    />
    <button type="submit">Search</button>
  </form>

  <div id="search-results" class="search-results"></div>
  <div id="search-loading" class="search-loading" style="display: none;">
    Loading search index...
  </div>
  <div id="search-error" class="search-error" style="display: none;"></div>
</div>

<script>
(function() {
  let db = null;
  const searchInput = document.getElementById('search-input');
  const searchForm = document.getElementById('search-form');
  const searchResults = document.getElementById('search-results');
  const searchLoading = document.getElementById('search-loading');
  const searchError = document.getElementById('search-error');

  // Load SQL.js script
  function loadSQLJS() {
    return new Promise((resolve, reject) => {
      if (typeof initSqlJs !== 'undefined') {
        resolve();
        return;
      }
      const script = document.createElement('script');
      script.src = 'assets/vendor/sqljs/sql-wasm.js';
      script.onload = () => {
        setTimeout(() => {
          if (typeof initSqlJs !== 'undefined') {
            resolve();
          } else {
            reject(new Error('initSqlJs not available after loading script'));
          }
        }, 100);
      };
      script.onerror = () => reject(new Error('Failed to load SQL.js script'));
      document.head.appendChild(script);
    });
  }

  // Initialize SQL.js and load database
  async function initSearch() {
    try {
      searchLoading.style.display = 'block';
      searchError.style.display = 'none';

      await loadSQLJS();

      const SQL = await initSqlJs({
        locateFile: file => 'assets/vendor/sqljs/' + file
      });

      const response = await fetch('search.db');
      if (!response.ok) {
        throw new Error('Failed to load search database');
      }

      const arrayBuffer = await response.arrayBuffer();
      const uint8Array = new Uint8Array(arrayBuffer);
      db = new SQL.Database(uint8Array);

      searchLoading.style.display = 'none';

      // Perform search if there's a query parameter
      const urlParams = new URLSearchParams(window.location.search);
      const query = urlParams.get('q');
      if (query) {
        searchInput.value = query;
        performSearch(query);
      }
    } catch (error) {
      searchLoading.style.display = 'none';
      searchError.style.display = 'block';
      searchError.textContent = 'Error loading search index: ' + error.message;
      console.error('Search initialization error:', error);
    }
  }

  function performSearch(query) {
    if (!db || !query || query.trim() === '') {
      searchResults.innerHTML = '<p class="search-empty">Enter a search term to find content.</p>';
      return;
    }

    try {
      const searchTerm = query.trim();

      // FTS4 returns results in relevance order by default.
      // Column indices: 0=title, 1=content, 2=url, 3=type, 4=date
      const stmt = db.prepare(`
        SELECT
          title,
          url,
          type,
          date,
          snippet(search_index, 1, '<mark>', '</mark>', '...', 32) as snippet
        FROM search_index
        WHERE search_index MATCH ?
        LIMIT 50
      `);

      stmt.bind([searchTerm]);

      const results = [];
      while (stmt.step()) {
        const row = stmt.getAsObject();
        results.push({
          title: row.title,
          url: row.url,
          type: row.type,
          date: row.date,
          snippet: row.snippet || ''
        });
      }

      stmt.free();

      displayResults(results, searchTerm);
    } catch (error) {
      searchResults.innerHTML = '<p class="search-error">Error performing search: ' + error.message + '</p>';
      console.error('Search error:', error);
    }
  }

  function displayResults(results, query) {
    if (results.length === 0) {
      searchResults.innerHTML = '<p class="search-empty">No results found for "' + escapeHtml(query) + '".</p>';
      return;
    }

    let html = '<div class="search-results-header"><p>Found ' + results.length + ' result' + (results.length !== 1 ? 's' : '') + ':</p></div>';
    html += '<ul class="search-results-list">';

    for (const result of results) {
      const url = result.url;
      const typeLabel = result.type.charAt(0).toUpperCase() + result.type.slice(1);
      const dateStr = result.date ? ' &middot; ' + result.date : '';

      html += '<li class="search-result-item">';
      html += '<h3 class="search-result-title">';
      html += '<a href="' + escapeHtml(url) + '">' + escapeHtml(result.title) + '</a>';
      html += '</h3>';
      html += '<p class="search-result-meta">' + escapeHtml(typeLabel) + dateStr + '</p>';
      if (result.snippet) {
        html += '<p class="search-result-snippet">' + result.snippet + '</p>';
      }
      html += '</li>';
    }

    html += '</ul>';
    searchResults.innerHTML = html;
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  searchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (query) {
      const url = new URL(window.location);
      url.searchParams.set('q', query);
      window.history.pushState({}, '', url);
      performSearch(query);
    }
  });

  searchInput.addEventListener('keyup', function(e) {
    if (e.key === 'Enter') {
      searchForm.dispatchEvent(new Event('submit'));
    }
  });

  initSearch();
})();
</script>

<style>
.search-container { max-width: 800px; margin: 2rem 0; }
.search-form { display: flex; gap: 0.5rem; margin-bottom: 2rem; }
.search-form input[type="search"] {
  flex: 1; padding: 0.75rem; font-size: 1rem;
  border: 1px solid #ddd; border-radius: 4px;
}
.search-form button {
  padding: 0.75rem 1.5rem; font-size: 1rem;
  background-color: #000; color: #fff;
  border: none; border-radius: 4px; cursor: pointer;
}
.search-form button:hover { background-color: #8C6D2C; }
.search-results-header { margin-bottom: 1rem; color: #666; }
.search-results-list { list-style: none; padding: 0; }
.search-result-item {
  margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid #eee;
}
.search-result-item:last-child { border-bottom: none; }
.search-result-title { margin: 0 0 0.5rem 0; font-size: 1.25rem; }
.search-result-title a { color: #003366; text-decoration: none; }
.search-result-title a:hover { text-decoration: underline; }
.search-result-meta { margin: 0.25rem 0; font-size: 0.9rem; color: #666; }
.search-result-snippet { margin: 0.5rem 0 0 0; color: #555; line-height: 1.6; }
.search-result-snippet mark { background-color: #ffeb3b; padding: 0.1em 0.2em; }
.search-empty { color: #666; font-style: italic; margin: 2rem 0; }
.search-loading { color: #666; margin: 2rem 0; }
.search-error {
  color: #d32f2f; margin: 2rem 0; padding: 1rem;
  background-color: #ffebee; border-radius: 4px;
}
</style>
"#
    .to_string()
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
    
    // Find all markdown files recursively (full_path, relative_path, title)
    let mut markdown_files: Vec<(PathBuf, PathBuf, String)> = Vec::new();
    find_markdown_files(content_dir, content_dir, &mut markdown_files)?;

    // Build a map of markdown file paths (without extension) to titles
    // Use relative path as key (e.g., "math/sir" for "content/math/sir.md")
    let mut markdown_titles: std::collections::HashMap<String, String> = std::collections::HashMap::new();
    for (_, relative_path, title) in &markdown_files {
        // Convert relative path to string key (without .md extension)
        let key = relative_path.with_extension("")
            .to_string_lossy()
            .replace('\\', "/"); // Normalize path separators
        markdown_titles.insert(key, title.clone());
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
        let mut index_file: Option<(PathBuf, PathBuf, String)> = None;
        let mut other_files: Vec<(PathBuf, PathBuf, String)> = Vec::new();
        
        for file in markdown_files {
            let relative_key = file.1.with_extension("")
                .to_string_lossy()
                .replace('\\', "/");
            if relative_key == "index" {
                index_file = Some(file);
            } else {
                other_files.push(file);
            }
        }
        
        // Sort other files according to config order
        other_files.sort_by(|a, b| {
            let a_key = a.1.with_extension("")
                .to_string_lossy()
                .replace('\\', "/");
            let b_key = b.1.with_extension("")
                .to_string_lossy()
                .replace('\\', "/");
            
            // Check if config matches just the filename or the full path
            let a_pos = order.iter().position(|x| {
                if let Some(page_name) = x.as_str() {
                    page_name == &a_key || a_key.ends_with(&format!("/{}", page_name))
                } else {
                    false
                }
            });
            let b_pos = order.iter().position(|x| {
                if let Some(page_name) = x.as_str() {
                    page_name == &b_key || b_key.ends_with(&format!("/{}", page_name))
                } else {
                    false
                }
            });
            
            match (a_pos, b_pos) {
                (Some(a_idx), Some(b_idx)) => a_idx.cmp(&b_idx),
                (Some(_), None) => std::cmp::Ordering::Less,
                (None, Some(_)) => std::cmp::Ordering::Greater,
                (None, None) => a_key.cmp(&b_key), // Alphabetical fallback for unlisted files
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
            let a_key = a.1.with_extension("")
                .to_string_lossy()
                .replace('\\', "/");
            let b_key = b.1.with_extension("")
                .to_string_lossy()
                .replace('\\', "/");
            
            match (a_key == "index", b_key == "index") {
                (true, false) => std::cmp::Ordering::Less,
                (false, true) => std::cmp::Ordering::Greater,
                _ => a_key.cmp(&b_key),
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
                    // Built-in search page (not backed by a markdown file)
                    if page_name.eq_ignore_ascii_case("search") {
                        navbar_items.push(NavbarItem::InternalPage(
                            "search.html".to_string(),
                            "Search".to_string(),
                            "search".to_string(),
                        ));
                        continue;
                    }
                    // Check if it's a dropdown name
                    if let Some(ref dropdowns_map) = dropdowns {
                        if dropdowns_map.contains_key(page_name) {
                            navbar_items.push(NavbarItem::Dropdown(page_name.clone()));
                            continue;
                        }
                    }
                    // Otherwise treat as markdown file name (can be filename or path like "math/sir")
                    if let Some((full_path, relative_path, title)) = markdown_files.iter()
                        .find(|(_, rel_path, _)| {
                            let rel_key = rel_path.with_extension("")
                                .to_string_lossy()
                                .replace('\\', "/");
                            rel_key == *page_name || rel_key.ends_with(&format!("/{}", page_name))
                        })
                        .cloned()
                    {
                        let rel_key = relative_path.with_extension("")
                            .to_string_lossy()
                            .replace('\\', "/");
                        // Skip index (already added with logo)
                        if rel_key != "index" {
                            navbar_items.push(NavbarItem::MarkdownFile(relative_path, title));
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
                    // Built-in search page (not backed by a markdown file)
                    if page_name.eq_ignore_ascii_case("search") {
                        navbar_items.push(NavbarItem::InternalPage(
                            "search.html".to_string(),
                            "Search".to_string(),
                            "search".to_string(),
                        ));
                        continue;
                    }
                    // Simple string - find matching markdown file
                    if let Some((_, relative_path, title)) = markdown_files.iter()
                        .find(|(_, rel_path, _)| {
                            let rel_key = rel_path.with_extension("")
                                .to_string_lossy()
                                .replace('\\', "/");
                            rel_key == *page_name || rel_key.ends_with(&format!("/{}", page_name))
                        })
                        .cloned()
                    {
                        let rel_key = relative_path.with_extension("")
                            .to_string_lossy()
                            .replace('\\', "/");
                        // Only add if not in dropdowns (but always include index)
                        if rel_key == "index" || !pages_in_dropdowns.contains(&rel_key) && !pages_in_dropdowns.contains(page_name) {
                            navbar_items.push(NavbarItem::MarkdownFile(relative_path, title));
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
        for (_, relative_path, title) in &markdown_files {
            let rel_key = relative_path.with_extension("")
                .to_string_lossy()
                .replace('\\', "/");
            if rel_key == "index" || !pages_in_dropdowns.contains(&rel_key) {
                navbar_items.push(NavbarItem::MarkdownFile(relative_path.clone(), title.clone()));
            }
        }
        // Add dropdowns at the end
        if let Some(ref dropdowns_map) = dropdowns {
            for dropdown_name in dropdowns_map.keys() {
                navbar_items.push(NavbarItem::Dropdown(dropdown_name.clone()));
            }
        }
        // Search page last when no explicit ordering is configured.
        navbar_items.push(NavbarItem::InternalPage(
            "search.html".to_string(),
            "Search".to_string(),
            "search".to_string(),
        ));
    }

    // Build a HashSet of markdown file paths (without extension) for link conversion
    let markdown_file_names: std::collections::HashSet<String> = markdown_files.iter()
        .map(|(_, relative_path, _)| {
            relative_path.with_extension("")
                .to_string_lossy()
                .replace('\\', "/")
        })
        .collect();

    // Process each markdown file
    for (full_path, relative_path, title) in &markdown_files {
        let content = fs::read_to_string(full_path)?;
        let (_, markdown_content) = extract_frontmatter(&content);
        let html_content = markdown_to_html(markdown_content, &markdown_file_names);
        
        let rel_key = relative_path.with_extension("")
            .to_string_lossy()
            .replace('\\', "/");
        
        // Calculate asset prefix based on depth (e.g., "../" for one level deep)
        let asset_prefix = calculate_asset_prefix(relative_path);
        
        // Generate navbar HTML with current page highlighted
        let navbar = generate_navbar(&navbar_items, true, dropdowns.as_ref(), &markdown_titles, Some(&rel_key), &asset_prefix);
        
        let html_output = generate_html(title, &html_content, &navbar, &asset_prefix)?;
        
        // Preserve directory structure in dist
        let html_path = dist_dir.join(relative_path.with_extension("html"));
        
        // Create parent directories if they don't exist
        if let Some(parent) = html_path.parent() {
            fs::create_dir_all(parent)?;
        }
        
        fs::write(&html_path, html_output)?;
        println!("Generated: {}", html_path.display());
    }

    // Build the full-text search index (dist/search.db) over every page.
    build_search_index(&markdown_files, dist_dir)?;

    // Emit the interactive search page at the dist root (asset_prefix = "").
    let search_navbar = generate_navbar(
        &navbar_items,
        true,
        dropdowns.as_ref(),
        &markdown_titles,
        Some("search"),
        "",
    );
    let search_html = generate_html("Search", &search_page_content(), &search_navbar, "")?;
    let search_path = dist_dir.join("search.html");
    fs::write(&search_path, search_html)?;
    println!("Generated: {}", search_path.display());

    // Copy assets to dist after building
    copy_assets_to_dist()?;

    Ok(())
}

