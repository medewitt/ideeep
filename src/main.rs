use std::fs;
use std::path::{Path, PathBuf};
use pulldown_cmark::{html, Event, Options, Parser, Tag};
use regex::Regex;
use katex::{Opts, OutputType};
use rusqlite::{params, Connection};

// ---------------------------------------------------------------------------
// Site-wide SEO / PWA identity
//
// These constants feed canonical URLs, Open Graph/Twitter cards, the sitemap,
// robots.txt, and the web app manifest. `SITE_URL` is the production origin
// with no trailing slash — it is concatenated with absolute paths.
//
// The origin is sourced from the `homepage` field in Cargo.toml (exposed by
// Cargo as CARGO_PKG_HOMEPAGE at compile time), so moving domains is a
// one-line change in the project's toml, not a code edit.
// ---------------------------------------------------------------------------
const SITE_URL: &str = env!("CARGO_PKG_HOMEPAGE");
const SITE_NAME: &str = "IDEEEP";
const SITE_TAGLINE: &str = "Infectious Disease Ecology, Evolution & Epidemiology Program";
const SITE_DESCRIPTION: &str = "The IDEEEP concentration at Wake Forest University unites ecology, evolutionary biology, and epidemiology to study how infectious diseases emerge, spread, and shape living systems — with quantitative methods, diagnostics, and reproducible computing.";

#[derive(Debug, serde::Deserialize)]
struct FrontMatter {
    title: Option<String>,
    toc: Option<bool>,
    /// Optional per-page meta description used for search snippets and social
    /// cards. When absent, the build derives one from the first paragraph.
    description: Option<String>,
    /// Optional per-page social/share image (Open Graph + Twitter Card), given
    /// as a site-root-relative asset path (e.g. `assets/photos/foo.jpg`). When
    /// absent, the shared `assets/og-image.png` card is used. A leading `/` or
    /// `../` is tolerated and stripped.
    image: Option<String>,
    /// Optional alt text for the per-page social image. Falls back to the
    /// page title when omitted.
    image_alt: Option<String>,
    /// When true, the build sorts every table on the page that has a `Day`
    /// and/or `Time` column by weekday then start time (see
    /// `sort_schedule_tables`). Lets a schedule stay in order after the
    /// Markdown is hand-edited. Off by default.
    sort_schedule: Option<bool>,
    /// When true, the page is unlisted: served with a `noindex` robots tag and
    /// kept out of `sitemap.xml` and the on-site search index. It still renders
    /// at its URL and is reachable by direct link; it is simply not advertised.
    /// Off by default. (Navbar placement is separate — driven by `config.yaml`.)
    hidden: Option<bool>,
}

/// Escape a string for safe use inside a double-quoted HTML attribute.
fn escape_attr(s: &str) -> String {
    s.replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
        .replace('"', "&quot;")
        .replace('\'', "&#39;")
}

/// Escape a string for safe embedding inside a JSON string literal (used for
/// the JSON-LD structured-data block).
fn escape_json(s: &str) -> String {
    let mut out = String::with_capacity(s.len() + 8);
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            '/' => out.push_str("\\/"), // defensive against a literal </script>
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out
}

/// Truncate to at most `max` characters on a word boundary, appending an
/// ellipsis when text was dropped. Used to keep meta descriptions within the
/// ~160-character window search engines display.
fn truncate_words(s: &str, max: usize) -> String {
    if s.chars().count() <= max {
        return s.to_string();
    }
    let mut out: String = s.chars().take(max).collect();
    if let Some(pos) = out.rfind(' ') {
        out.truncate(pos);
    }
    format!("{}…", out.trim_end())
}

