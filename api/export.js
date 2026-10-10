// 事前登録の一覧（Vercel Blob）を、集計JSONまたはCSVで返す管理用API。
// 合言葉は環境変数 ADMIN_EXPORT_KEY。ヘッダ x-export-key か ?key= で渡す。未設定のときは常に503を返す。
// GET /api/export            → 集計JSON（件数・性別・年代・年収・日別）
// GET /api/export?view=1     → 合言葉を入れて集計とCSVを見る管理画面（HTML）
// GET /api/export?format=csv → 登録者一覧のCSV（Excel向けにBOM付きUTF-8）
const crypto = require('crypto');


const VIEW_HTML = `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>事前登録 Re.en（管理）</title>
<style>body{font:15px/1.7 -apple-system,"Noto Sans JP",sans-serif;margin:0;padding:24px 16px;background:#14161a;color:#e6e8ea}main{max-width:720px;margin:auto}h1{font-size:20px}input{width:100%;box-sizing:border-box;font:inherit;padding:8px;border-radius:6px;border:1px solid #444;background:#1d2025;color:inherit}button{font:inherit;padding:6px 16px;border-radius:6px;border:1px solid #9fb2f0;background:#9fb2f0;color:#14161a;font-weight:700;cursor:pointer;margin:8px 8px 8px 0}h2{font-size:13px;color:#959ca2;margin:20px 0 6px}.r{display:grid;grid-template-columns:minmax(90px,170px) 1fr 40px;gap:8px;align-items:center;font-size:13px}.t{height:8px;background:#2d3238;border-radius:4px;overflow:hidden}.f{display:block;height:100%;background:#9fb2f0}.n{text-align:right;font-family:monospace}</style></head><body><main>
<h1>事前登録 Re.en（管理）<span id="tot"></span></h1>
<input id="k" type="password" autocomplete="off" placeholder="合言葉" aria-label="合言葉">
<button id="go" type="button">読み込む</button><button id="csv" type="button" hidden>CSVをダウンロード</button><span id="st"></span>
<div id="body"></div></main>
<script>
var k=document.getElementById('k'),st=document.getElementById('st'),body=document.getElementById('body');
function call(fmt){var key=k.value.trim();if(!key){st.textContent='合言葉を入れてください';return Promise.reject()}
return fetch('/api/export'+(fmt?'?format='+fmt:''),{headers:{'x-export-key':key}}).then(function(r){
if(r.status===401)throw new Error('合言葉が違います');if(r.status===503)throw new Error('サーバに合言葉が設定されていません');if(!r.ok)throw new Error('読み込めませんでした（'+r.status+'）');
return fmt==='csv'?r.blob():r.json()})}
function bars(title,o){var h=document.createElement('h2');h.textContent=title;body.appendChild(h);
var rows=Object.keys(o).map(function(x){return[x,o[x]]}).sort(function(a,b){return b[1]-a[1]}),m=Math.max.apply(null,rows.map(function(r){return r[1]}).concat([1]));
rows.forEach(function(r){var d=document.createElement('div');d.className='r';var a=document.createElement('span');a.textContent=r[0];
var t=document.createElement('span');t.className='t';var f=document.createElement('span');f.className='f';f.style.width=Math.round(r[1]/m*100)+'%';t.appendChild(f);
var n=document.createElement('span');n.className='n';n.textContent=r[1];d.appendChild(a);d.appendChild(t);d.appendChild(n);body.appendChild(d)})}
document.getElementById('go').onclick=function(){st.textContent='読み込み中…';call().then(function(d){body.textContent='';
document.getElementById('tot').textContent='　'+d.total+'件（メール '+d.uniqueEmails+'件）';bars('性別',d.gender);bars('年代',d.age);bars('年収',d.income);bars('日別の件数',d.byDay);
document.getElementById('csv').hidden=false;st.textContent='更新しました'},function(e){if(e)st.textContent=e.message})};
document.getElementById('csv').onclick=function(){call('csv').then(function(b){var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='reen-registrations.csv';document.body.appendChild(a);a.click();a.remove()},function(e){if(e)st.textContent=e.message})};
</script></body></html>`;

function keyMatches(given, expected) {
  const a = crypto.createHash('sha256').update(String(given || '')).digest();
  const b = crypto.createHash('sha256').update(String(expected)).digest();
  return crypto.timingSafeEqual(a, b);
}

function csvCell(value) {
  let s = String(value == null ? '' : value);
  // 表計算ソフトで式として解釈されないようにする
  if (/^[=+\-@\t\r]/.test(s)) s = `'${s}`;
  return `"${s.replace(/"/g, '""')}"`;
}

async function readAll() {
  const { list, get } = require('@vercel/blob');
  const rows = [];
  let cursor;
  do {
    const page = await list({ prefix: 'registrations/', cursor, limit: 1000 });
    for (const b of page.blobs) {
      try {
        const res = await get(b.pathname, { access: 'private' });
        if (!res || res.statusCode !== 200) continue;
        rows.push(JSON.parse(await new Response(res.stream).text()));
      } catch (e) {
        console.error('[RE.EN EXPORT READ ERROR]', b.pathname, e && e.message);
      }
    }
    cursor = page.hasMore ? page.cursor : undefined;
  } while (cursor);
  rows.sort((x, y) => String(x.timestamp).localeCompare(String(y.timestamp)));
  return rows;
}

function tally(rows, field) {
  const out = {};
  for (const r of rows) {
    const k = r[field] || '未選択';
    out[k] = (out[k] || 0) + 1;
  }
  return out;
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'x-export-key');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method Not Allowed' });

  // 画面（データを含まない）。合言葉は画面内で入力し、同じ /api/export を呼ぶ
  if (req.query && req.query.view === '1') {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res.status(200).send(VIEW_HTML);
  }

  const expected = process.env.ADMIN_EXPORT_KEY;
  if (!expected) return res.status(503).json({ error: 'ADMIN_EXPORT_KEY is not configured' });

  const given = req.headers['x-export-key'] || (req.query && req.query.key);
  if (!keyMatches(given, expected)) return res.status(401).json({ error: 'Unauthorized' });

  try {
    const rows = await readAll();

    if (req.query && req.query.format === 'csv') {
      const header = ['登録日時(JST)', '性別', '年代', '年収', 'メールアドレス', 'ご要望・ご期待'];
      const lines = [header.map(csvCell).join(',')];
      for (const r of rows) {
        const jst = new Date(new Date(r.timestamp).getTime() + 9 * 3600 * 1000).toISOString().replace('T', ' ').slice(0, 19);
        lines.push([jst, r.gender, r.age, r.income, r.email, r.feedback].map(csvCell).join(','));
      }
      res.setHeader('Content-Type', 'text/csv; charset=utf-8');
      res.setHeader('Content-Disposition', 'attachment; filename="reen-registrations.csv"');
      return res.status(200).send('﻿' + lines.join('\r\n') + '\r\n');
    }

    const byDay = {};
    for (const r of rows) {
      const day = new Date(new Date(r.timestamp).getTime() + 9 * 3600 * 1000).toISOString().slice(0, 10);
      byDay[day] = (byDay[day] || 0) + 1;
    }
    return res.status(200).json({
      total: rows.length,
      uniqueEmails: new Set(rows.map((r) => String(r.email || '').toLowerCase()).filter(Boolean)).size,
      gender: tally(rows, 'gender'),
      age: tally(rows, 'age'),
      income: tally(rows, 'income'),
      byDay
    });
  } catch (error) {
    console.error('[RE.EN EXPORT ERROR]', error && error.message);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
};
