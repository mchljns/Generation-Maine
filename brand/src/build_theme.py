"""The WordPress theme takes its stylesheet, its mural data, its marks and its images from the same sources as the splash page,
so the two never drift. Run after build_splash.py.

  python3 brand/src/build_theme.py

Writes: generation-maine/style.css, assets/data/mural.json, inc/marks.php, assets/img/*.svg
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gmlib import ROOT, write
import build_splash as SP

THEME = os.path.join(ROOT, "generation-maine")
SIG = os.path.join(ROOT, "brand", "identity", "logo-maine", "signature")

HEADER = """/*
Theme Name: Generation Maine
Theme URI: https://generationmaine.org
Author: Green Falls
Description: One-page block theme for Generation Maine. Every piece of copy is a block; every creator is a post. No build step, no plugins.
Version: 2.0.0
Requires at least: 6.5
Tested up to: 6.8
Requires PHP: 7.4
License: GNU General Public License v2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: generation-maine
*/

/* This stylesheet is generated from brand/src/build_theme.py, which shares its CSS with the splash page mockup.
   Edit brand/src/build_splash.py (the CSS block) or the WordPress additions in build_theme.py, then rebuild. */

/* The page's names for the theme.json palette, so the shared CSS reads the same here as on the mockup. */
:root{
  --sp:var(--wp--preset--color--primary);--pine:var(--wp--preset--color--pine);--bi:var(--wp--preset--color--base);--ink:var(--wp--preset--color--contrast);
  --mg:var(--wp--preset--color--accent);--sage:var(--wp--preset--color--sage);--moss:var(--wp--preset--color--moss);--sand:var(--wp--preset--color--sand);
  --white:#FFFFFF;--snow:var(--wp--preset--color--white);--muted:var(--wp--preset--color--muted);--stone:#5E6A63;
  --display:var(--wp--preset--font-family--display);--body:var(--wp--preset--font-family--body);
}
"""

# What WordPress markup needs on top of the shared CSS: block wrappers, the editable nav, the follow row as groups, the quote block.
WP_ADDITIONS = """
/* ---------- WordPress additions ---------- */
.wp-site-blocks>*+*{margin-block-start:0}
/* the shared CSS sets its own spacing; the block editor's flow gaps would double it and push the capsule's pills off center */
.wp-site-blocks .is-layout-flow>*+*{margin-block-start:0}
.wp-site-blocks .is-layout-flex{gap:0}
.top nav.is-layout-flex{gap:30px}.top.scrolled nav.is-layout-flex{gap:4px}
.hero .ctas.is-layout-flex{gap:18px}
.wp-block-group.w{max-width:1280px;margin:0 auto;padding-inline:var(--M)}
.admin-bar .top{top:var(--wp-admin--admin-bar--height,32px)}
.admin-bar .sheet{padding-top:calc(68px + var(--wp-admin--admin-bar--height,32px))}
h1.wp-block-heading,h2.wp-block-heading,h3.wp-block-heading{margin:0}
.hero .wp-block-buttons{margin:0}
.hero .ctas{display:flex;gap:18px;flex-wrap:wrap;align-items:center}
/* the nav is a group of paragraph links so the labels stay editable */
.top nav p{margin:0}
.top .wp-block-button{margin:0}
.top .wp-block-buttons.cta{padding:0;border:0;background:transparent;border-radius:0}
.top .cta .wp-block-button__link{font-size:14px;padding:12px 16px;background:transparent;color:inherit;border:1.5px solid var(--snow)}
.top .cta .wp-block-button__link:hover{background:rgba(255,255,255,.1)}
.top.scrolled .cta .wp-block-button__link{padding:10px 14px;font-size:13px;background:var(--sp);color:var(--snow);border-color:var(--sp)}
/* the follow row: each platform is a small group with a heading and a handle, and the mark comes from CSS so the text stays editable */
.follow .row-in{display:block;padding:22px 0;border-bottom:1.5px solid var(--rule)}
.follow .row-in h3{font:600 15px/1.3 var(--body);letter-spacing:0;margin:0}
.follow .row-in p{margin:0;color:var(--muted);font-size:17px}
.follow .row-in::before{content:"";display:block;width:28px;height:28px;margin-bottom:14px;background:var(--fg);-webkit-mask:var(--mark) center/contain no-repeat;mask:var(--mark) center/contain no-repeat}
%(marks)s
/* quotes are core quote blocks */
.words .wp-block-quote{margin:0;padding:18px 0 0;border:0;position:relative}
.words .wp-block-quote::before{content:"";position:absolute;left:0;right:0;top:0;height:1.5px;background:var(--ink);transform-origin:left;transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.words .wp-block-quote:nth-child(2)::before{transition-delay:.1s}.words .wp-block-quote:nth-child(3)::before{transition-delay:.2s}
.js .reveal.pre .wp-block-quote::before{transform:scaleX(0)}
.words .wp-block-quote p{font:800 clamp(22px,2.1vw,30px)/1.1 var(--display);letter-spacing:-.02em;margin:0 0 14px;text-wrap:balance}
.words .wp-block-quote cite{font:600 15px/1.3 var(--body);font-style:normal;display:block}.words .wp-block-quote cite span{font-weight:400}
/* the empty creators state and admin-only notes */
.gm-empty{padding:40px 0;color:var(--muted)}
.gm-newsletter-missing{font-size:14px;color:var(--muted);border:1.5px dashed var(--rule);padding:14px 16px;border-radius:12px}
.gm-newsletter{display:flex;gap:10px;flex-wrap:wrap;max-width:520px}
.gm-newsletter__label{flex-basis:100%%;font:600 12px/1.2 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.gm-newsletter__row{display:flex;gap:10px;flex-wrap:wrap;flex:1 1 100%%}
.gm-newsletter input{flex:1 1 220px;min-width:0;font:16px var(--body);padding:15px 20px;border-radius:999px;border:1.5px solid var(--rule);background:var(--card);color:var(--fg)}
.gm-newsletter__note{flex-basis:100%%;font-size:13px;color:var(--muted);margin:4px 0 0}
.gm-newsletter__ok{flex-basis:100%%;font:600 15px var(--body);color:var(--fg);margin:4px 0 0}
/* editor: show the page as it ships */
.editor-styles-wrapper .top{position:static}
"""


def svg_data_uri(inner, vb="0 0 24 24"):
    # a path filled with the icon background is a hole: fold it into the first path as an evenodd subpath
    holes = re.findall(r'<path d="([^"]+)" fill="var\(--icon-bg,#fff\)"/>', inner)
    inner = re.sub(r'<path d="[^"]+" fill="var\(--icon-bg,#fff\)"/>', "", inner)
    if holes:
        inner = re.sub(r'<path d="([^"]+)"', lambda m: '<path fill-rule="evenodd" d="%s %s"' % (m.group(1), " ".join(holes)), inner, count=1)
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">%s</svg>' % (vb, inner.replace("currentColor", "#000"))
    return "url(\"data:image/svg+xml,%s\")" % svg.replace("#", "%23").replace('"', "'").replace("<", "%3C").replace(">", "%3E")


def css():
    body = SP.CSS
    body = re.sub(r"@font-face\{[^}]*\}\n", "", body)
    marks = "\n".join(".follow .row-in.%s{--mark:%s}" % (k, svg_data_uri(v)) for k, v in SP.ICONS.items())
    return HEADER + body + WP_ADDITIONS % {"marks": marks}


def marks_php():
    icons = ",\n".join("\t\t%s => %s" % (json.dumps(k), json.dumps(v)) for k, v in SP.ICONS.items())
    return """<?php
/**
 * Hand-drawn marks shared with the splash mockup: the platform icons and the placeholder avatar.
 * Generated by brand/src/build_theme.py. Do not edit here.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Inner SVG for a platform mark, 24 units, one color (currentColor).
 *
 * @return array<string,string>
 */
function gm_mark_paths() {
	return array(
%s
	);
}

/**
 * A platform mark as an inline SVG.
 *
 * @param string $name instagram, tiktok, youtube or substack.
 * @param string $class CSS class on the svg.
 * @return string
 */
function gm_mark( $name, $class = 'ic' ) {
	$paths = gm_mark_paths();
	if ( ! isset( $paths[ $name ] ) ) {
		return '';
	}
	return '<svg class="' . esc_attr( $class ) . '" viewBox="0 0 24 24" aria-hidden="true">' . $paths[ $name ] . '</svg>';
}

/**
 * The placeholder avatar, a circle with a simple figure. Replaced by the creator's photo when one is set.
 *
 * @return string
 */
function gm_avatar_placeholder() {
	return %s;
}

/**
 * A logo file from assets/img as inline SVG, with a class and no role attribute.
 *
 * @param string $name File name without .svg.
 * @param string $class Class for the svg element.
 * @return string
 */
function gm_logo( $name, $class = 'lk' ) {
	$file = get_theme_file_path( 'assets/img/' . $name . '.svg' );
	if ( ! file_exists( $file ) ) {
		return '';
	}
	$svg = (string) file_get_contents( $file ); // phpcs:ignore WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
	$svg = str_replace( 'role="img"', '', $svg );
	return preg_replace( '/<svg /', '<svg class="' . esc_attr( $class ) . '" ', $svg, 1 );
}
""" % (icons, json.dumps(SP.avatar()))


def mural_json():
    return json.dumps(SP.mural_rows(), separators=(",", ":"))


def images():
    out = os.path.join(THEME, "assets", "img")
    for f in os.listdir(out):
        if f.endswith(".svg") or f.endswith(".jpg"):
            os.remove(os.path.join(out, f))
    for src, dst in (("lockup-compact.svg", "lockup-compact.svg"), ("lockup-compact-reversed.svg", "lockup-compact-reversed.svg"),
                     ("lockup-two-line-reversed.svg", "lockup-two-line-reversed.svg"), ("lockup-two-line.svg", "lockup-two-line.svg"),
                     ("favicon.svg", "icon.svg"), ("app-icon.svg", "app-icon.svg")):
        p = os.path.join(SIG, src)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(out, dst))


def build():
    write("generation-maine/style.css", css())
    write("generation-maine/assets/data/mural.json", mural_json())
    write("generation-maine/inc/marks.php", marks_php())
    images()
    print("theme: style.css, mural.json, marks.php, images")


if __name__ == "__main__":
    build()