/// Derive a meta description from the first real prose paragraph of a page,
/// skipping headings and block quotes. Falls back to the site description.
fn extract_description(markdown: &str, fallback: &str) -> String {
    let options = Options::all();
    let parser = Parser::new_ext(markdown, options);

    let mut blockquote_depth: i32 = 0;
    let mut in_heading = false;
    let mut collecting = false;
    let mut started = false;
    let mut text = String::new();

    for event in parser {
        match event {
            Event::Start(Tag::BlockQuote) => blockquote_depth += 1,
            Event::End(Tag::BlockQuote) => blockquote_depth -= 1,
            Event::Start(Tag::Heading(..)) => in_heading = true,
            Event::End(Tag::Heading(..)) => in_heading = false,
            Event::Start(Tag::Paragraph) => {
                if blockquote_depth == 0 && !in_heading {
                    collecting = true;
                    started = true;
                }
            }
            Event::End(Tag::Paragraph) => {
                if started {
                    break;
                }
            }
            Event::Text(t) | Event::Code(t) => {
                if collecting {
                    text.push_str(&t);
                }
            }
            Event::SoftBreak | Event::HardBreak => {
                if collecting {
                    text.push(' ');
                }
            }
            _ => {}
        }
    }

    // Drop math delimiters and collapse whitespace so the snippet reads cleanly.
    let cleaned = text.replace('$', "");
    let whitespace_re = Regex::new(r"\s+").unwrap();
    let cleaned = whitespace_re.replace_all(cleaned.trim(), " ").to_string();

    if cleaned.is_empty() {
        fallback.to_string()
    } else {
        truncate_words(&cleaned, 160)
    }
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

/// Rendered KaTeX HTML must not be re-parsed by the Markdown engine: the
/// output contains characters that are meaningful to GitHub-flavoured Markdown
/// (most notably the ASCII `~` that KaTeX emits for `\tilde`, which pulldown
/// pairs into `<del>` strikethrough runs, but also `*`, `_`, etc.). We render
/// each math span to HTML up front, stash it, and leave an inert placeholder
/// token in the Markdown stream. `restore_math` swaps the HTML back in after
/// Markdown parsing. The placeholder is delimited by Private Use Area code
/// points so it survives parsing untouched and cannot collide with real prose.
const MATH_PLACEHOLDER_OPEN: char = '\u{E000}';
const MATH_PLACEHOLDER_CLOSE: char = '\u{E001}';

fn math_placeholder(index: usize) -> String {
    format!("{}{}{}", MATH_PLACEHOLDER_OPEN, index, MATH_PLACEHOLDER_CLOSE)
}

fn preprocess_math(md: &str) -> (String, Vec<String>) {
    let mut result = String::with_capacity(md.len() * 2);
    let mut fragments: Vec<String> = Vec::new();
    let mut chars = md.chars().peekable();

    // Render a math fragment to HTML, store it, and emit its placeholder.
    let stash = |result: &mut String, fragments: &mut Vec<String>, html: String| {
        result.push_str(&math_placeholder(fragments.len()));
        fragments.push(html);
    };

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
                    stash(&mut result, &mut fragments, html);
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
                    stash(&mut result, &mut fragments, html);
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
                        stash(&mut result, &mut fragments, html);
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
                        stash(&mut result, &mut fragments, html);
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

    (result, fragments)
}

/// Replace the placeholders left by `preprocess_math` with their rendered
/// KaTeX HTML, now that Markdown parsing is complete and can no longer mangle
/// the math output.
fn restore_math(html: &str, fragments: &[String]) -> String {
    if fragments.is_empty() {
        return html.to_string();
    }
    let mut out = String::with_capacity(html.len());
    let mut chars = html.chars();
    while let Some(ch) = chars.next() {
        if ch == MATH_PLACEHOLDER_OPEN {
            let mut digits = String::new();
            for c in chars.by_ref() {
                if c == MATH_PLACEHOLDER_CLOSE {
                    break;
                }
                digits.push(c);
            }
            if let Some(fragment) = digits.parse::<usize>().ok().and_then(|i| fragments.get(i)) {
                out.push_str(fragment);
            }
            // A placeholder that fails to parse is dropped rather than shown.
        } else {
            out.push(ch);
        }
    }
    out
}

fn convert_internal_links(html: &str, markdown_files: &std::collections::HashSet<String>) -> String {
    // Match <a ...> tags with href anywhere in the tag (attributes may precede
    // href, e.g. class="card" href="...").
    let link_pattern = Regex::new(r#"<a\s+([^>]*?)href="([^"]+)"([^>]*)>"#).unwrap();
    let mut result = html.to_string();

    // Find all matches and replace from end to start to preserve indices
    let mut replacements: Vec<(usize, usize, String)> = Vec::new();

    for cap in link_pattern.captures_iter(html) {
        let full_match = cap.get(0).unwrap();
        let pre_attrs = cap.get(1).unwrap().as_str();
        let href = cap.get(2).unwrap().as_str();
        let attrs = cap.get(3).unwrap().as_str();
        
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
        
        let new_link = format!(r#"<a {}href="{}"{}>"#, pre_attrs, new_href, attrs);
        replacements.push((full_match.start(), full_match.end(), new_link));
    }
    
    // Replace from end to start to preserve indices
    for (start, end, replacement) in replacements.iter().rev() {
        result.replace_range(*start..*end, replacement);
    }
    
    result
}

/// SVG glyph for each callout type (inline so it themes with currentColor).
fn callout_icon(kind: &str) -> &'static str {
    match kind {
        "tip" => r#"<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18h6M10 21h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1h6c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/></svg>"#,
        "warning" => r#"<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></svg>"#,
        "example" => r#"<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16v14H4z"/><path d="M8 9h8M8 13h5"/></svg>"#,
        // note / default
        _ => r#"<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/></svg>"#,
    }
}

/// Transform GitHub-style admonition blockquotes (`> [!NOTE]`, `[!TIP]`,
/// `[!WARNING]`, `[!EXAMPLE]`) into styled callout blocks.
fn render_callouts(html: &str) -> String {
    let re = Regex::new(r"(?is)<blockquote>\s*<p>\s*\[!(NOTE|TIP|WARNING|EXAMPLE|IMPORTANT|CAUTION)\][ \t]*(?:<br\s*/?>|\n)?(.*?)</blockquote>").unwrap();
    re.replace_all(html, |caps: &regex::Captures| {
        let raw = caps[1].to_ascii_lowercase();
        let (kind, label) = match raw.as_str() {
            "tip" => ("tip", "Tip"),
            "warning" | "caution" => ("warning", "Warning"),
            "example" => ("example", "Example"),
            _ => ("note", "Note"), // note / important
        };
        format!(
            "<div class=\"callout callout-{kind}\">\n<div class=\"callout-heading\">{icon}<span>{label}</span></div>\n<p>{body}</div>",
            kind = kind,
            icon = callout_icon(kind),
            label = label,
            body = &caps[2],
        )
    }).into_owned()
}

/// Drop HTML tags and collapse whitespace, for slugs and TOC labels.
fn strip_tags(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    let mut in_tag = false;
    for c in s.chars() {
        match c {
            '<' => in_tag = true,
            '>' => in_tag = false,
            _ if !in_tag => out.push(c),
            _ => {}
        }
    }
    out.split_whitespace().collect::<Vec<_>>().join(" ")
}

/// A URL-safe slug from heading text.
fn slugify(s: &str) -> String {
    let text = strip_tags(s)
        .replace("&amp;", " ")
        .replace("&lt;", " ")
        .replace("&gt;", " ")
        .replace("&quot;", " ")
        .replace("&#39;", " ");
    let mut slug = String::new();
    let mut prev_dash = false;
    for c in text.chars() {
        if c.is_ascii_alphanumeric() {
            slug.push(c.to_ascii_lowercase());
            prev_dash = false;
        } else if !slug.is_empty() && !prev_dash {
            slug.push('-');
            prev_dash = true;
        }
    }
    slug.trim_matches('-').to_string()
}

/// Give every h2/h3 a unique id and return the ordered heading list for a TOC.
fn add_heading_ids(html: &str) -> (String, Vec<(u8, String, String)>) {
    let re = Regex::new(r"(?is)<h([23])>(.*?)</h[23]>").unwrap();
    let mut out = String::with_capacity(html.len());
    let mut last = 0;
    let mut seen: std::collections::HashMap<String, u32> = std::collections::HashMap::new();
    let mut headings = Vec::new();
    for caps in re.captures_iter(html) {
        let m = caps.get(0).unwrap();
        let lvl: u8 = caps[1].parse().unwrap_or(2);
        let inner = &caps[2];
        let base = {
            let b = slugify(inner);
            if b.is_empty() { "section".to_string() } else { b }
        };
        let n = seen.entry(base.clone()).or_insert(0);
        let slug = if *n == 0 { base.clone() } else { format!("{}-{}", base, n) };
        *n += 1;
        out.push_str(&html[last..m.start()]);
        // Emit the heading with a trailing permalink anchor. The `#` is visually
        // revealed on hover/focus (see `.heading-anchor` in styles.css) and lets a
        // reader copy a direct link to any section. The anchor is appended *after*
        // `inner`, and the TOC/heading list below still uses the anchor-free
        // `inner`, so neither the "On this page" nav nor the search text sees it.
        out.push_str(&format!(
            "<h{l} id=\"{s}\">{inner}<a class=\"heading-anchor\" href=\"#{s}\" aria-label=\"Permalink to this section\">#</a></h{l}>",
            l = lvl,
            s = slug,
            inner = inner
        ));
        last = m.end();
        headings.push((lvl, slug, strip_tags(inner)));
    }
    out.push_str(&html[last..]);
    (out, headings)
}

/// Build the "On this page" navigation from collected headings.
fn build_toc(headings: &[(u8, String, String)]) -> String {
    let mut s = String::from(
        "<nav class=\"page-toc\" aria-label=\"On this page\">\n<p class=\"page-toc-title\">On this page</p>\n<ul>\n",
    );
    for (lvl, slug, text) in headings {
        let cls = if *lvl == 3 { " class=\"toc-sub\"" } else { "" };
        // `text` is stripped from already-escaped HTML, so it is safe to emit as-is.
        s.push_str(&format!(
            "<li{}><a href=\"#{}\">{}</a></li>\n",
            cls, slug, text
        ));
    }
    s.push_str("</ul>\n</nav>\n");
    s
}

/// Flow flat link lists (>=4 items, mostly links, no nesting) into columns.
fn columnize_link_lists(html: &str) -> String {
    let mut out = String::with_capacity(html.len());
    let mut rest = html;
    while let Some(pos) = rest.find("<ul>") {
        out.push_str(&rest[..pos]);
        let after = &rest[pos..];
        let b = after.as_bytes();
        let mut depth = 0i32;
        let mut idx = 0usize;
        let mut end = None;
        while idx < b.len() {
            if b[idx..].starts_with(b"<ul>") {
                depth += 1;
                idx += 4;
            } else if b[idx..].starts_with(b"</ul>") {
                depth -= 1;
                idx += 5;
                if depth == 0 {
                    end = Some(idx);
                    break;
                }
            } else {
                idx += 1;
            }
        }
        match end {
            Some(e) => {
                let inner = &after[4..e - 5];
                let li_count = inner.matches("<li>").count();
                let link_items = inner.matches("<li><a").count();
                let nested = inner.contains("<ul");
                if !nested && li_count >= 4 && link_items * 2 >= li_count {
                    out.push_str("<ul class=\"col-list\">");
                    out.push_str(&after[4..e]);
                } else {
                    out.push_str(&after[..e]);
                }
                rest = &after[e..];
            }
            None => {
                out.push_str(after);
                rest = "";
                break;
            }
        }
    }
    out.push_str(rest);
    out
}

/// Wrap block images in numbered `<figure>`/`<figcaption>` elements and resolve
/// `[@fig:label]` cross-references to their number.
///
/// A paragraph that contains nothing but a single image (the `![alt](src)`
/// convention this site uses, which the Markdown parser renders as
/// `<p><img …></p>`) becomes:
///
/// ```html
/// <figure id="fig-…" class="figure">
///   <img …>
///   <figcaption><span class="figure-label">Figure N.</span> alt text</figcaption>
/// </figure>
/// ```
///
/// Figures are numbered sequentially per page, and the alt text doubles as the
/// visible caption (matching the authoring guide). A figure can be *labelled*
/// for cross-referencing by giving the Markdown image a title that starts with
/// `fig:` — `![Epidemic curve](curve.svg "fig:curve")` — which becomes the
/// element id (`fig-curve`) and is stripped from the rendered `<img>`. Anywhere
/// in the prose, `[@fig:curve]` then renders as a link reading "Figure N"
/// pointing at that figure; the reference and the figure may appear in either
/// order. An image with empty alt text and no `fig:` label is left as a plain
/// inline image (an escape hatch for decorative art). An unresolved reference
/// renders a loud marker rather than silently vanishing.
fn process_figures(html: &str) -> String {
    let para_img = Regex::new(r"(?s)<p>\s*(<img\b[^>]*?>)\s*</p>").unwrap();
    let alt_re = Regex::new(r#"alt="([^"]*)""#).unwrap();
    let title_re = Regex::new(r#"\s*title="([^"]*)""#).unwrap();

    // Map a `fig:label` to the number assigned to that figure, filled during the
    // wrapping pass and consumed by the reference-resolution pass.
    let mut labels: std::collections::HashMap<String, usize> = std::collections::HashMap::new();
    let mut counter = 0usize;

    let wrapped = para_img.replace_all(html, |caps: &regex::Captures| {
        let img_tag = &caps[1];
        let alt = alt_re
            .captures(img_tag)
            .map(|c| c[1].to_string())
            .unwrap_or_default();
        let title = title_re.captures(img_tag).map(|c| c[1].to_string());
        let label = title.as_deref().filter(|t| t.starts_with("fig:"));

        // Decorative image (no caption, no label): leave the paragraph as-is.
        if alt.trim().is_empty() && label.is_none() {
            return caps[0].to_string();
        }

        counter += 1;
        let id = match label {
            Some(l) => {
                let slug = l.replace(':', "-");
                labels.insert(l.to_string(), counter);
                slug
            }
            None => format!("figure-{}", counter),
        };

        // Strip a `fig:` sentinel title from the emitted <img> so it does not
        // surface as a browser tooltip; a non-sentinel title is left intact.
        let clean_img = if label.is_some() {
            title_re.replace(img_tag, "").into_owned()
        } else {
            img_tag.to_string()
        };

        let caption = if alt.trim().is_empty() {
            format!("<span class=\"figure-label\">Figure {}.</span>", counter)
        } else {
            format!(
                "<span class=\"figure-label\">Figure {}.</span> {}",
                counter, alt
            )
        };

        format!(
            "<figure id=\"{id}\" class=\"figure\">\n{img}\n<figcaption>{cap}</figcaption>\n</figure>",
            id = id,
            img = clean_img,
            cap = caption,
        )
    });

    // Second pass: resolve `[@fig:label]` references now that every figure has a
    // number. Undefined references become a visible error marker.
    let ref_re = Regex::new(r"\[@(fig:[A-Za-z0-9_:-]+)\]").unwrap();
    ref_re
        .replace_all(&wrapped, |caps: &regex::Captures| {
            let key = &caps[1];
            match labels.get(key) {
                Some(n) => format!(
                    "<a class=\"fig-ref\" href=\"#{id}\">Figure {n}</a>",
                    id = key.replace(':', "-"),
                    n = n
                ),
                None => format!(
                    "<span class=\"fig-ref-error\">[unresolved figure reference: {}]</span>",
                    key
                ),
            }
        })
        .into_owned()
}

/// Directory (relative to the project root) that holds reusable Markdown
/// fragments. A page injects one with a `:::{fragment-name.md}:::` shortcode on
/// its own line (the `.md` extension is optional). Fragments live under a
/// leading-underscore directory so `find_markdown_files` skips them and they are
/// never compiled into standalone pages of their own — they exist only to be
/// spliced into the pages that reference them.
const FRAGMENTS_DIR: &str = "content/_fragments";

/// Expand `:::{fragment.md}:::` include shortcodes by splicing the referenced
/// fragment's Markdown into the stream *before* it is parsed, so a fragment
/// renders exactly as if its text had been written inline (headings, tables,
/// callouts and math all work). Update the fragment once and every page that
/// includes it changes on the next build.
///
/// Includes may nest (a fragment can include another). A per-branch stack guards
/// against cycles, and shortcodes that reference a missing file or try to escape
/// the fragments directory are left as a visible, logged marker rather than
/// silently dropping content — a lost policy section should never pass unnoticed.
/// Parse a fragment shortcode's inner text into `(filename, sort_schedule)`.
///
/// The text is the fragment name, optionally followed by `;`-separated options:
/// `:::{fellow-schedule-2026; schedule=true}:::`. The only option today is
/// `schedule` — bare or truthy (`true`/`1`/`yes`/`on`, case-insensitive) — which
/// requests build-time schedule-sorting of the fragment's tables. The `.md`
/// extension on the name stays optional. Unknown options are ignored so the
/// syntax can grow without breaking existing includes.
fn parse_include_spec(raw: &str) -> (String, bool) {
    let mut parts = raw.split(';');
    let name_part = parts.next().unwrap_or("").trim();
    let name = if name_part.ends_with(".md") {
        name_part.to_string()
    } else {
        format!("{}.md", name_part)
    };

    let mut sort_schedule = false;
    for opt in parts {
        let opt = opt.trim();
        if opt.is_empty() {
            continue;
        }
        let (key, val) = match opt.split_once('=') {
            Some((k, v)) => (k.trim().to_lowercase(), v.trim().to_lowercase()),
            None => (opt.to_lowercase(), String::new()),
        };
        if key == "schedule" {
            sort_schedule = val.is_empty() || matches!(val.as_str(), "true" | "1" | "yes" | "on");
        }
    }
    (name, sort_schedule)
}

fn expand_includes(markdown: &str) -> String {
    expand_includes_from(markdown, Path::new(FRAGMENTS_DIR))
}

/// Core of `expand_includes`, parameterised by the fragments directory so it can
/// be exercised against fixtures in tests. `stack` is the chain of fragments
/// currently being expanded on this branch; a name already on it would form a
/// cycle (direct `a→a` or mutual `a→b→a`) and is refused instead of recursed
/// into, which is what stops the expansion from looping forever.
fn expand_includes_from(markdown: &str, dir: &Path) -> String {
    fn expand(md: &str, dir: &Path, stack: &mut Vec<String>) -> String {
        // A shortcode occupies its own line: optional indentation, then
        // `:::{ name }:::`, then optional trailing whitespace.
        let re = Regex::new(r"(?m)^[ \t]*:::\{\s*([^{}]+?)\s*\}:::[ \t]*$").unwrap();
        re.replace_all(md, |caps: &regex::Captures| {
            let raw = caps[1].trim();
            let (name, sort_sched) = parse_include_spec(raw);

            // Refuse anything that could reach outside the fragments directory.
            if name.contains("..")
                || name.starts_with('/')
                || name.starts_with('\\')
                || Path::new(&name).is_absolute()
            {
                eprintln!("Warning: ignoring unsafe fragment include: {}", raw);
                return format!("<!-- unsafe fragment include: {} -->", raw);
            }

            // A fragment already active on this branch would loop forever if
            // re-entered (self-reference or a mutual `a→b→a` cycle). Diamonds
            // (the same fragment included twice on *separate* branches) are fine
            // because each name is popped once its subtree finishes expanding.
            if stack.iter().any(|n| n == &name) {
                eprintln!("Warning: skipping recursive fragment include: {}", name);
                return format!("<!-- recursive fragment include: {} -->", name);
            }

            let path = dir.join(&name);
            match fs::read_to_string(&path) {
                Ok(text) => {
                    stack.push(name.clone());
                    let expanded = expand(&text, dir, stack);
                    stack.pop();
                    // `schedule=true` on the include sorts the fragment's own
                    // schedule tables (by Day then Time) as it is spliced in, so
                    // a reusable agenda fragment stays ordered after hand-edits.
                    let expanded = if sort_sched {
                        sort_schedule_tables(&expanded)
                    } else {
                        expanded
                    };
                    // Set the fragment off as its own block(s): blank lines above
                    // and below guarantee the splice can't fuse with adjacent
                    // prose (e.g. a heading running into a preceding paragraph).
                    format!("\n\n{}\n\n", expanded.trim())
                }
                Err(_) => {
                    eprintln!(
                        "Warning: template fragment not found: {}",
                        path.display()
                    );
                    format!(
                        "\n\n<div class=\"fragment-error\">Missing template fragment: <code>{}</code></div>\n\n",
                        name
                    )
                }
            }
        })
        .into_owned()
    }

    // Fast path: most pages contain no shortcodes at all.
    if !markdown.contains(":::{") {
        return markdown.to_string();
    }
    let mut stack: Vec<String> = Vec::new();
    expand(markdown, dir, &mut stack)
}

/// Default summary label for a spoiler block whose opener gives no text of its
/// own (`:::spoiler` with nothing after it).
const SPOILER_DEFAULT_SUMMARY: &str = "Show more";

/// Escape a string for use as HTML *text* (element content, not an attribute).
fn escape_text(s: &str) -> String {
    s.replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
}

/// If `line` opens a spoiler block, return its summary label (trimmed, possibly
/// empty). The opener is `:::spoiler` or `:::details` at the start of the line
/// (after optional indentation); everything after the keyword on that line is
/// the free-text summary. Returns `None` for any other line.
///
/// The summary is deliberately author-configurable — `:::spoiler Show the
/// solution`, `:::details Reveal the derivation`, `:::spoiler Spoiler` all work,
/// and a bare `:::spoiler` falls back to `SPOILER_DEFAULT_SUMMARY`.
fn spoiler_opener_label(line: &str) -> Option<String> {
    let t = line.trim_start();
    for kw in ["spoiler", "details"] {
        if let Some(rest) = t.strip_prefix(":::") {
            if let Some(after) = rest.strip_prefix(kw) {
                // The keyword must end the token (end of line or whitespace),
                // so `:::spoilerfoo` is not mistaken for an opener.
                if after.is_empty() || after.starts_with(char::is_whitespace) {
                    return Some(after.trim().to_string());
                }
            }
        }
    }
    None
}

/// Whether a line closes a fenced block: exactly `:::` (with optional
/// surrounding whitespace) and nothing else.
fn is_fence_close(line: &str) -> bool {
    line.trim() == ":::"
}

/// Expand `:::spoiler … ::: ` (and the `:::details` alias) fenced blocks into
/// native `<details>`/`<summary>` disclosure widgets, so a page can hide a
/// worked solution, a long derivation, or an aside behind a click with no
/// JavaScript.
///
/// ```text
/// :::spoiler Show the solution
/// The body is **ordinary Markdown** — lists, math, code, even nested spoilers.
/// :::
/// ```
///
/// The text after the keyword is the clickable summary (configurable per block;
/// a bare `:::spoiler` uses "Show more"). The body is emitted between blank
/// lines inside the `<details>` element so the Markdown parser still renders it
/// normally (a `<details>` HTML block is closed by the blank line, the body is
/// parsed, then `</details>` reopens an HTML block). Blocks may nest. An opener
/// with no matching `:::` close is left untouched so stray text is never eaten.
/// Runs on the raw Markdown before parsing, like `expand_includes`.
fn expand_spoilers(markdown: &str) -> String {
    // Fast path: nothing to do unless a spoiler/details opener is present.
    if !markdown.contains(":::spoiler") && !markdown.contains(":::details") {
        return markdown.to_string();
    }

    let lines: Vec<&str> = markdown.lines().collect();
    let mut out = String::with_capacity(markdown.len() + 64);
    let mut i = 0;
    while i < lines.len() {
        if let Some(label) = spoiler_opener_label(lines[i]) {
            // Scan forward for the matching close, tracking nested spoiler
            // openers so an inner `:::` doesn't close the outer block early.
            let mut depth = 1i32;
            let mut j = i + 1;
            let mut body: Vec<&str> = Vec::new();
            while j < lines.len() {
                if spoiler_opener_label(lines[j]).is_some() {
                    depth += 1;
                    body.push(lines[j]);
                } else if is_fence_close(lines[j]) {
                    depth -= 1;
                    if depth == 0 {
                        break;
                    }
                    body.push(lines[j]);
                } else {
                    body.push(lines[j]);
                }
                j += 1;
            }

            if depth == 0 {
                // Recurse so nested spoilers inside the body are expanded too.
                let inner = expand_spoilers(&body.join("\n"));
                let summary = if label.is_empty() {
                    SPOILER_DEFAULT_SUMMARY.to_string()
                } else {
                    escape_text(&label)
                };
                out.push_str(&format!(
                    "<details class=\"spoiler\">\n<summary>{}</summary>\n\n{}\n\n</details>\n",
                    summary,
                    inner.trim_matches('\n')
                ));
                i = j + 1;
                continue;
            }
            // Unterminated opener: emit the line verbatim and move on.
        }
        out.push_str(lines[i]);
        out.push('\n');
        i += 1;
    }
    out
}

/// Whether a line is a GFM table delimiter row (`|---|:--:|`): every
/// pipe-separated cell is dashes with optional alignment colons.
fn is_table_delimiter(line: &str) -> bool {
    let cells: Vec<&str> = line.trim().trim_matches('|').split('|').collect();
    !cells.is_empty()
        && cells.iter().all(|c| {
            let c = c.trim();
            !c.is_empty() && c.contains('-') && c.chars().all(|ch| ch == '-' || ch == ':')
        })
}

/// Split a Markdown table row into trimmed cell strings, dropping the outer pipes.
fn table_cells(line: &str) -> Vec<String> {
    line.trim()
        .trim_matches('|')
        .split('|')
        .map(|c| c.trim().to_string())
        .collect()
}

/// Locate the `Day` and `Time` columns in a table header row (case-insensitive,
/// ignoring `*` emphasis), returning their cell indices when present.
fn schedule_columns(header: &str) -> (Option<usize>, Option<usize>) {
    let (mut day, mut time) = (None, None);
    for (idx, cell) in table_cells(header).iter().enumerate() {
        match cell.replace('*', "").trim().to_lowercase().as_str() {
            "day" => day = Some(idx),
            "time" => time = Some(idx),
            _ => {}
        }
    }
    (day, time)
}

/// Rank a weekday from the start of a cell like `Mon (Jul 20 / Aug 3)`.
/// Unknown days sort last.
fn weekday_rank(cell: &str) -> u32 {
    let c = cell.trim().to_lowercase();
    for (i, d) in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].iter().enumerate() {
        if c.starts_with(d) {
            return i as u32;
        }
    }
    u32::MAX
}

/// Parse the start of a slot like `9-9:50`, `12-1p`, or `1-1:50` into minutes
/// since midnight, so morning and afternoon slots order correctly.
///
/// The start hour is read from the text before the `-`. A `p`/`pm` or `a`/`am`
/// in the cell sets the meridiem; without one, hours 1–6 are read as afternoon
/// and 7–12 as morning/noon — the convention this program's day follows
/// (9–11 AM lectures, 12 noon, 1–3 PM sessions).
fn start_minutes(cell: &str) -> u32 {
    let lower = cell.to_lowercase();
    let start = lower.split('-').next().unwrap_or("");

    // First contiguous digit run = hour.
    let mut hour_str = String::new();
    let mut seen = false;
    for ch in start.chars() {
        if ch.is_ascii_digit() {
            hour_str.push(ch);
            seen = true;
        } else if seen {
            break;
        }
    }
    let hour: u32 = hour_str.parse().unwrap_or(0);

    // Digits after a `:` = minutes.
    let min: u32 = start
        .split_once(':')
        .map(|(_, rest)| {
            rest.chars()
                .take_while(|c| c.is_ascii_digit())
                .collect::<String>()
                .parse()
                .unwrap_or(0)
        })
        .unwrap_or(0);

    let hour24 = if lower.contains('p') {
        if hour == 12 { 12 } else { hour + 12 }
    } else if lower.contains('a') {
        if hour == 12 { 0 } else { hour }
    } else {
        match hour {
            1..=6 => hour + 12,
            _ => hour,
        }
    };
    hour24 * 60 + min
}

/// Reorder the body rows of GFM tables on schedule pages, enabled per page with
/// `sort_schedule: true` in front matter.
///
/// Every Markdown table that has a `Day` and/or `Time` header column is sorted
/// by weekday then start time, so editing a cell in the Markdown reorders the
/// rendered agenda on the next build instead of leaving rows where they were
/// typed. The sort is stable (equal rows keep their written order), tables
/// without either column are left untouched, and all surrounding prose is
/// preserved. Runs on the raw Markdown before parsing, like `expand_includes`.
fn sort_schedule_tables(markdown: &str) -> String {
    let lines: Vec<&str> = markdown.lines().collect();
    let mut out: Vec<String> = Vec::with_capacity(lines.len());
    let mut i = 0;
    while i < lines.len() {
        let is_table_head = i + 1 < lines.len()
            && lines[i].contains('|')
            && is_table_delimiter(lines[i + 1]);
        if !is_table_head {
            out.push(lines[i].to_string());
            i += 1;
            continue;
        }

        let header = lines[i];
        let delim = lines[i + 1];
        let mut j = i + 2;
        let mut body: Vec<&str> = Vec::new();
        while j < lines.len() && lines[j].contains('|') && !lines[j].trim().is_empty() {
            body.push(lines[j]);
            j += 1;
        }

        out.push(header.to_string());
        out.push(delim.to_string());

        let (day_col, time_col) = schedule_columns(header);
        if day_col.is_some() || time_col.is_some() {
            // Stable sort by (weekday, start time), keeping written order on ties.
            let mut indexed: Vec<(usize, &str)> = body.iter().copied().enumerate().collect();
            indexed.sort_by(|a, b| {
                let key = |row: &str| {
                    let cells = table_cells(row);
                    let d = day_col
                        .and_then(|c| cells.get(c))
                        .map(|s| weekday_rank(s))
                        .unwrap_or(0);
                    let t = time_col
                        .and_then(|c| cells.get(c))
                        .map(|s| start_minutes(s))
                        .unwrap_or(0);
                    (d, t)
                };
                key(a.1).cmp(&key(b.1)).then(a.0.cmp(&b.0))
            });
            for (_, row) in indexed {
                out.push(row.to_string());
            }
        } else {
            for row in body {
                out.push(row.to_string());
            }
        }
        i = j;
    }

    let mut result = out.join("\n");
    if markdown.ends_with('\n') {
        result.push('\n');
    }
    result
}

fn markdown_to_html(markdown: &str, markdown_files: &std::collections::HashSet<String>) -> String {
    // Splice in any `:::{fragment.md}:::` template fragments first, so the rest
    // of the pipeline sees one flat Markdown document.
    let markdown = expand_includes(markdown);
    // Expand `:::spoiler … :::` disclosure blocks into `<details>` wrappers whose
    // bodies the Markdown parser still renders normally. Done before math/parse.
    let markdown = expand_spoilers(&markdown);
    let markdown = markdown.as_str();

    // Pre-process math expressions: render them server-side with KaTeX, leaving
    // inert placeholders in the Markdown so the parser can't mangle the output.
    let (processed_markdown, math_fragments) = preprocess_math(markdown);

    let options = Options::all();
    let parser = Parser::new_ext(&processed_markdown, options);
    let mut html_output = String::new();
    html::push_html(&mut html_output, parser);

    // Splice the rendered KaTeX HTML back in now that parsing is done.
    let html_output = restore_math(&html_output, &math_fragments);

    let linked = convert_internal_links(&html_output, markdown_files);
    let with_callouts = render_callouts(&linked);
    let with_columns = columnize_link_lists(&with_callouts);
    // Number block images into <figure>s and resolve [@fig:…] cross-references.
    process_figures(&with_columns)
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
    let mut nav = String::from("<nav class=\"site-nav\" aria-label=\"Primary\">\n<div class=\"nav-inner\">\n");

    // Logo/home link sits outside the collapsible menu so it stays visible on mobile.
    let index_is_active = current_page.map(|cp| cp == "index").unwrap_or(false);
    let index_link_class = if index_is_active { "nav-logo active" } else { "nav-logo" };
    // Calculate relative path to index.html from current page
    let index_path = if asset_prefix.is_empty() {
        "index.html".to_string()
    } else {
        format!("{}index.html", asset_prefix)
    };
    nav.push_str(&format!(
        "  <a href=\"{}\" class=\"{}\"{}><img class=\"nav-logo-img\" src=\"{}assets/emblem.png\" alt=\"\" width=\"40\" height=\"40\"><span class=\"nav-wordmark\"><span class=\"nav-wordmark-main\">Infectious Diseases</span><span class=\"nav-wordmark-sub\">Ecology, Evolution &amp; Epidemiology</span></span></a>\n",
        index_path,
        index_link_class,
        if index_is_active { " aria-current=\"page\"" } else { "" },
        asset_prefix
    ));

    // Hamburger toggle (shown on narrow screens; controlled by assets/nav.js).
    nav.push_str("  <button class=\"nav-toggle\" aria-expanded=\"false\" aria-controls=\"primary-menu\" aria-label=\"Toggle navigation menu\"><span class=\"nav-toggle-bars\" aria-hidden=\"true\"></span></button>\n");

    nav.push_str("  <ul class=\"nav-list\" id=\"primary-menu\">\n");

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
                let aria_current = if is_active { " aria-current=\"page\"" } else { "" };

                nav.push_str(&format!(
                    "  <li class=\"nav-item\"><a href=\"{}\" class=\"{}\"{}>{}</a></li>\n",
                    html_path, link_class, aria_current, title
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
                let aria_current = if is_active { " aria-current=\"page\"" } else { "" };
                nav.push_str(&format!(
                    "  <li class=\"nav-item\"><a href=\"{}\" class=\"{}\"{}>{}</a></li>\n",
                    href, link_class, aria_current, label
                ));
            }
            NavbarItem::Dropdown(dropdown_name) => {
                // Render dropdown inline
                if let Some(dropdowns_map) = dropdowns {
                    if let Some(dropdown_value) = dropdowns_map.get(dropdown_name) {
                        // A URL-safe id for aria-controls / the panel.
                        let slug: String = dropdown_name
                            .chars()
                            .map(|c| if c.is_ascii_alphanumeric() { c.to_ascii_lowercase() } else { '-' })
                            .collect();
                        let panel_id = format!("dd-{}", slug);

                        // Highlight the dropdown parent when the current page lives inside it.
                        let dd_active = current_page.map(|cp| match dropdown_value {
                            serde_yaml::Value::Sequence(seq) => seq.iter().any(|it| {
                                it.as_str()
                                    .map(|pn| cp == pn || cp.starts_with(&format!("{}/", pn)))
                                    .unwrap_or(false)
                            }),
                            _ => false,
                        }).unwrap_or(false);
                        let toggle_class = if dd_active { "nav-link dropdown-toggle active" } else { "nav-link dropdown-toggle" };

                        nav.push_str("  <li class=\"nav-item dropdown\">\n");
                        nav.push_str(&format!(
                            "    <button type=\"button\" class=\"{}\" aria-expanded=\"false\" aria-haspopup=\"true\" aria-controls=\"{}\">{}<svg class=\"dropdown-caret\" width=\"11\" height=\"7\" viewBox=\"0 0 10 6\" aria-hidden=\"true\"><path d=\"M1 1l4 4 4-4\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg></button>\n",
                            toggle_class, panel_id, dropdown_name
                        ));
                        nav.push_str(&format!("    <div class=\"dropdown-content\" id=\"{}\">\n", panel_id));
                        
                        // Handle different dropdown value types
                        match dropdown_value {
                            serde_yaml::Value::Mapping(map) => {
                                // For mappings the key is the display label and the
                                // value is the target URL, e.g.
                                //   Program:
                                //     Program Overview: programs.html
                                //     Courses & Syllabi: programs.html#curriculum
                                // Relative URLs are resolved against the page being
                                // rendered, so they must carry the same asset_prefix
                                // the rest of the navbar uses; absolute URLs and pure
                                // fragment links are emitted verbatim.
                                for (key, value) in map {
                                    let page_name = key.as_str().unwrap_or("");
                                    let url = value.as_str().unwrap_or("");
                                    let display_title = markdown_titles.get(page_name)
                                        .cloned()
                                        .unwrap_or_else(|| page_name.to_string());
                                    let is_external = url.starts_with("http://")
                                        || url.starts_with("https://")
                                        || url.starts_with("//");
                                    let is_rooted = url.starts_with('/') || url.starts_with('#');
                                    if is_external {
                                        nav.push_str(&format!(
                                            "      <a href=\"{}\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a>\n",
                                            url, display_title
                                        ));
                                    } else {
                                        let href = if is_rooted {
                                            url.to_string()
                                        } else {
                                            format!("{}{}", asset_prefix, url)
                                        };
                                        nav.push_str(&format!(
                                            "      <a href=\"{}\">{}</a>\n",
                                            href, display_title
                                        ));
                                    }
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
    
    // Theme toggle (last item; handler lives in assets/nav.js)
    nav.push_str("  <li class=\"nav-item\"><button type=\"button\" class=\"nav-link theme-toggle\" aria-label=\"Toggle dark mode\" title=\"Toggle light/dark theme\"><svg class=\"icon-moon\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z\"/></svg><svg class=\"icon-sun\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><circle cx=\"12\" cy=\"12\" r=\"4.5\"/><path d=\"M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4\"/></svg></button></li>\n");

    nav.push_str("  </ul>\n</div>\n</nav>\n");
    nav
}

fn generate_html(
    title: &str,
    description: &str,
    canonical_path: &str,
    robots: &str,
    breadcrumbs: &[(String, String)],
    content: &str,
    navbar: &str,
    asset_prefix: &str,
    page_image: Option<&str>,
    page_image_alt: Option<&str>,
) -> Result<String, Box<dyn std::error::Error>> {
    let katex_css = format!(r#"<link rel="stylesheet" href="{}assets/vendor/katex/katex.min.css" type="text/css" />"#, asset_prefix);

    // Read footer.html
    let footer_path = Path::new("assets/footer.html");
    let footer_content = if footer_path.exists() {
        fs::read_to_string(footer_path)?
    } else {
        String::new()
    };

    // Preload the self-hosted Nunito Sans faces so text paints without a swap flash.
    let font_preload = format!(
        "<link rel=\"preload\" href=\"{p}assets/fonts/nunito-sans-latin.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>\n    <link rel=\"preload\" href=\"{p}assets/fonts/nunito-sans-latin-italic.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>",
        p = asset_prefix
    );

    // Syntax-highlight themes swap with the color scheme; an early script applies
    // any saved manual preference before paint (and toggles the code themes).
    let hljs_block = format!(
        r#"<link rel="stylesheet" id="hljs-light" href="{p}assets/vendor/highlightjs/github.min.css" media="(prefers-color-scheme: light)">
    <link rel="stylesheet" id="hljs-dark" href="{p}assets/vendor/highlightjs/github-dark.min.css" media="(prefers-color-scheme: dark)">
    <script>
    window.__applyTheme = function (t, persist) {{
        var r = document.documentElement, l = document.getElementById('hljs-light'), d = document.getElementById('hljs-dark');
        if (t === 'dark' || t === 'light') {{ r.setAttribute('data-theme', t); }} else {{ r.removeAttribute('data-theme'); }}
        if (l && d) {{
            if (t === 'dark') {{ l.media = 'not all'; d.media = 'all'; }}
            else if (t === 'light') {{ l.media = 'all'; d.media = 'not all'; }}
            else {{ l.media = '(prefers-color-scheme: light)'; d.media = '(prefers-color-scheme: dark)'; }}
        }}
        if (persist) {{ try {{ localStorage.setItem('theme', t); }} catch (e) {{}} }}
    }};
    try {{ var _t = localStorage.getItem('theme'); if (_t) window.__applyTheme(_t, false); }} catch (e) {{}}
    </script>"#,
        p = asset_prefix
    );

    // --- SEO / social metadata -------------------------------------------
    // `canonical_path` is the site-root-relative URL of this page without a
    // leading slash ("" for the home page, "math/sir.html" otherwise).
    let is_home = canonical_path.is_empty();
    let canonical = if is_home {
        format!("{}/", SITE_URL)
    } else {
        format!("{}/{}", SITE_URL, canonical_path)
    };

    let display_title = if title.trim().is_empty() {
        format!("{} · {}", SITE_NAME, SITE_TAGLINE)
    } else {
        title.to_string()
    };
    let head_title = if title.trim().is_empty() {
        format!("{} · {}", SITE_NAME, SITE_TAGLINE)
    } else {
        format!("{} · {}", title, SITE_NAME)
    };

    let og_type = if is_home { "website" } else { "article" };

    // Social share image. A page can override the default site card via front
    // matter `image:` (a site-root-relative asset path). For the default card we
    // know the exact type and dimensions; for a custom image we advertise the
    // MIME type from its extension but omit width/height, which we cannot know.
    const DEFAULT_OG_ALT: &str = "Wake Forest University IDEEEP concentration — Infectious Disease Ecology, Evolution and Epidemiology";
    let (og_image, og_image_meta, og_image_alt) = match page_image
        .map(|p| p.trim())
        .filter(|p| !p.is_empty())
    {
        Some(path) => {
            let norm = path.trim_start_matches("../").trim_start_matches('/');
            let url = format!("{}/{}", SITE_URL, norm);
            let lower = norm.to_ascii_lowercase();
            let mime = if lower.ends_with(".png") {
                "image/png"
            } else if lower.ends_with(".jpg") || lower.ends_with(".jpeg") {
                "image/jpeg"
            } else if lower.ends_with(".webp") {
                "image/webp"
            } else if lower.ends_with(".svg") {
                "image/svg+xml"
            } else {
                ""
            };
            let meta = if mime.is_empty() {
                String::new()
            } else {
                format!(
                    "\n    <meta property=\"og:image:type\" content=\"{}\">",
                    mime
                )
            };
            let alt = page_image_alt
                .map(str::trim)
                .filter(|a| !a.is_empty())
                .unwrap_or(&display_title);
            (url, meta, alt.to_string())
        }
        None => {
            let url = format!("{}/assets/og-image.png", SITE_URL);
            let meta = "\n    <meta property=\"og:image:type\" content=\"image/png\">\n    <meta property=\"og:image:width\" content=\"1200\">\n    <meta property=\"og:image:height\" content=\"630\">".to_string();
            (url, meta, DEFAULT_OG_ALT.to_string())
        }
    };

    let t_attr = escape_attr(&display_title);
    let d_attr = escape_attr(description);

    // JSON-LD structured data: a WebPage that is part of the site's WebSite.
    let json_ld = format!(
        r#"{{"@context":"https://schema.org","@type":"WebPage","name":"{name}","description":"{desc}","url":"{url}","inLanguage":"en","isPartOf":{{"@type":"WebSite","name":"{site} — {tagline}","url":"{site_url}/","potentialAction":{{"@type":"SearchAction","target":{{"@type":"EntryPoint","urlTemplate":"{site_url}/search.html?q={{search_term_string}}"}},"query-input":"required name=search_term_string"}}}},"publisher":{{"@type":"Organization","name":"Infectious Disease Epidemiology and Applied Statistics (IDEAS)","url":"https://wakeforestid.com"}}}}"#,
        name = escape_json(&display_title),
        desc = escape_json(description),
        url = escape_json(&canonical),
        site = escape_json(SITE_NAME),
        tagline = escape_json(SITE_TAGLINE),
        site_url = SITE_URL,
    );

    // Optional BreadcrumbList structured data (Home > Section > Page).
    let breadcrumb_ld = if breadcrumbs.len() >= 2 {
        let items: Vec<String> = breadcrumbs
            .iter()
            .enumerate()
            .map(|(i, (name, url))| {
                format!(
                    r#"{{"@type":"ListItem","position":{},"name":"{}","item":"{}"}}"#,
                    i + 1,
                    escape_json(name),
                    escape_json(url)
                )
            })
            .collect();
        format!(
            "\n    <script type=\"application/ld+json\">{{\"@context\":\"https://schema.org\",\"@type\":\"BreadcrumbList\",\"itemListElement\":[{}]}}</script>",
            items.join(",")
        )
    } else {
        String::new()
    };

    Ok(format!(
        r##"<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{head_title}</title>
    <meta name="description" content="{d_attr}">
    <link rel="canonical" href="{canonical}">
    <meta name="robots" content="{robots}">
    <meta name="author" content="Infectious Disease Epidemiology and Applied Statistics (IDEAS)">
    <meta name="theme-color" content="#12151a">
    <meta name="color-scheme" content="light dark">

    <!-- Open Graph -->
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="{site_name}">
    <meta property="og:title" content="{t_attr}">
    <meta property="og:description" content="{d_attr}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{og_image}">{og_image_meta}
    <meta property="og:image:alt" content="{og_image_alt}">
    <meta property="og:locale" content="en_US">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{t_attr}">
    <meta name="twitter:description" content="{d_attr}">
    <meta name="twitter:image" content="{og_image}">
    <meta name="twitter:image:alt" content="{og_image_alt}">

    <!-- Icons / PWA -->
    <link rel="icon" type="image/png" href="{ap}assets/favicon.png" />
    <link rel="apple-touch-icon" href="{ap}assets/apple-touch-icon.png" />
    <link rel="manifest" href="{ap}manifest.webmanifest" />

    <script type="application/ld+json">{json_ld}</script>{breadcrumb_ld}

    <link rel="stylesheet" href="{ap}assets/styles.css" type="text/css" />
    {font_preload}
    <!-- Self-hosted syntax highlighting (highlight.js) with light/dark themes -->
    {hljs_block}
    <script defer src="{ap}assets/vendor/highlightjs/highlight.bundle.min.js"></script>
    <script defer src="{ap}assets/nav.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        if (window.hljs) {{ hljs.highlightAll(); }}
    }});
    if ('serviceWorker' in navigator) {{
        window.addEventListener('load', function() {{
            navigator.serviceWorker.register('{ap}sw.js').catch(function() {{}});
        }});
    }}
    </script>
    {katex_css}
</head>
<body>
    <a class="skip-link" href="#content">Skip to content</a>
    {navbar}
    <main id="content">
        <div class="blogbody">
            {content}
        </div>
    </main>
    {footer_content}
</body>
</html>"##,
        head_title = escape_attr(&head_title),
        d_attr = d_attr,
        canonical = escape_attr(&canonical),
        robots = robots,
        og_type = og_type,
        site_name = SITE_NAME,
        t_attr = t_attr,
        og_image = escape_attr(&og_image),
        og_image_meta = og_image_meta,
        og_image_alt = escape_attr(&og_image_alt),
        json_ld = json_ld,
        breadcrumb_ld = breadcrumb_ld,
        font_preload = font_preload,
        hljs_block = hljs_block,
        katex_css = katex_css,
        navbar = navbar,
        content = content,
        footer_content = footer_content,
        ap = asset_prefix,
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
            // Skip leading-underscore directories (e.g. `_fragments`): they hold
            // reusable include fragments, not standalone pages, so they must not
            // be compiled to HTML on their own.
            if path
                .file_name()
                .and_then(|s| s.to_str())
                .map(|n| n.starts_with('_'))
                .unwrap_or(false)
            {
                continue;
            }
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


/// Whether a page (identified by its extensionless relative key, e.g.
/// `epidemiology/study-designs`) may be indexed by search engines: listed in
/// `sitemap.xml` and served with an indexable `robots` meta tag.
///
/// A page opts out generally with `hidden: true` in its front matter (the
/// `hidden` argument). The 404 page and the interest-form confirmation page are
/// always excluded — neither is a real indexable destination — regardless of
/// front matter.
fn is_indexable(rel_key: &str, hidden: bool) -> bool {
    !hidden
        && !rel_key.eq_ignore_ascii_case("404")
        && !rel_key.eq_ignore_ascii_case("interest-thank-you")
}

/// Whether a page belongs in the on-site full-text search index. A page opts
/// out with `hidden: true` in front matter (the `hidden` argument); the 404
/// page is never a useful hit. The interest-form confirmation page is
/// de-indexed (see `is_indexable`) but stays searchable.
fn is_search_indexable(rel_key: &str, hidden: bool) -> bool {
    !hidden && !rel_key.eq_ignore_ascii_case("404")
}

/// Build a client-loadable FTS4 SQLite index (`dist/search.db`) over every page.
/// One row per page: title, extracted content, relative URL, category, date.
/// The browser queries this with SQL.js (see `generate_search_page`).
fn build_search_index(
    markdown_files: &[(PathBuf, PathBuf, String)],
    hidden_pages: &std::collections::HashSet<String>,
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

        // Skip pages that should not surface as search hits (see
        // `is_search_indexable`): the 404 page and any `hidden: true` page.
        if !is_search_indexable(&rel_key, hidden_pages.contains(&rel_key)) {
            continue;
        }

        let content = fs::read_to_string(full_path)?;
        let (_, markdown_content) = extract_frontmatter(&content);
        // Expand template fragments so injected sections (course/university
        // policies, etc.) are searchable on the pages that include them.
        let markdown_content = expand_includes(markdown_content);
        let content_text = extract_search_text(&markdown_content);

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

/// Write `dist/sitemap.xml` listing every published page plus the search page.
/// The 404 page is excluded (it should not be indexed). URLs are absolute and
/// use the `.html` paths Netlify serves; the home page canonicalises to "/".
fn write_sitemap(
    markdown_files: &[(PathBuf, PathBuf, String)],
    hidden_pages: &std::collections::HashSet<String>,
    dist_dir: &Path,
) -> Result<(), Box<dyn std::error::Error>> {
    let mut urls: Vec<String> = Vec::new();

    for (_, relative_path, _) in markdown_files {
        let rel_key = relative_path
            .with_extension("")
            .to_string_lossy()
            .replace('\\', "/");

        // Keep non-indexable pages (404, form confirmation, any `hidden: true`
        // page) out of the sitemap. See `is_indexable`.
        if !is_indexable(&rel_key, hidden_pages.contains(&rel_key)) {
            continue;
        }

        let loc = if rel_key == "index" {
            format!("{}/", SITE_URL)
        } else {
            format!("{}/{}.html", SITE_URL, rel_key)
        };
        urls.push(loc);
    }
    // The interactive search page is a real, linkable destination.
    urls.push(format!("{}/search.html", SITE_URL));

    urls.sort();
    urls.dedup();

    let mut xml = String::from(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n",
    );
    for loc in &urls {
        // Home page is the priority root; hubs and content follow.
        let priority = if loc == &format!("{}/", SITE_URL) { "1.0" } else { "0.7" };
        xml.push_str(&format!(
            "  <url>\n    <loc>{}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>{}</priority>\n  </url>\n",
            escape_attr(loc),
            priority
        ));
    }
    xml.push_str("</urlset>\n");

    let path = dist_dir.join("sitemap.xml");
    fs::write(&path, xml)?;
    println!("Generated: {}", path.display());
    Ok(())
}

/// Write `dist/robots.txt`: allow all crawlers and advertise the sitemap.
fn write_robots(dist_dir: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let body = format!(
        "User-agent: *\nAllow: /\n\nSitemap: {}/sitemap.xml\n",
        SITE_URL
    );
    let path = dist_dir.join("robots.txt");
    fs::write(&path, body)?;
    println!("Generated: {}", path.display());
    Ok(())
}

/// Write `dist/_headers` (read by Netlify from the publish root). Ensures the
/// service worker is revalidated on every load so updates ship promptly, and
/// that the manifest is served with the correct content type.
fn write_headers(dist_dir: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let body = "\
/sw.js
  Cache-Control: no-cache
/manifest.webmanifest
  Content-Type: application/manifest+json; charset=utf-8
  Cache-Control: public, max-age=86400
/assets/figures/*
  Cache-Control: public, max-age=604800
";
    let path = dist_dir.join("_headers");
    fs::write(&path, body)?;
    println!("Generated: {}", path.display());
    Ok(())
}

/// Write `dist/manifest.webmanifest` describing the installable web app.
/// Icon paths are absolute so they resolve from any page depth.
fn write_manifest(dist_dir: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let manifest = format!(
        r##"{{
  "name": "{name}",
  "short_name": "{short}",
  "description": "{desc}",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "lang": "en-US",
  "icons": [
    {{ "src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" }},
    {{ "src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any" }},
    {{ "src": "/assets/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }}
  ]
}}
"##,
        name = escape_json(&format!("{} — {}", SITE_NAME, SITE_TAGLINE)),
        short = escape_json(SITE_NAME),
        desc = escape_json(SITE_DESCRIPTION),
    );
    let path = dist_dir.join("manifest.webmanifest");
    fs::write(&path, manifest)?;
    println!("Generated: {}", path.display());
    Ok(())
}

/// Write `dist/sw.js`: a small service worker giving the site offline support.
/// Documents are network-first (fresh content when online, cached fallback
/// offline); same-origin static assets are cache-first. Cross-origin CDN
/// requests are left to the network. Bump `CACHE` to invalidate old caches.
fn write_service_worker(dist_dir: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let sw = r#"// IDEEEP service worker — offline support + installability.
const CACHE = 'ideeep-v1';
const CORE = [
  '/',
  '/index.html',
  '/search.html',
  '/manifest.webmanifest',
  '/assets/styles.css',
  '/assets/icon-192.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(CORE)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // Leave cross-origin (CDN) requests to the network.
  if (url.origin !== self.location.origin) return;

  const isDocument = req.mode === 'navigate' || req.destination === 'document';

  if (isDocument) {
    // Network-first: prefer fresh HTML, fall back to cache when offline.
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match(req).then((m) => m || caches.match('/index.html')))
    );
  } else {
    // Cache-first for static assets.
    event.respondWith(
      caches.match(req).then(
        (m) =>
          m ||
          fetch(req).then((res) => {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
            return res;
          })
      )
    );
  }
});
"#;
    let path = dist_dir.join("sw.js");
    fs::write(&path, sw)?;
    println!("Generated: {}", path.display());
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

    // Pages marked `hidden: true` in front matter are unlisted: excluded from
    // the sitemap and the search index (both built after this loop). Collected
    // here so those later passes don't have to re-read every file's front matter.
    let mut hidden_pages: std::collections::HashSet<String> = std::collections::HashSet::new();

    // Process each markdown file
    for (full_path, relative_path, title) in &markdown_files {
        let content = fs::read_to_string(full_path)?;
        let (frontmatter, markdown_content) = extract_frontmatter(&content);
        let page_hidden = frontmatter.as_ref().and_then(|fm| fm.hidden).unwrap_or(false);
        // Schedule pages opt into build-time row sorting so hand-edited times
        // reorder the rendered agenda. `sorted_body` owns the rewritten Markdown
        // only when the flag is set; otherwise the original slice is used.
        let sorted_body;
        let body: &str = match frontmatter.as_ref().and_then(|fm| fm.sort_schedule) {
            Some(true) => {
                sorted_body = sort_schedule_tables(markdown_content);
                &sorted_body
            }
            _ => markdown_content,
        };
        let html_content = markdown_to_html(body, &markdown_file_names);

        // Give headings ids, then add an "On this page" TOC where a page opts in
        // with `toc: true` in its front matter (used on the section hub pages).
        let (html_content, headings) = add_heading_ids(&html_content);
        let toc_enabled = frontmatter.as_ref().and_then(|fm| fm.toc).unwrap_or(false);
        let html_content = if toc_enabled && !headings.is_empty() {
            let toc = build_toc(&headings);
            let with_lead = html_content.replacen("<p>", "<p class=\"lead\">", 1);
            match with_lead.find("<h2") {
                Some(pos) => format!("{}{}{}", &with_lead[..pos], toc, &with_lead[pos..]),
                None => format!("{}{}", toc, with_lead),
            }
        } else {
            html_content
        };

        let rel_key = relative_path.with_extension("")
            .to_string_lossy()
            .replace('\\', "/");

        // Optional per-page social/share image (Open Graph + Twitter). Read
        // before `frontmatter` is consumed for the description below.
        let page_image = frontmatter
            .as_ref()
            .and_then(|fm| fm.image.clone())
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty());
        let page_image_alt = frontmatter
            .as_ref()
            .and_then(|fm| fm.image_alt.clone())
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty());

        // Per-page meta description: front matter wins, else first-paragraph text.
        let description = frontmatter
            .and_then(|fm| fm.description)
            .map(|d| d.trim().to_string())
            .filter(|d| !d.is_empty())
            .unwrap_or_else(|| extract_description(markdown_content, SITE_DESCRIPTION));

        // Canonical URL path (site-root-relative, no leading slash). The home
        // page canonicalises to "/" via an empty path.
        let canonical_path = if rel_key == "index" {
            String::new()
        } else {
            format!("{}.html", rel_key)
        };
        let canonical_url = if canonical_path.is_empty() {
            format!("{}/", SITE_URL)
        } else {
            format!("{}/{}", SITE_URL, canonical_path)
        };

        // Record hidden pages so the sitemap and search passes can skip them.
        if page_hidden {
            hidden_pages.insert(rel_key.clone());
        }

        // Non-indexable pages (404, form confirmation, any `hidden: true` page)
        // get `noindex`; everything else is indexable. See `is_indexable`.
        let robots = if is_indexable(&rel_key, page_hidden) {
            "index, follow, max-image-preview:large"
        } else {
            "noindex, follow"
        };

        // Breadcrumb trail: Home › [Section hub] › Page. Skipped for the home
        // page; the section crumb is added only when the page lives under a
        // directory that has a hub page of the same name.
        let mut breadcrumbs: Vec<(String, String)> = Vec::new();
        if rel_key != "index" {
            breadcrumbs.push(("Home".to_string(), format!("{}/", SITE_URL)));
            if let Some(section) = relative_path
                .parent()
                .and_then(|p| p.components().next())
                .map(|c| c.as_os_str().to_string_lossy().to_string())
                .filter(|s| !s.is_empty())
            {
                if let Some(hub_title) = markdown_titles.get(&section) {
                    breadcrumbs.push((hub_title.clone(), format!("{}/{}.html", SITE_URL, section)));
                }
            }
            breadcrumbs.push((title.clone(), canonical_url.clone()));
        }

        // Calculate asset prefix based on depth (e.g., "../" for one level deep)
        let asset_prefix = calculate_asset_prefix(relative_path);

        // Generate navbar HTML with current page highlighted
        let navbar = generate_navbar(&navbar_items, true, dropdowns.as_ref(), &markdown_titles, Some(&rel_key), &asset_prefix);

        let html_output = generate_html(title, &description, &canonical_path, robots, &breadcrumbs, &html_content, &navbar, &asset_prefix, page_image.as_deref(), page_image_alt.as_deref())?;

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
    build_search_index(&markdown_files, &hidden_pages, dist_dir)?;

    // Emit the interactive search page at the dist root (asset_prefix = "").
    let search_navbar = generate_navbar(
        &navbar_items,
        true,
        dropdowns.as_ref(),
        &markdown_titles,
        Some("search"),
        "",
    );
    let search_description =
        "Full-text search across IDEEEP: quantitative methods, programming, epidemiology, diagnostics, syllabi, and research.";
    let search_breadcrumbs = vec![
        ("Home".to_string(), format!("{}/", SITE_URL)),
        ("Search".to_string(), format!("{}/search.html", SITE_URL)),
    ];
    let search_html = generate_html(
        "Search",
        search_description,
        "search.html",
        "index, follow, max-image-preview:large",
        &search_breadcrumbs,
        &search_page_content(),
        &search_navbar,
        "",
        None,
        None,
    )?;
    let search_path = dist_dir.join("search.html");
    fs::write(&search_path, search_html)?;
    println!("Generated: {}", search_path.display());

    // Emit SEO/PWA support files: sitemap, robots, manifest, service worker.
    write_sitemap(&markdown_files, &hidden_pages, dist_dir)?;
    write_robots(dist_dir)?;
    write_manifest(dist_dir)?;
    write_service_worker(dist_dir)?;
    write_headers(dist_dir)?;

    // Copy assets to dist after building
    copy_assets_to_dist()?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashSet;

    fn render(md: &str) -> String {
        markdown_to_html(md, &HashSet::new())
    }

    /// Regression: KaTeX emits an ASCII tilde (`~`) for `\tilde` accents. Math
    /// used to be spliced into the Markdown stream before parsing, so GFM
    /// strikethrough (enabled via `Options::all`) paired those tildes into
    /// `<del>` runs, dropping mismatched `<del>`/`</del>` tags inside the KaTeX
    /// spans. That corrupted the DOM and truncated the page at the first
    /// `\tilde`. The math must render without any strikethrough artifacts.
    #[test]
    fn tilde_accent_does_not_produce_strikethrough() {
        let html = render(r"A bullet with $\tilde F_x$ then $\tilde r_i$ accents.");
        assert!(
            !html.contains("<del>") && !html.contains("</del>"),
            "KaTeX \\tilde output must not be mangled into <del> strikethrough:\n{html}"
        );
        // The math itself must actually have rendered.
        assert!(html.contains("class=\"katex"), "expected rendered KaTeX:\n{html}");
    }

    /// Reproduces the page structure that failed: a display-math block followed
    /// by prose containing `\tilde` inline math. The corruption used to swallow
    /// everything after the block, so assert the trailing content survives.
    #[test]
    fn content_after_tilde_math_is_not_truncated() {
        let md = "Intro paragraph.\n\n\
                  \\[ \\operatorname{Var}(F) = \\sigma_S^2 + \\sigma_T^2 + \\sigma_{ST}^2 \\]\n\n\
                  - **Pure spatial**, $\\sigma_S^2=\\operatorname{Var}_x(\\tilde F_x)$: how patches differ.\n\n\
                  TRAILING_SENTINEL_TEXT";
        let html = render(md);
        assert!(
            html.contains("TRAILING_SENTINEL_TEXT"),
            "content after \\tilde math was truncated:\n{html}"
        );
        assert!(!html.contains("<del>"), "unexpected strikethrough from math:\n{html}");
    }

    /// The placeholder tokens used to shield math from the Markdown parser must
    /// never survive into the final HTML.
    #[test]
    fn math_placeholders_do_not_leak() {
        let html = render(r"Inline $x^2$ and display \[ y = mx + b \] math.");
        assert!(
            !html.contains(MATH_PLACEHOLDER_OPEN) && !html.contains(MATH_PLACEHOLDER_CLOSE),
            "math placeholder token leaked into output:\n{html}"
        );
        assert!(html.contains("class=\"katex"), "expected rendered KaTeX:\n{html}");
    }

    /// Guard the fix from over-correcting: genuine Markdown strikethrough in
    /// prose (`~~...~~`) must still render as `<del>`.
    #[test]
    fn prose_strikethrough_still_works() {
        let html = render("This is ~~struck through~~ text.");
        assert!(
            html.contains("<del>struck through</del>"),
            "GFM strikethrough regressed for real prose:\n{html}"
        );
    }

    /// A missing fragment must degrade to a visible, logged marker rather than
    /// silently vanishing — a dropped policy section should be obvious.
    #[test]
    fn missing_fragment_is_visible() {
        let html = render(":::{definitely-not-a-real-fragment.md}:::");
        assert!(
            html.contains("Missing template fragment")
                && html.contains("definitely-not-a-real-fragment.md"),
            "missing include should render a visible marker:\n{html}"
        );
    }

    /// A shortcode that tries to escape the fragments directory is refused.
    #[test]
    fn unsafe_fragment_include_is_refused() {
        let html = render(":::{../../etc/passwd}:::");
        assert!(
            !html.contains("root:") && html.contains("unsafe fragment include"),
            "path-traversal include must be refused:\n{html}"
        );
    }

    /// Text with no shortcode is passed through untouched (fast path).
    #[test]
    fn expand_includes_is_noop_without_shortcode() {
        let md = "Just a normal paragraph with a :: colon but no shortcode.";
        assert_eq!(expand_includes(md), md);
    }

    /// Build a throwaway fragments directory for an include test, returning its
    /// path. Uses the process id so parallel test runs don't collide, and is
    /// cleaned up by the caller.
    fn write_fixtures(tag: &str, files: &[(&str, &str)]) -> std::path::PathBuf {
        let dir = std::env::temp_dir().join(format!("ideeep-frag-{}-{}", tag, std::process::id()));
        let _ = fs::remove_dir_all(&dir);
        fs::create_dir_all(&dir).unwrap();
        for (name, body) in files {
            fs::write(dir.join(name), body).unwrap();
        }
        dir
    }

    /// A fragment that includes itself must be caught, not recursed into
    /// forever. If the guard were missing this test would hang rather than fail.
    #[test]
    fn direct_self_reference_is_broken() {
        let dir = write_fixtures("self", &[("a.md", "top\n\n:::{a.md}:::\n\nbottom")]);
        let out = expand_includes_from(":::{a.md}:::", &dir);
        let _ = fs::remove_dir_all(&dir);
        assert!(
            out.contains("recursive fragment include: a.md"),
            "self-include should be refused with a marker:\n{out}"
        );
        // The first level of `a` still expands; only the re-entry is cut.
        assert!(out.contains("top") && out.contains("bottom"));
    }

    /// A mutual cycle `a → b → a` must terminate at the re-entry of `a`, leaving
    /// a marker rather than looping. This is the exact scenario from the report:
    /// a includes b, b includes a.
    #[test]
    fn mutual_cycle_is_broken() {
        let dir = write_fixtures(
            "mutual",
            &[
                ("a.md", "A-start\n\n:::{b.md}:::\n\nA-end"),
                ("b.md", "B-start\n\n:::{a.md}:::\n\nB-end"),
            ],
        );
        let out = expand_includes_from("page\n\n:::{a.md}:::", &dir);
        let _ = fs::remove_dir_all(&dir);
        // Both fragments expanded one level deep, and the loop back into `a` was
        // cut with a marker.
        assert!(out.contains("A-start") && out.contains("A-end"), "a not expanded:\n{out}");
        assert!(out.contains("B-start") && out.contains("B-end"), "b not expanded:\n{out}");
        assert!(
            out.contains("recursive fragment include: a.md"),
            "the a→b→a cycle should be cut with a marker:\n{out}"
        );
    }

    /// A diamond (the same fragment included on two independent branches) is NOT
    /// a cycle and must expand in both places — the guard must not over-fire.
    #[test]
    fn diamond_include_is_allowed_twice() {
        let dir = write_fixtures(
            "diamond",
            &[
                ("leaf.md", "LEAF"),
                ("left.md", ":::{leaf.md}:::"),
                ("right.md", ":::{leaf.md}:::"),
            ],
        );
        let out = expand_includes_from(":::{left.md}:::\n\n:::{right.md}:::", &dir);
        let _ = fs::remove_dir_all(&dir);
        assert_eq!(
            out.matches("LEAF").count(),
            2,
            "leaf should expand on both branches, not be treated as a cycle:\n{out}"
        );
        assert!(!out.contains("recursive fragment include"), "diamond wrongly flagged:\n{out}");
    }

    /// A mapping-style dropdown (custom label -> URL) must resolve relative URLs
    /// against the current page's asset_prefix, so anchor links like
    /// `programs.html#curriculum` don't break on nested pages. Absolute and pure
    /// fragment targets are emitted verbatim.
    #[test]
    fn mapping_dropdown_links_respect_asset_prefix() {
        use std::collections::HashMap;
        let mut inner = serde_yaml::Mapping::new();
        inner.insert(
            serde_yaml::Value::String("Courses & Syllabi".to_string()),
            serde_yaml::Value::String("programs.html#curriculum".to_string()),
        );
        inner.insert(
            serde_yaml::Value::String("Home".to_string()),
            serde_yaml::Value::String("https://example.com".to_string()),
        );
        let mut dropdowns: HashMap<String, serde_yaml::Value> = HashMap::new();
        dropdowns.insert("Program".to_string(), serde_yaml::Value::Mapping(inner));
        let items = vec![NavbarItem::Dropdown("Program".to_string())];
        let titles: HashMap<String, String> = HashMap::new();

        // Rendered from a nested page (asset_prefix "../").
        let nav = generate_navbar(&items, true, Some(&dropdowns), &titles, Some("math/sir"), "../");
        assert!(
            nav.contains("href=\"../programs.html#curriculum\""),
            "relative mapping URL must be prefixed with asset_prefix:\n{nav}"
        );
        assert!(
            nav.contains(">Courses & Syllabi</a>"),
            "mapping key should be used as the link label:\n{nav}"
        );
        // External URLs are left untouched and open in a new tab.
        assert!(
            nav.contains("href=\"https://example.com\" target=\"_blank\""),
            "external mapping URL must be emitted verbatim with target=_blank:\n{nav}"
        );

        // From the site root there is no prefix to add.
        let nav_root = generate_navbar(&items, true, Some(&dropdowns), &titles, Some("index"), "");
        assert!(
            nav_root.contains("href=\"programs.html#curriculum\""),
            "root-level mapping URL must be unprefixed:\n{nav_root}"
        );
    }

    /// With no per-page `image:`, the shared social card is used and its known
    /// type/dimensions are advertised for both Open Graph and Twitter.
    #[test]
    fn og_image_defaults_to_site_card() {
        let html = generate_html(
            "Quantitative Methods", "desc", "math.html", "index, follow",
            &[], "<p>body</p>", "<nav></nav>", "../", None, None,
        )
        .unwrap();
        let card = format!("{}/assets/og-image.png", SITE_URL);
        assert!(html.contains(&format!("property=\"og:image\" content=\"{card}\"")), "default og:image missing:\n{html}");
        assert!(html.contains(&format!("name=\"twitter:image\" content=\"{card}\"")), "default twitter:image missing:\n{html}");
        assert!(html.contains("property=\"og:image:width\" content=\"1200\""), "default card must keep its known width:\n{html}");
        assert!(html.contains("property=\"og:image:height\" content=\"630\""), "default card must keep its known height:\n{html}");
    }

    /// A per-page `image:` overrides the share card for Open Graph and Twitter,
    /// resolves to an absolute URL, advertises the MIME type from its extension,
    /// and drops the fixed dimensions (unknown for an arbitrary image). A leading
    /// `../` or `/` in the path is tolerated. The alt falls back to the title.
    #[test]
    fn og_image_uses_per_page_override() {
        let html = generate_html(
            "Diagnostics", "desc", "diagnostics.html", "index, follow",
            &[], "<p>body</p>", "<nav></nav>", "", Some("../assets/photos/serology-antibody-test.jpg"), None,
        )
        .unwrap();
        let img = format!("{}/assets/photos/serology-antibody-test.jpg", SITE_URL);
        assert!(html.contains(&format!("property=\"og:image\" content=\"{img}\"")), "per-page og:image not applied:\n{html}");
        assert!(html.contains(&format!("name=\"twitter:image\" content=\"{img}\"")), "per-page twitter:image not applied:\n{html}");
        assert!(html.contains("property=\"og:image:type\" content=\"image/jpeg\""), "jpeg MIME type should be advertised:\n{html}");
        assert!(!html.contains("og:image:width"), "custom image must not claim the default card's dimensions:\n{html}");
        assert!(html.contains("property=\"og:image:alt\" content=\"Diagnostics\""), "image alt should fall back to the page title:\n{html}");
    }

    /// Any page can opt out of indexing and search with `hidden: true` in front
    /// matter (the `hidden` argument): it is then excluded from the sitemap,
    /// `robots`, and search, while an ordinary page (`hidden = false`) stays
    /// both indexable and searchable. This is the general mechanism the schedule
    /// draft uses instead of a hardcoded page name.
    #[test]
    fn hidden_flag_excludes_a_page_from_indexing_and_search() {
        assert!(!is_indexable("schedule", true), "hidden page out of sitemap/robots");
        assert!(!is_search_indexable("schedule", true), "hidden page out of search");

        // A regular page (not hidden) stays indexable and searchable.
        assert!(is_indexable("epidemiology/study-designs", false));
        assert!(is_search_indexable("epidemiology/study-designs", false));
    }

    /// The two visibility predicates keep their established, deliberately
    /// different behaviour for the built-in special pages, independent of the
    /// `hidden` flag: the 404 page is out of everything; the interest-form
    /// confirmation is de-indexed but still searchable.
    #[test]
    fn indexing_and_search_exclusion_sets_are_preserved() {
        assert!(!is_indexable("404", false));
        assert!(!is_search_indexable("404", false));

        assert!(!is_indexable("interest-thank-you", false), "confirmation page is not indexed");
        assert!(is_search_indexable("interest-thank-you", false), "confirmation page stays searchable");
    }

    /// A slot's start time parses meridiem-aware, so a program day orders
    /// morning → noon → afternoon rather than lexically (which would sort the
    /// "1" of 1 PM before the "9" of 9 AM).
    #[test]
    fn start_minutes_orders_morning_before_afternoon() {
        assert_eq!(start_minutes("9-9:50"), 9 * 60);
        assert!(start_minutes("9-9:50") < start_minutes("11-11:50"));
        assert!(start_minutes("11-11:50") < start_minutes("12-1p")); // 11 AM < noon
        assert!(start_minutes("12-1p") < start_minutes("1-1:50")); // noon < 1 PM
        assert!(start_minutes("1-1:50") < start_minutes("3-3:50")); // 1 PM < 3 PM
    }

    /// `sort_schedule: true` reorders a table's rows by weekday then start time,
    /// so an out-of-order (or hand-edited) Markdown schedule renders in order.
    /// The 11 AM row must precede the 1 PM row, which lexical sorting gets wrong.
    #[test]
    fn schedule_table_sorts_by_day_then_time() {
        let md = "\
| Day | Time | Session |
|-----|------|---------|
| Tue | 9-9:50 | Bee |
| Mon | 1-1:50 | Cee |
| Mon | 9-9:50 | Ayy |
| Mon | 11-11:50 | Dee |
";
        let out = sort_schedule_tables(md);
        let sessions: Vec<String> = out
            .lines()
            .skip(2)
            .filter(|l| l.contains('|'))
            .map(|l| l.split('|').nth(3).unwrap().trim().to_string())
            .collect();
        assert_eq!(
            sessions,
            vec!["Ayy", "Dee", "Cee", "Bee"],
            "rows should sort by weekday then start time (11 AM before 1 PM):\n{out}"
        );
    }

    /// Tables without a `Day` or `Time` column are left exactly as written, and
    /// prose around a schedule table is preserved.
    #[test]
    fn sort_schedule_only_touches_schedule_tables() {
        let plain = "\
| Name | Score |
|------|-------|
| Zoe | 2 |
| Amy | 1 |
";
        assert_eq!(sort_schedule_tables(plain), plain, "no Day/Time column: leave untouched");

        let doc = "Intro line.\n\n| Day | Time |\n|-----|------|\n| Mon | 10-10:50 |\n| Mon | 9-9:50 |\n\nAfter.\n";
        let out = sort_schedule_tables(doc);
        assert!(out.starts_with("Intro line.\n\n"), "leading prose preserved:\n{out}");
        assert!(out.trim_end().ends_with("After."), "trailing prose preserved:\n{out}");
        assert!(
            out.find("9-9:50").unwrap() < out.find("10-10:50").unwrap(),
            "9 AM should sort before 10 AM:\n{out}"
        );
    }

    /// The include shortcode parses an optional `; schedule=…` flag after the
    /// fragment name, tolerating an omitted `.md`, casing, and truthy spellings,
    /// while leaving a plain name un-sorted.
    #[test]
    fn parse_include_spec_reads_schedule_option() {
        assert_eq!(parse_include_spec("foo"), ("foo.md".to_string(), false));
        assert_eq!(parse_include_spec("foo.md"), ("foo.md".to_string(), false));
        assert_eq!(
            parse_include_spec("fellow-schedule-2026; schedule=true"),
            ("fellow-schedule-2026.md".to_string(), true)
        );
        assert_eq!(
            parse_include_spec("fellow-schedule-2026; schedule=TRUE"),
            ("fellow-schedule-2026.md".to_string(), true)
        );
        assert_eq!(parse_include_spec("foo; schedule").1, true, "bare flag means on");
        assert_eq!(parse_include_spec("foo; schedule=false").1, false);
        assert_eq!(parse_include_spec("foo; other=1").1, false, "unknown option ignored");
    }

    /// A fragment embedded with `:::{name; schedule=true}:::` has its schedule
    /// table sorted as it is spliced in, so a reusable, out-of-order agenda
    /// fragment renders in day/time order; without the flag it is spliced as
    /// written.
    #[test]
    fn fragment_include_sorts_when_schedule_flag_set() {
        let fragment = "\
| Day | Time | Session |
|-----|------|---------|
| Mon | 1-1:50 | Afternoon |
| Mon | 9-9:50 | Morning |
";
        let dir = write_fixtures("sched-opt", &[("sched.md", fragment)]);

        let sorted = expand_includes_from(":::{sched; schedule=true}:::", &dir);
        let plain = expand_includes_from(":::{sched}:::", &dir);
        let _ = fs::remove_dir_all(&dir);

        assert!(
            sorted.find("Morning").unwrap() < sorted.find("Afternoon").unwrap(),
            "schedule=true must sort the fragment (9 AM before 1 PM):\n{sorted}"
        );
        assert!(
            plain.find("Afternoon").unwrap() < plain.find("Morning").unwrap(),
            "without the flag the fragment is spliced as written:\n{plain}"
        );
    }

    // --- Heading permalink anchors ---------------------------------------

    /// Every h2/h3 keeps its stable id and now carries a trailing permalink
    /// anchor pointing at that id, so a reader can deep-link any section.
    #[test]
    fn headings_get_permalink_anchors() {
        let (html, headings) = add_heading_ids("<h2>Worked Example</h2><h3>In Code</h3>");
        assert!(
            html.contains("<h2 id=\"worked-example\">Worked Example<a class=\"heading-anchor\" href=\"#worked-example\""),
            "h2 should keep its id and gain a permalink anchor:\n{html}"
        );
        assert!(
            html.contains("<h3 id=\"in-code\">In Code<a class=\"heading-anchor\" href=\"#in-code\""),
            "h3 should keep its id and gain a permalink anchor:\n{html}"
        );
        // The anchor must not leak into the TOC/heading label text.
        assert_eq!(headings[0].2, "Worked Example");
        assert!(!headings[0].2.contains('#'), "anchor char must stay out of the TOC label");
    }

    // --- Spoiler / details disclosure blocks -----------------------------

    /// A `:::spoiler <label>` block becomes a native `<details>` with the given
    /// summary, and its body is still rendered as Markdown (bold, here).
    #[test]
    fn spoiler_block_renders_details_with_custom_summary() {
        let html = render(":::spoiler Show the solution\nThe answer is **42**.\n:::");
        assert!(html.contains("<details class=\"spoiler\">"), "expected a details wrapper:\n{html}");
        assert!(html.contains("<summary>Show the solution</summary>"), "custom summary missing:\n{html}");
        assert!(html.contains("<strong>42</strong>"), "body should be parsed as Markdown:\n{html}");
        assert!(html.contains("</details>"), "details must be closed:\n{html}");
    }

    /// The summary label is fully configurable — any wording works — and the
    /// `:::details` alias behaves the same as `:::spoiler`.
    #[test]
    fn spoiler_summary_is_configurable_and_has_alias() {
        assert!(render(":::spoiler Reveal the derivation\nx\n:::")
            .contains("<summary>Reveal the derivation</summary>"));
        assert!(render(":::details See more\ny\n:::")
            .contains("<summary>See more</summary>"));
        // A bare opener falls back to the default label.
        assert!(render(":::spoiler\nz\n:::").contains("<summary>Show more</summary>"));
    }

    /// Spoilers may nest: an inner `:::` must not close the outer block early.
    #[test]
    fn spoiler_blocks_nest() {
        let html = render(":::spoiler Outer\nbefore\n:::spoiler Inner\ndeep\n:::\nafter\n:::");
        assert_eq!(html.matches("<details class=\"spoiler\">").count(), 2, "both levels should expand:\n{html}");
        assert!(html.contains("<summary>Outer</summary>") && html.contains("<summary>Inner</summary>"), "both summaries present:\n{html}");
        assert!(html.contains("deep") && html.contains("after"), "inner and trailing content survive:\n{html}");
    }

    /// An opener with no matching close is left untouched so stray text is not
    /// swallowed into a runaway details block.
    #[test]
    fn unterminated_spoiler_is_left_alone() {
        let html = render(":::spoiler Oops\nno closing fence here");
        assert!(!html.contains("<details"), "an unterminated opener must not open a details:\n{html}");
    }

    // --- Figure numbering, captions, and cross-references ----------------

    /// A lone block image becomes a numbered `<figure>` whose caption is the alt
    /// text, matching the site's "alt doubles as caption" convention.
    #[test]
    fn block_image_becomes_numbered_figure() {
        let html = render("![Epidemic curve over time](../assets/figures/curve.svg)");
        assert!(html.contains("<figure id=\"figure-1\" class=\"figure\">"), "expected a numbered figure wrapper:\n{html}");
        assert!(html.contains("<figcaption><span class=\"figure-label\">Figure 1.</span> Epidemic curve over time</figcaption>"), "caption should carry the number and alt text:\n{html}");
        assert!(!html.contains("<p><img"), "the image paragraph should be replaced by a figure:\n{html}");
    }

    /// A `fig:`-titled image is labelled for cross-referencing: it gets a stable
    /// id, the sentinel title is stripped from the <img>, and `[@fig:…]` resolves
    /// to a numbered link — regardless of whether the reference precedes or
    /// follows the figure in the document.
    #[test]
    fn figure_label_and_cross_reference_resolve() {
        let html = render("As shown in [@fig:curve], cases peak early.\n\n![Cases](curve.svg \"fig:curve\")");
        assert!(html.contains("<figure id=\"fig-curve\" class=\"figure\">"), "labelled figure should use the label as its id:\n{html}");
        assert!(!html.contains("title=\"fig:curve\""), "the fig: sentinel title must be stripped from the img:\n{html}");
        assert!(html.contains("<a class=\"fig-ref\" href=\"#fig-curve\">Figure 1</a>"), "reference should resolve to a numbered link even when it precedes the figure:\n{html}");
    }

    /// A decorative image (empty alt, no label) is left as a plain image, and an
    /// unresolved `[@fig:…]` reference renders a visible error marker.
    #[test]
    fn decorative_image_kept_and_unresolved_ref_is_loud() {
        let deco = render("![](../assets/spacer.svg)");
        assert!(!deco.contains("<figure"), "an empty-alt image must not be numbered:\n{deco}");

        let bad = render("See [@fig:missing] please.");
        assert!(bad.contains("fig-ref-error") && bad.contains("fig:missing"), "an unresolved reference should be a loud marker:\n{bad}");
    }
}

