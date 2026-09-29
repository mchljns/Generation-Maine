# Generation Maine

Brand identity, splash page theme and copy for Generation Maine, an initiative of Maine Policy Institute.

| Folder | Contents |
| --- | --- |
| `generation-maine/` | The WordPress block theme. See [its README](generation-maine/README.md) to install, edit and switch brand directions |
| `dist/generation-maine.zip` | Ready-to-upload theme zip |
| `brand/` | Strategy, two creative directions, logo files, social kit, fonts and the brand guide (HTML and PDF) |
| `copy/` | Page copy with headline options |
| `qa/` | Screenshots, axe and Lighthouse results, and the QA scripts |
| `REPORT.md` | Summary of the work, assumptions, QA results and open questions for the client |

## Rebuilding brand files

The logos and social graphics are generated from code so they stay consistent.

```bash
npm install
pip install fonttools uharfbuzz brotli pillow
python3 brand/src/build_brand.py      # logo and social SVGs
node brand/src/render.mjs             # PNGs, favicon.ico, share card
python3 brand/src/build_directions.py # brand/directions.html
python3 brand/src/build_guide.py      # brand/brand-guide.html
node brand/src/guide-pdf.mjs          # brand/brand-guide.pdf
```
