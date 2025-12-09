const express = require('express');
const router = express.Router();
const { format } = require('date-fns');
const { format: formatTZ, utcToZonedTime } = require('date-fns-tz');

router.get('/', (req, res) => {
  const now = new Date();
  const serverTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const zonedDate = utcToZonedTime(now, serverTimezone);

  res.json({
    message: 'Real Estate Agency API',
    serverTime: {
      utc: format(now, "yyyy-MM-dd'T'HH:mm:ss.SSSxxx"),
      serverLocal: formatTZ(zonedDate, "yyyy-MM-dd'T'HH:mm:ss.SSSxxx", { timeZone: serverTimezone }),
      serverTimezone: serverTimezone,
      note: 'This is server timezone.'
    },
    endpoints: {
      auth: '/api/auth',
      estates: '/api/estates',
      reviews: '/api/reviews',
      sales: '/api/sales'
    }
  });
});

module.exports = router;

