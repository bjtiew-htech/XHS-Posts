#!/usr/bin/env node
// 自有渲染器：把 index.html 里每个 .poster 截成 PNG，并输出 DOM 几何检查结果。
//
//   node tools/render.mjs <index.html> --out <dir>      截图 + 几何检查
//   node tools/render.mjs <index.html> --check-only     只做几何检查（preflight 用）
//
// stdout 最后一行固定为 JSON：{"posters":[{id,width,height,scrollHeight,scrollWidth}], "files":[...]}
import { mkdirSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import { chromium } from 'playwright'

const args = process.argv.slice(2)
const htmlPath = resolve(args.find((a) => !a.startsWith('--') && args[args.indexOf(a) - 1] !== '--out') || '')
const outIdx = args.indexOf('--out')
const outDir = outIdx >= 0 ? resolve(args[outIdx + 1]) : null
const checkOnly = args.includes('--check-only')
if (!htmlPath.endsWith('.html') || (!checkOnly && !outDir)) {
  console.error('用法：node tools/render.mjs <index.html> --out <dir> | --check-only')
  process.exit(2)
}

const browser = await chromium.launch()
try {
  const page = await browser.newPage({ viewport: { width: 1600, height: 1800 }, deviceScaleFactor: 1 })
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' })
  await page.evaluate(async () => { await document.fonts.ready })
  await page.waitForTimeout(500)

  const posters = await page.evaluate(() =>
    [...document.querySelectorAll('.poster')].map((p, i) => {
      const r = p.getBoundingClientRect()
      return {
        id: p.id || `poster-${i + 1}`,
        width: Math.round(r.width),
        height: Math.round(r.height),
        scrollHeight: p.scrollHeight,
        scrollWidth: p.scrollWidth,
      }
    }))

  const files = []
  if (!checkOnly) {
    mkdirSync(outDir, { recursive: true })
    const els = await page.$$('.poster')
    for (const [i, el] of els.entries()) {
      const file = join(outDir, `${String(i + 1).padStart(2, '0')}.png`)
      await el.screenshot({ path: file })
      files.push(file)
    }
  }
  console.log(JSON.stringify({ posters, files }))
} finally {
  await browser.close()
}
