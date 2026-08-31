// Vercel Serverless Function to receive & log pre-registrations on Vercel Server
export default async function handler(req, res) {
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

    console.log('[RE.EN VERCEL SERVER DATA RECORD]', JSON.stringify(logEntry));

    return res.status(200).json({ 
      status: 'ok', 
      message: 'Preregistration stored on Vercel server successfully',
      record: logEntry
    });
  } catch (error) {
    console.error('[RE.EN VERCEL SERVER ERROR]', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
