// Vercel Serverless Function to receive & store pre-registrations on Vercel Server
// 履歴は Vercel Blob（private ストア）に1件1ファイルで保存する。Vercel上では BLOB_STORE_ID（OIDC認証）またはBLOB_READ_WRITE_TOKENで認証される。

module.exports = async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const data = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    const logEntry = {
      timestamp: new Date().toISOString(),
      gender: data.gender || data['性別'] || '',
      age: data.age || data['年代'] || '',
      income: data.income || data['年収'] || '',
      email: data.email || data['メールアドレス'] || '',
      feedback: data.feedback || data['ご要望・ご期待'] || ''
    };

    // 常にログにも残す（Blob保存に失敗した場合のフォールバック）
    console.log('[RE.EN VERCEL SERVER DATA RECORD]', JSON.stringify(logEntry));

    let stored = false;
    try {
      // 読み込み失敗時も500にせず、ログ出力のみで継続させるため関数内で読み込む
      const { put } = require('@vercel/blob');
      const key = `registrations/${logEntry.timestamp.replace(/[:.]/g, '-')}.json`;
      await put(key, JSON.stringify(logEntry), {
        access: 'private',
        contentType: 'application/json',
        addRandomSuffix: true
      });
      stored = true;
    } catch (blobError) {
      console.error('[RE.EN BLOB STORE ERROR]', blobError);
    }

    // 個人情報を返さない
    return res.status(200).json({ status: 'ok', stored });
  } catch (error) {
    console.error('[RE.EN VERCEL SERVER ERROR]', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
