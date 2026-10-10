// 事前登録の一覧（Vercel Blob）を、集計JSONまたはCSVで返す管理用API。
// 合言葉は環境変数 ADMIN_EXPORT_KEY。ヘッダ x-export-key か ?key= で渡す。未設定のときは常に503を返す。
// GET /api/export            → 集計JSON（件数・性別・年代・年収・日別）
// GET /api/export?format=csv → 登録者一覧のCSV（Excel向けにBOM付きUTF-8）
const crypto = require('crypto');

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
