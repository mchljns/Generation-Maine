// Opens the block editor in Playground and validates every theme pattern and template with wp.blocks.parse.
import { chromium } from 'playwright';
const base = process.argv[2] || 'http://127.0.0.1:9400';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage();
await p.goto(base + '/wp-admin/post-new.php?post_type=page', { waitUntil: 'load' }); // auto-login happens here
await p.goto(base + '/wp-admin/post-new.php?post_type=page', { waitUntil: 'load' });
await p.waitForFunction(() => window.wp && wp.blocks && wp.blocks.getBlockTypes().length > 50, null, { timeout: 120000 });
const out = await p.evaluate(async () => {
  const pats = await wp.apiFetch({ path: '/wp/v2/block-patterns/patterns' });
  const tpls = await wp.apiFetch({ path: '/wp/v2/templates?per_page=50' });
  const parts = await wp.apiFetch({ path: '/wp/v2/template-parts?per_page=50' });
  const items = [
    ...pats.filter((x) => x.name.startsWith('generation-maine/')).map((x) => ['pattern ' + x.name, x.content]),
    ...tpls.filter((x) => x.theme === 'generation-maine').map((x) => ['template ' + x.slug, x.content.raw]),
    ...parts.filter((x) => x.theme === 'generation-maine').map((x) => ['part ' + x.slug, x.content.raw]),
  ];
  const bad = [];
  const walk = (blocks, name) => blocks.forEach((bl) => {
    if (!bl.isValid) bad.push({ name, block: bl.name, issues: (bl.validationIssues || []).map((i) => i.args.slice(0, 3).join(' ')).join(' | ').slice(0, 600) });
    walk(bl.innerBlocks || [], name);
  });
  items.forEach(([n, c]) => walk(wp.blocks.parse(c), n));
  return { checked: items.map((i) => i[0]), bad };
});
console.log(JSON.stringify(out, null, 1));
await b.close();
