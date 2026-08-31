// Vercel Serverless Function to receive & log pre-registrations
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const data = req.body;
    console.log('[RE.EN REGISTRATION LOG]', JSON.stringify({
      timestamp: new Date().toISOString(),
      ...data
    }));

    return res.status(200).json({ status: 'ok', message: 'Registration logged successfully' });
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
